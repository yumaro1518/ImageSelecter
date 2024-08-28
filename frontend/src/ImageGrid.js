import React, { useState } from 'react';
import ImageCard from './ImageCard';

function ImageGrid({ images }) {
  const [selectedImages, setSelectedImages] = useState([]);

  const handleSelectImage = (image) => {
    setSelectedImages((prevSelectedImages) => {
      if (prevSelectedImages.includes(image)) {
        return prevSelectedImages.filter((img) => img !== image);
      } else {
        return [...prevSelectedImages, image];
      }
    });
  };

  const handleSaveImages = () => {
    selectedImages.forEach((image) => {
      const link = document.createElement('a');
      link.href = image;
      link.download = image.split('/').pop();
      link.click();
    });
  };

  return (
    <div>
      <div className="image-grid">
        {images.map((image, index) => (
          <ImageCard
            key={index}
            image={image}
            onSelect={() => handleSelectImage(image)}
            isSelected={selectedImages.includes(image)}
          />
        ))}
      </div>
      <button onClick={handleSaveImages}>Save Selected Images</button>
    </div>
  );
}

export default ImageGrid;
