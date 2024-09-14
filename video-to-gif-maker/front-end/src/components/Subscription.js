import React from 'react';
import StripeCheckout from 'react-stripe-checkout';
import axios from 'axios';
import './Subscription.css'; // Optional for additional styling

const Subscription = () => {
  const handleToken = async (token) => {
    try {
      const response = await axios.post('/api/subscription', { token, user_id: 1, plan: 'basic' });
      alert('Subscription successful! Thank you for subscribing.');
      console.log('Subscription success:', response.data);
    } catch (error) {
      alert('Subscription error. Please try again.');
      console.error('Subscription error:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Choose Your Plan</h2>
      <div className="text-center">
        <p className="lead">Subscribe to our service and enjoy premium features.</p>
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Basic Plan</h5>
            <p className="card-text">Access to basic features and functionalities.</p>
            <p className="card-text"><strong>$10.00</strong> per month</p>
            <StripeCheckout
              token={handleToken}
              stripeKey="pk_test_51PysspP0YIgmInaD6KR5Dmq8IpDJm92IpO1yiCUWcOkxv6DlAoS7h38vtzAzxmjyIACCX6kPkToDUcFFbgSN3gMV004K4kg99O"
              name="Gif App Subscription"
              amount={1000} // Amount in cents
              currency="USD"
              description="Subscribe to the Basic Plan"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Subscription;
