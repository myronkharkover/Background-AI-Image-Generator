import json
import boto3
import base64
from botocore.exceptions import NoCredentialsError
import os
import openai
import cloudinary
from io import BytesIO
import requests

cloudinary.config( 
        cloud_name = "XXXXXXXX", 
        api_key = "XXXXXXXX", 
        api_secret = "XXXXXXXXXXX",
        secure = True 
)

import cloudinary.uploader
import cloudinary.api

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Parse the text prompt from the event
    text_prompt = event['body']
    game_Id = event['gameId']
    time_generated = event['timeGenerated']

    openai.api_key = os.environ["OpenAI_API_KEY"]

    # generate image with Dall-E
    response = openai.Image.create(
        prompt=text_prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )

    result = response["data"][0]["b64_json"]

    # Specify the bucket and key
    bucket = 'stablediffusionmyroncorrectregion'
    # / infront makes it a folder
    key = f'{game_Id}_{time_generated}_result.jpg'

    # delete all files with the same gameId that are in s3 to save space
    file_list = s3.list_objects_v2(Bucket=bucket)
    for obj in file_list['Contents']:
        if obj['Key'].startswith(game_Id):
            s3.delete_object(Bucket=bucket, Key=obj['Key'])
    
    # final image not compresed (about 3 MB)
    image_data = base64.b64decode(result)
    
    # upload image to cloudinary to compress (compressing happens with fetch_format='auto')
    cloudinary.uploader.upload(image_data, public_id=f'{game_Id}_result', unique_filename=False, overwrite=True, invalidate=True, folder="wiply-platform/Dall-E-Image-Generator", fetch_format="auto")

    srcURL = cloudinary.CloudinaryImage(f'wiply-platform/Dall-E-Image-Generator/{game_Id}_result').build_url()
    print(srcURL)

    # pull image from cloudinary and transform it so it can be uploaded to se 3
    # final_image = f'https://res.cloudinary.com/shulgirit/image/upload/wiply-platform/Dall-E-Image-Generator/{game_Id}_result.png.jpg'
    final_image = srcURL
    final_image_data = requests.get(final_image)

    # Upload the image data to S3
    try:
        # Upload the image data to S3 (accessed via cloudfront link: https://d10bnmsvmjptwd.cloudfront.net/{game_Id}_{time_generated}_result.png)
        s3.put_object(Body=final_image_data.content, Bucket=bucket, Key=key)
    except NoCredentialsError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No AWS credentials found'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }

    # Return the image
    return {
        'statusCode': 200,
        'body': json.dumps({'backgroundGeneratedImageURL': f'https://d10bnmsvmjptwd.cloudfront.net/{game_Id}_{time_generated}_result.jpg'}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
