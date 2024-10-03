import React, { useRef } from "react";
import "./SubscriptionPlans.css";
import StripeCheckout from 'react-stripe-checkout';
import { toast } from "react-toastify";
function SubscriptionPlans() {
  const stripeBtnRef = useRef(null);
  const handleToken = async (token) => {
    try {
      const response = await axios.post('/api/subscription', { token, user_id: 1, plan: 'basic' });
      // alert('Subscription successful! Thank you for subscribing.');
      console.log('Subscription success:', response.data);
    } catch (error) {
      // alert('Subscription error. Please try again.');
      console.error('Subscription error:', error);
    } finally {
      toast.success('Congratulations, You are a premium member now!')
    }
  };

  const handleCustomButtonClick = () => {
    // Programmatically trigger the hidden Stripe button click
    console.log(stripeBtnRef);
    
    stripeBtnRef.current.onClick();
  };


  return (
    <section className="subscription-plans" id="subscription-plans">
      <h2>Choose Your Plan</h2>
      <div className="plans-container">
        <div className="plan">
          <h3>Free Plan</h3>
          <p>Max GIF length: 5 seconds</p>
          <p>Limited to 5 conversions/day</p> <br />
          <button onClick={handleCustomButtonClick}  className="plan-btn">Sign Up</button>
        </div>
        <div className="plan">
          <h3>Pro Plan</h3>
          <p>Max GIF length: 30 seconds</p>
          <p>Unlimited conversions</p>
          <p>HD quality</p>
          <button onClick={handleCustomButtonClick} className="plan-btn">Subscribe - $9.99/month</button>
          <StripeCheckout
              token={handleToken}
              stripeKey="pk_test_51PysspP0YIgmInaD6KR5Dmq8IpDJm92IpO1yiCUWcOkxv6DlAoS7h38vtzAzxmjyIACCX6kPkToDUcFFbgSN3gMV004K4kg99O"
              name="Gif App Subscription"
              amount={1000} // Amount in cents
              currency="USD"
              description="Subscribe to the Basic Plan"
              ref={stripeBtnRef}
              style={{ display: "none" }}
            />
        </div>
        <div className="plan">
          <h3>Enterprise Plan</h3>
          <p>Custom length & features</p> <br /> <br /> <br />
          <button className="plan-btn">Contact Us</button>
        </div>
      </div>
    </section>
  );
}

export default SubscriptionPlans;
