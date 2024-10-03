import React from "react";
import "./Features.css";

function Features() {
  return (
    <section className="features" id="features">
      <h2>Why Choose Our Converter?</h2>
      <div className="features-grid">
        <div className="feature-item">
          <h3>Fast Conversion</h3>
          <p>Lightning-speed processing for quick GIF creation.</p>
        </div>
        <div className="feature-item">
          <h3>Customizable Settings</h3>
          <p>Adjust resolution, frame rate, and loop settings.</p>
        </div>
        <div className="feature-item">
          <h3>No Watermarks</h3>
          <p>Clean, watermark-free GIFs for premium users.</p>
        </div>
        <div className="feature-item">
          <h3>Cross-Platform</h3>
          <p>Works on any device and browser.</p>
        </div>
      </div>
    </section>
  );
}

export default Features;
