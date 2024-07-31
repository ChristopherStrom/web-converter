import React, { useState } from 'react';
import axios from 'axios';
import { useParams, useHistory } from 'react-router-dom';
import { Puff } from 'react-loader-spinner';

const ModulePage = () => {
  const { moduleId } = useParams();
  const history = useHistory();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    console.log('File selected:', e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    console.log('Form submitted. Starting file upload.');

    try {
      const response = await axios.post(`/api/convert/${moduleId}`, formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log('File upload successful:', response);

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', response.headers['content-disposition'].split('filename=')[1]);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
      console.log('File upload complete. Redirecting to root.');
      history.push('/');
    }
  };

  return (
    <div>
      <h1>Convert File - {moduleId}</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? (
            <Puff color="#00BFFF" height={24} width={24} />
          ) : (
            'Convert'
          )}
        </button>
      </form>
    </div>
  );
};

export default ModulePage;
