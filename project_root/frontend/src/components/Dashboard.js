import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard({ isAuthenticated }) {
  const navigate = useNavigate();
  const [repositories, setRepositories] = useState([]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/');
    } else {
      fetchRepositories();
    }
  }, [isAuthenticated, navigate]);

  const fetchRepositories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/repositories/', {
        method: 'GET',
        credentials: 'include',
      });
      const data = await response.json();
      setRepositories(data);
    } catch (error) {
      console.error('Error fetching repositories:', error);
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <h2>Your Repositories:</h2>
      <ul>
        {repositories.map((repo) => (
          <li key={repo.id}>{repo.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;