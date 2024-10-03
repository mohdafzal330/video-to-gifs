import React from "react";
import "./HowItWorks.css";

function HowItWorks() {
  return (
    <section className="how-it-works" id="howItWorks">
      <h2>How to Convert Your Video to a GIF</h2>
      <div className="steps-container">
        <div className="step">
          <h3>Step 1</h3>
          <p>Upload your video.</p>
        </div>
        <div className="step">
          <h3>Step 2</h3>
          <p>Customize your GIF.</p>
        </div>
        <div className="step">
          <h3>Step 3</h3>
          <p>Download and share!</p>
        </div>
      </div>
    </section>
  );
}

export default HowItWorks;
