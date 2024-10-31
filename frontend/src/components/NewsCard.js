import React, { useEffect, useState } from 'react';
import '../styles/NewsCard.css';
import { fetchNewsUrl } from '../services/api';

function NewsCard({ title, content, NewsID }) {
  const [provider, setProvider] = useState('Unknown Provider');

  useEffect(() => {
    const getProvider = async () => {
      const newsData = await fetchNewsUrl(NewsID);
      if (newsData.url) {
        const url = newsData.url;

        // Determine the provider based on the URL prefix
        if (url.substring(0, 15) === 'https://edition') {
          setProvider('CNN News');
        } else if (url.substring(0, 15) === 'https://eu.usat') {
          setProvider('USA Today News');
        } else {
          setProvider('Unknown Provider');
        }
      } else {
        setProvider('Unknown Provider');
      }
    };

    getProvider();
  }, [NewsID]);

  const handleReadMore = async () => {
    const newsData = await fetchNewsUrl(NewsID);
    if (newsData.url) {
      window.open(newsData.url, '_blank');
    } else {
      alert('URL not available');
    }
  };

  const providerStyle = {
    backgroundColor: provider === 'CNN News' ? '#CC0000' : provider === 'USA Today News' ? '#009BFF' : '#ffcc00',
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: '1rem',
    padding: '5px 10px',
    borderRadius: '5px',
    marginRight: '10px',
  };

  return (
    <div className="news-card">
      <h2>{title}</h2>
      {/* Check if content exists before calling substring */}
      <p>{content ? content.substring(0, 150) : 'No content available'}...</p>
      <span className="news-provider" style={providerStyle}>{provider}</span>
      <button onClick={handleReadMore} className="read-more-button">Read More</button>
    </div>
  );
}

export default NewsCard;
