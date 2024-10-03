import React, { useState } from "react";
import "./App.css";
import Navbar from "./Navbar";
import Hero from "./Hero";
import Features from "./Features";
import SubscriptionPlans from "./SubscriptionPlans";
import HowItWorks from "./HowItWorks";
import Footer from "./Footer";
import LoginModal from "./LoginModal";
import SignupModal from "./SignupModal";
// import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const handleLoginOpen = () => setShowLogin(true);
  const handleLoginClose = () => setShowLogin(false);

  const handleSignupOpen = () => setShowSignup(true);
  const handleSignupClose = () => setShowSignup(false);

  return (
    <div className="App">
      <Navbar onLoginClick={handleLoginOpen} onSignupClick={handleSignupOpen} />
      <Hero />
      <Features />
      <SubscriptionPlans />
      <HowItWorks />
      <Footer />

      <LoginModal show={showLogin} handleClose={handleLoginClose} />
      <SignupModal show={showSignup} handleClose={handleSignupClose} />
    </div>
  );
}

export default App;
