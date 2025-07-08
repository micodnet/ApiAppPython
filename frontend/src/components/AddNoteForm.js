import React, { useState } from 'react';
import axios from 'axios';
        
const AddNoteForm = ({ setNotes }) => {
  const [titre, setTitre] = useState('');
  const [contenu, setContenu] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("http://localhost:8000/ajouter-note", { titre, contenu })
      .then(() => {
        setNotes(prev => [...prev, { titre, contenu }]);
        setTitre('');
        setContenu('');
      })
      .catch(error => console.log(error));
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "30px" }}>
      <h2>📝 Ajouter une note</h2>
      <input 
        type="text" 
        value={titre} 
        onChange={(e) => setTitre(e.target.value)} 
        placeholder="Titre" 
        required 
      />
      <br />
      <textarea 
        value={contenu} 
        onChange={(e) => setContenu(e.target.value)} 
        placeholder="Contenu" 
        rows="4"
        required 
      />
      <br />
      <button type="submit">➕ Ajouter</button>
    </form>
  );
}
 

export default AddNoteForm;
