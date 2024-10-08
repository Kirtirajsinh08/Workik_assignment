// src/components/Home.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home({ setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleGitHubAuth = async () => {
    try {
      console.log('Initiating GitHub auth request');
      const response = await fetch('http://localhost:8000/api/github-auth/', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Received data:', data);
      
      if (data.authorization_url) {
        console.log('Redirecting to:', data.authorization_url);
        window.location.href = data.authorization_url;
      } else {
        console.error('No authorization URL received');
      }
    } catch (error) {
      console.error('Error during GitHub authentication:', error);
      console.error('Error details:', error.message);
      if (error instanceof TypeError) {
        console.error('Network error. Is the backend server running?');
      }
    }
  };

  return (
    <div>
      <h1>GitHub PR Review System</h1>
      <button onClick={handleGitHubAuth}>Connect GitHub</button>
    </div>
  );
}

export default Home;