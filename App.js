import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [prompt, setPrompt] = useState('');
  const [imageSrc, setImageSrc] = useState('');

  const handleGenerateClick = () => {
    const timestamp = new Date().toISOString();

    const requestBody = JSON.stringify({ body: prompt, gameId: "websiteTest2", timeGenerated: timestamp});
    console.log(requestBody);
    // Set the headers to indicate JSON content
    const headers = {
      'Content-Type': 'application/json',
    };


    // Make an HTTP POST request to the Lambda function endpoint
    axios.post('https://9g6hwsnbu4.execute-api.us-east-1.amazonaws.com/Dev/stableDiffusionMyronNOTBROKEN', requestBody, { headers })
    .then(response => {
      // Assuming the response data contains the CloudFront link for the image
      const imageUrl = `https://d10bnmsvmjptwd.cloudfront.net/websiteTest2_${timestamp}_result.jpg`;
      setImageSrc(imageUrl);
    })  
    .catch(error => {
      console.error('Error:', error);
      setImageSrc('');
    });
  };
  
  return (
    <div className="App">
      <div className="App-header">
        <p>
          Prompt of Image You Want to Generate
        </p>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          style={{ width: '30%', padding: '10px' }}
        />

        <div>
          <button style={{ backgroundColor: '#5c12a6', color: 'white', fontSize: '20px', fontFamily: 'Courier-Bold' }} onClick={handleGenerateClick}>Generate</button>
        </div>

        {imageSrc && (
          <div>
            <img src={imageSrc} alt="Generated Image"/>
          </div>
        )}

        <div className="iframe-container">
          <p>
          Here is a sample game with the background set to an image I generated from this plugin with prompt:
          </p>
          <p>"house built in a huge Soap bubble, windows, doors, porches, awnings, middle of SPACE, cyberpunk lights, Hyper Detail, 8K, HD, Octane Rendering, Unreal Engine, V-Ray, full hd "</p>
          <iframe title="wiply-game" src="https://myron-680e6a.wiplify.com/" width="640px" height="700px"/>
        </div>
      </div>
    </div>
  );
}

export default App;
