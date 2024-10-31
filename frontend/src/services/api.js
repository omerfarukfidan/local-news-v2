export const fetchNews = async () => {
  try {
    const response = await fetch('/news');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  } catch (error) {
    console.error('Failed to fetch news:', error);
    return [];
  }
};

export const fetchCityNews = async (city) => {
  try {
    const response = await fetch(`/news/${city}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  } catch (error) {
    console.error(`Failed to fetch news for city ${city}:`, error);
    return [];
  }
};

export const fetchDistinctCities = async () => {
  try {
    const response = await fetch('/distinct-cities');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  } catch (error) {
    console.error('Failed to fetch distinct cities:', error);
    return [];
  }
};

export const fetchNewsUrl = async (newsId) => {
  try {
    const response = await fetch(`/news-url/${newsId}`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  } catch (error) {
    console.error(`Failed to fetch news URL for news ID ${newsId}:`, error);
    return { url: '' };
  }
};
