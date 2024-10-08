import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home({ setIsAuthenticated }) {
  const navigate = useNavigate();

  const handleGitHubAuth = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/github-auth/', {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      window.location.href = data.authorization_url;
    } catch (error) {
      console.error('Error during GitHub authentication:', error);
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