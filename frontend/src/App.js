import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    await axios
      .get('http://localhost:5000/api/data')
      .then(response => {
        setMessage(response.data.message);
      })
  };

  return (
    <div className="App">
      <h1>React Frontend</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;