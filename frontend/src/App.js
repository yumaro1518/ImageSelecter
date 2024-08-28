import React, { useState } from 'react';
import UrlInput from './UrlInput';
import ImageGrid from './ImageGrid';

function App() {
  const [images, setImages] = useState([]);

  const handleUrlSubmit = async (url) => {
    try {
      const response = await fetch('http://localhost:5000/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      setImages(data.images);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  return (
    <div>
      <h1>Image Scraper</h1>
      <UrlInput onSubmit={handleUrlSubmit} />
      <ImageGrid images={images} />
    </div>
  );
}

export default App;
