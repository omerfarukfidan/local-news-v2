import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Dropdown from '../components/Dropdown';
import SlidingMenu from '../components/SlidingMenu';
import '../styles/Home.css';

function Home() {
  const handleSelect = (city) => {
    if (city) {
      window.location.href = `/city/${city}`;
    }
  };

  return (
    <div className="home-container">
      <Header />
      <div className="content">
        <h2 className="home-title">Find Local News for Your City</h2>
        <Dropdown onSelect={handleSelect} />
      </div>
      <Footer />
      <SlidingMenu />
    </div>
  );
}

export default Home;
