import React from "react";
import "./GifGallery.css";

function GifGallery({ gifs }) {
  return (
    <section className="gif-gallery">
      <h2>GIF Gallery</h2>
      <div className="gallery-grid">
        {gifs.length === 0 ? (
          <p>No GIFs uploaded yet!</p>
        ) : (
          gifs.map((gif, index) => (
            <div className="gif-item" key={index}>
              <img src={gif.url} alt={`GIF ${index + 1}`} />
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export default GifGallery;
``;
