import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RootPage.css';

const RootPage = () => {
  const [modules, setModules] = useState([]);

  useEffect(() => {
    const fetchModules = async () => {
      try {
        const response = await axios.get('/api/modules');
        setModules(response.data);
      } catch (error) {
        console.error('Error fetching modules:', error);
      }
    };

    fetchModules();
  }, []);

  return (
    <div className="root-container">
      <header className="header">
        <h1>File Conversion Tools</h1>
      </header>
      <div className="modules-container">
        {modules.map((module) => (
          <div key={module.id} className="module-card">
            <h2>{module.name}</h2>
            <p>Category: {module.category}</p>
            <a href={`/convert/${module.id}`} className="convert-button">
              Convert
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RootPage;
