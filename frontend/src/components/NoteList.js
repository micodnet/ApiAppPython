import React from 'react';

const NoteList = ({ notes, onDelete, onEdit }) => {
  return (
    <div>
      <h2>📄 Liste des notes</h2>
      {notes.length === 0 && <p>Aucune note trouvée.</p>}
      {notes.map(note => (
        <div key={note.id} style={{
          border: '1px solid #ccc',
          marginBottom: '15px',
          padding: '15px',
          borderRadius: '8px',
          backgroundColor: '#f9f9f9'
        }}>
          <h3>{note.titre}</h3>
          <p>{note.contenu}</p>
          <button onClick={() => onDelete(note.id)}>🗑 Supprimer</button>
          <button onClick={() => onEdit(note)} style={{ marginLeft: "10px" }}>✏ Modifier</button>
        </div>
      ))}
    </div>
  );
};

export default NoteList;
