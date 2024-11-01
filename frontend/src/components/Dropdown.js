import React, { useState, useEffect, useRef } from 'react';
import { fetchDistinctCities } from '../services/api';
import '../styles/Dropdown.css';

function Dropdown({ onSelect }) {
  const [options, setOptions] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const getCities = async () => {
      const cities = await fetchDistinctCities();
      setOptions(cities);
      setFilteredOptions(cities);
    };
    getCities();
  }, []);

  const handleSearch = (e) => {
    const term = e.target.value;
    setSearchTerm(term);
    if (term === '') {
      setFilteredOptions(options);
    } else {
      setFilteredOptions(options.filter((city) => city.toLowerCase().includes(term.toLowerCase())));
    }
  };

  const handleSelect = (city) => {
    setSearchTerm(city);
    onSelect(city);
    setIsOpen(false);
  };

  const handleClear = () => {
    setSearchTerm('');
    setFilteredOptions(options);
    setIsOpen(false);
  };

  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="dropdown-container" ref={dropdownRef}>
      <div className="search-container">
        <input
          type="text"
          value={searchTerm}
          onChange={handleSearch}
          onFocus={() => setIsOpen(true)}
          placeholder="Search for a city..."
          className="search-input"
        />
        {searchTerm && (
          <button onClick={handleClear} className="clear-button">
            &#10005; {/* X symbol */}
          </button>
        )}
      </div>
      {isOpen && (
        <div className="dropdown-menu">
          {filteredOptions.map((city, index) => (
            <div key={index} onClick={() => handleSelect(city)} className="dropdown-item">
              {city}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dropdown;
