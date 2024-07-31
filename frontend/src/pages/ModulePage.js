import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ModulePage = () => {
  const { moduleId } = useParams();
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    axios.post(`/api/convert/${moduleId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => setResult(response.data))
    .catch(error => console.error('Error uploading file:', error));
  };

  return (
    <div>
      <h1>Convert File - {moduleId}</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Convert</button>
      </form>
      {result && <div>
        <h2>Conversion Result</h2>
        <p>{result.message}</p>
        {/* Display conversion result, e.g., a link to the converted file */}
      </div>}
    </div>
  );
};

export default ModulePage;
