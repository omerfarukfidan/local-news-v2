import React, { useState, useEffect } from 'react';
import { fetchDistinctCities } from '../services/api';
import '../styles/Dropdown.css';

function Dropdown({ onSelect }) {
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('');

  useEffect(() => {
    const getCities = async () => {
      const cities = await fetchDistinctCities();
      setOptions(cities);
    };
    getCities();
  }, []);

  const handleChange = (e) => {
    setSelectedOption(e.target.value);
    onSelect(e.target.value);
  };

  return (
    <select value={selectedOption} onChange={handleChange} className="dropdown">
      <option value="">Select a city...</option>
      {options.map((option, index) => (
        <option key={index} value={option}>{option}</option>
      ))}
    </select>
  );
}

export default Dropdown;