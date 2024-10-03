import React from "react";
import "./LoginModal.css";

function LoginModal({ show, handleClose }) {
  if (!show) return null;

  return (
    <div className="modal-overlay" style={{zIndex:2}}>
      <div className="modal">
        <h2>Login</h2>
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button>Login</button>
        <p>Forgot your password?</p>
        <button className="close-btn" onClick={handleClose}>
          Close
        </button>
      </div>
    </div>
  );
}

export default LoginModal;
