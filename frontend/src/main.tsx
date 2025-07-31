import React, { useState, useEffect } from 'react';

function App() {
  const [listText, setListText] = useState('');
  const [loading, setLoading] = useState(true);

  // Fetch list from backend
  useEffect(() => {
    fetch('/api/get-list')
      .then(res => res.json())
      .then(data => {
        setListText(data.join('\n')); // Convert list to newline-separated string
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching list:', err);
        setLoading(false);
      });
  }, []);

  // Handle sending updated list to backend
  const handleSave = () => {
    const updatedList = listText
      .split('\n')
      .map(item => item.trim())
      .filter(item => item !== '');

    fetch('/api/update-list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedList),
    })
      .then(res => {
        if (res.ok) alert('List updated!');
        else throw new Error('Failed to update');
      })
      .catch(err => alert('Error: ' + err.message));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Editable List</h2>
      <textarea
        rows={10}
        cols={40}
        value={listText}
        onChange={(e) => setListText(e.target.value)}
      />
      <br />
      <button onClick={handleSave}>Save List</button>
    </div>
  );
}

export default App;
