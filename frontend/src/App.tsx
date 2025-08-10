import React, { useState, useEffect } from 'react';
import type { ChangeEvent } from 'react';

const App: React.FC = () => {
  const [listText, setListText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch the list from backend on mount
  useEffect(() => {
    const fetchList = async () => {
      try {
        const res = await fetch('http://localhost:5000/getQualifications');
        const data: string[] = await res.json();
        setListText(data.join('\n'));
      } catch (err) {
        console.error('Fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchList();
  }, []);


  // Update list text as user types
  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setListText(e.target.value);
  };

  // Send the updated list to the backend
  const handleSave = () => {
    const updatedList: string[] = listText
      .split('\n')
      .map(item => item.trim())
      .filter(item => item !== '');

    fetch('http://localhost:5000/setQualificationListToList', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qualifications: updatedList }),
    })
      .then(res => {
        if (res.ok) alert('Qualifications updated!');
        else throw new Error('Failed to update');
      })
      .catch(err => alert('Error: ' + err.message));
  };


  if (loading) return <div>Loading...</div>;

  console.log("App rendered");


  return (
    <div style={{ padding: '20px' }}>
      <h2>Editable List</h2>
      <textarea
        rows={30}
        cols={150}
        value={listText}
        onChange={handleChange}
      />
      <br />
      <button onClick={handleSave}>Save List</button>
    </div>
  );
};

export default App;
