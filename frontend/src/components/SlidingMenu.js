import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/SlidingMenu.css';

function SlidingMenu() {
  return (
    <div className="sliding-menu">
      <Link to="/">Home</Link>
      <Link to="/city/Global">Global News</Link>
    </div>
  );
}

export default SlidingMenu;