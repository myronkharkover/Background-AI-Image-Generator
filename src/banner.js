import React from 'react';
import styles from "./banner.module.css";
import logo from './knicksPlayers.jpeg';

const Banner = () => {
  return (
    <header className="row mb-5" style={{ backgroundColor: '#282c34' }}>
      <div className="col-10">
        <img src={logo} alt="banner" className={styles.banner} />
      </div>
    </header>
  );
};

export default Banner;
