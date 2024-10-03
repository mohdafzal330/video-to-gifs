import React from "react";
import "./Navbar.css";

function Navbar({ onLoginClick, onSignupClick }) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">GIF Studio | Ventures</div>
      <ul className="navbar-links">
        <li>
          <a href="#hero">Home</a>
        </li>
        <li>
          <a href="#features">Features</a>
        </li>
        <li>
          <a href="#subscription-plans">Subscription</a>
        </li>
        <li>
          <a href="#howItWorks">Help</a>
        </li>
        <li>
          <button onClick={onLoginClick} className="login-btn">
            Login
          </button>
        </li>
        <li>
          <button onClick={onSignupClick} className="signup-btn">
            Sign Up
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
