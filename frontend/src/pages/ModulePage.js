import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Puff } from 'react-loader-spinner';

const ModulePage = () => {
  const { moduleId } = useParams();
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);

    axios.post(`/api/convert/${moduleId}`, formData, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', response.headers['content-disposition'].split('filename=')[1]);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      setResult("File converted successfully");
    })
    .catch(error => console.error('Error uploading file:', error))
    .finally(() => setLoading(false));
  };

  return (
    <div>
      <h1>Convert File - {moduleId}</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Convert</button>
      </form>
      {loading && (
        <div>
          <Puff color="#00BFFF" height={100} width={100} />
          <p>Processing...</p>
        </div>
      )}
      {result && <div>
        <h2>Conversion Result</h2>
        <p>{result}</p>
      </div>}
    </div>
  );
};

export default ModulePage;
