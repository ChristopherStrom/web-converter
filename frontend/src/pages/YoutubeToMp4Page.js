import React, { useState } from 'react';
import axios from 'axios';

const YoutubeToMp4Page = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) {
      alert('Please enter a YouTube URL');
      return;
    }
    setLoading(true);

    try {
      const response = await axios.post('/api/convert/youtube_to_mp4', { url }, {
        responseType: 'blob'
      });
      const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.setAttribute('download', 'video.mp4');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Error downloading video:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>YouTube to MP4 Converter</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" value={url} onChange={handleUrlChange} placeholder="Enter YouTube URL" />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Convert'}
        </button>
      </form>
    </div>
  );
};

export default YoutubeToMp4Page;
