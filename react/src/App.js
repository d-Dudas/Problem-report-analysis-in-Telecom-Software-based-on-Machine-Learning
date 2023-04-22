import React, { useState, useEffect } from 'react';

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('/api/data')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  return (
    <div>
      <h1>{data.message}</h1>
      <p>{data.msg}</p>
    </div>
  );
}

export default App;