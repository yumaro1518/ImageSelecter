import React from 'react';

function ImageCard({ image, onSelect, isSelected }) {
  return (
    <div className={`image-card ${isSelected ? 'selected' : ''}`} onClick={onSelect}>
      <img src={image} alt="Scraped" />
    </div>
  );
}

export default ImageCard;
