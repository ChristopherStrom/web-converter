import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const RootPage = () => {
  const [modules, setModules] = useState([]);
  const [categories, setCategories] = useState({});

  useEffect(() => {
    axios.get('/api/modules')
      .then(response => {
        const modules = response.data;
        setModules(modules);

        const categorizedModules = modules.reduce((acc, module) => {
          const category = module.category || 'Uncategorized';
          if (!acc[category]) {
            acc[category] = [];
          }
          acc[category].push(module);
          return acc;
        }, {});
        setCategories(categorizedModules);
      })
      .catch(error => console.error('Error fetching modules:', error));
  }, []);

  return (
    <div>
      <h1>File Conversion Tools</h1>
      {Object.keys(categories).map(category => (
        <div key={category}>
          <h2>{category}</h2>
          <ul>
            {categories[category].map(module => (
              <li key={module.id}>
                <Link to={`/convert/${module.id}`}>{module.name}</Link>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default RootPage;
