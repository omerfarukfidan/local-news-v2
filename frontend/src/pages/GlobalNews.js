import React, { useEffect, useState } from 'react';
import NewsList from '../components/NewsList';
import SlidingMenu from '../components/SlidingMenu';
import { fetchNews } from '../services/api';
import '../styles/GlobalNews.css';

function GlobalNews() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    const getNews = async () => {
      const newsData = await fetchNews();
      setNews(newsData.filter((article) => article.type === 'global'));
    };
    getNews();
  }, []);

  return (
    <div className="global-news-container">
      <h2>Global News</h2>
      <NewsList news={news} />
      <SlidingMenu />
    </div>
  );
}

export default GlobalNews;