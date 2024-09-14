import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Dashboard.css';  // Optional for additional styles

const Dashboard = () => {
  const [gifs, setGifs] = useState([]);

  useEffect(() => {
    const fetchGifs = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/gifs');
        setGifs(response.data);
      } catch (error) {
        console.error('Error fetching GIFs:', error);
      }
    };
    fetchGifs();
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Your GIF Dashboard</h2>
      {gifs.length === 0 ? (
        <p className="text-center">No GIFs available at the moment</p>
      ) : (
        <div className="row">
          {gifs.map((gif) => (
            <div className="col-md-4 mb-4" key={gif.id}>
              <div className="card h-100">
                <img src={gif.gif_url} className="card-img-top" alt={gif.title} />
                <div className="card-body">
                  <h5 className="card-title">{gif.title || 'GIF'}</h5>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
