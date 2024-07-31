import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ModulePage = () => {
  const { moduleId } = useParams();
  const [moduleInfo, setModuleInfo] = useState(null);
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchModuleInfo = async () => {
      try {
        const response = await axios.get('/api/modules');
        const module = response.data.find(mod => mod.id === moduleId);
        setModuleInfo(module);
      } catch (error) {
        console.error('Error fetching module info:', error);
      }
    };

    fetchModuleInfo();
  }, [moduleId]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      let response;
      if (moduleInfo.input_type === 'file') {
        if (!file) {
          alert('Please select a file');
          setLoading(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', file);
        response = await axios.post(`/api/convert/${moduleId}`, formData, {
          responseType: 'blob'
        });
      } else if (moduleInfo.input_type === 'url') {
        if (!url) {
          alert('Please enter a URL');
          setLoading(false);
          return;
        }
        response = await axios.post(`/api/convert/${moduleId}`, { url }, {
          responseType: 'blob'
        });
      }

      const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'output.mp4');  // Adjust the file name and extension accordingly
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Error during conversion:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!moduleInfo) return <div>Loading...</div>;

  return (
    <div>
      <h1>{moduleInfo.name}</h1>
      <form onSubmit={handleSubmit}>
        {moduleInfo.input_type === 'file' && (
          <input type="file" onChange={handleFileChange} />
        )}
        {moduleInfo.input_type === 'url' && (
          <input type="text" value={url} onChange={handleUrlChange} placeholder="Enter URL" />
        )}
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Convert'}
        </button>
      </form>
    </div>
  );
};

export default ModulePage;
