import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ConnectionTable = () => {
  const [connections, setConnections] = useState([]);

  useEffect(() => {
    fetchConnections();
  }, []);

  const fetchConnections = async () => {
    const response = await axios.get('/api/connections');
    setConnections(response.data);
  };

  const handleAccept = async (profileUrl) => {
    await axios.post(`/api/connections/${profileUrl}/accept`);
    fetchConnections();
  };

  const handleMessage = async (profileUrl) => {
    const message = "Thanks for connecting! Looking forward to networking with you.";
    await axios.post(`/api/connections/${profileUrl}/message`, { message });
  };

  return (
    <div className="container">
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Title</th>
            <th>Score</th>
            <th>Message</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {connections.map((connection) => (
            <tr key={connection.profile_url}>
              <td>{connection.name}</td>
              <td>{connection.title}</td>
              <td>{connection.score}</td>
              <td>{connection.message}</td>
              <td>
                <button 
                  onClick={() => handleAccept(connection.profile_url)}
                  className={`btn ${connection.score >= 70 ? 'btn-success' : 'btn-warning'}`}
                >
                  {connection.score >= 70 ? 'Accept' : 'Review'}
                </button>
                <button 
                  onClick={() => handleMessage(connection.profile_url)}
                  className="btn btn-primary ml-2"
                >
                  Send Message
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ConnectionTable; 