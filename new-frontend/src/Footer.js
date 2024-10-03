import React from "react";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <ul className="footer-links">
        <li>
          <a href="#">About Us</a>
        </li>
        <li>
          <a href="#">Privacy Policy</a>
        </li>
        <li>
          <a href="#">Terms of Service</a>
        </li>
        <li>
          <a href="#">Contact Us</a>
        </li>
      </ul>
      <div className="footer-socials">
        <a href="#" aria-label="Facebook">
          <i className="fab fa-facebook"></i>
        </a>
        <a href="#" aria-label="Twitter">
          <i className="fab fa-twitter"></i>
        </a>
        <a href="#" aria-label="Instagram">
          <i className="fab fa-instagram"></i>
        </a>
      </div>
      <p>
        &copy; 2024 Gif Studio | Powered by Persist Ventures. All Rights
        Reserved.
      </p>
      <p style={{ color: "white", fontSize: 15 }}>
        Designed and developed by Mohammed Afzal Khan
      </p>
    </footer>
  );
}

export default Footer;
