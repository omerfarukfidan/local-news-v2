import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CityNews from './pages/CityNews';
import GlobalNews from './pages/GlobalNews';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/city/:city" element={<CityNews />} />
        <Route path="/global" element={<GlobalNews />} />
      </Routes>
    </Router>
  </React.StrictMode>
);