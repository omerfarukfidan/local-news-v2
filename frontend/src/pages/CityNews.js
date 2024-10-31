import React, { useEffect, useState } from 'react';
import NewsList from '../components/NewsList';
import SlidingMenu from '../components/SlidingMenu';
import { fetchCityNews } from '../services/api';
import { useParams } from 'react-router-dom';
import '../styles/CityNews.css';

function CityNews() {
  const { city } = useParams();
  const [news, setNews] = useState([]);

  useEffect(() => {
    const getNews = async () => {
      const newsData = await fetchCityNews(city);
      setNews(newsData);
    };
    getNews();
  }, [city]);

  return (
    <div className="city-news-container">
      <h2>News in {city}</h2>
      <NewsList news={news} />
      <SlidingMenu />
    </div>
  );
}

export default CityNews;