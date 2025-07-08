import React, { useState, useEffect } from "react";
import './App.css';
import axios from 'axios';
import NoteList from './components/NoteList';
import AddNoteForm from './components/AddNoteForm';
import EditNoteForm from './components/EditNoteForm';

function App() {
  const [notes, setNotes] = useState([]);
  const [editingNote, setEditingNote] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/notes")
      .then(res => res.ok ? res.json() : Promise.reject(res))
      .then(data => setNotes(data))
      .catch(err => console.error("Erreur HTTP :", err));
  }, []);

  return (
    <div style={{ fontFamily: "Arial, sans-serif", margin: "2rem" }}>
      <h1>Mes notes (FastAPI + SQLite)</h1>
      {notes.length === 0 ? (
        <p>Aucune note trouvée.</p>
      ) : (
        <ul>
          {notes.map(note => (
            <li key={note.id} style={{ marginBottom: "0.5rem" }}>
              <strong>{note.titre}</strong> : {note.contenu}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// useEffect(() => {
//     axios.get("http://localhost:8000/notes")
//       .then(response => setNotes(response.data))
//       .catch(error => console.log(error));
//   }, []);

//   return (
//     <div className="App">
//       <h1>Mes Notes</h1>
//       <AddNoteForm setNotes={setNotes} />
//       <NoteList notes={notes} />
//     </div>
//   );
// }

// useEffect(() => {
//     fetchNotes();
//   }, []);

//   const fetchNotes = async () => {
//     const response = await axios.get('http://localhost:8000/notes');
//     setNotes(response.data);
//   };

//   const handleDelete = async (id) => {
//     await axios.post('http://localhost:8000/supprimer-note', { note_id: id });
//     fetchNotes();
//   };

//   const handleEdit = (note) => {
//     setEditingNote(note);
//   };

//   const handleCancelEdit = () => {
//     setEditingNote(null);
//   };

//   const handleSaveEdit = () => {
//     setEditingNote(null);
//     fetchNotes();
//   };

//   return (
//     <div className="App">
//       <h1>📚 Mes Notes</h1>

//       {!editingNote ? (
//         <>
//           <NoteForm onAdd={fetchNotes} />
//           <NoteList notes={notes} onDelete={handleDelete} onEdit={handleEdit} />
//         </>
//       ) : (
//         <EditNoteForm
//           noteToEdit={editingNote}
//           onSave={handleSaveEdit}
//           onCancel={handleCancelEdit}
//         />
//       )}
//     </div>
//   );
export default App;
