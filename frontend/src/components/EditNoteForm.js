import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EditNoteForm = ({ noteToEdit, onSave, onCancel }) => {
  const [titre, setTitre] = useState('');
  const [contenu, setContenu] = useState('');

  useEffect(() => {
    if (noteToEdit) {
      setTitre(noteToEdit.titre);
      setContenu(noteToEdit.contenu);
    }
  }, [noteToEdit]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/modifier-note', {
        note_id: noteToEdit.id,
        titre,
        contenu
      });
      onSave();  // Pour rafraîchir la liste ou revenir à la vue liste
    } catch (error) {
      console.error("Erreur lors de la mise à jour :", error);
    }
  };

  if (!noteToEdit) return null;

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: "20px", background: "#f1f1f1", padding: "15px", borderRadius: "8px" }}>
      <h3>✏️ Modifier la note</h3>
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
        required
        rows="5"
      />
      <br />
      <button type="submit">💾 Enregistrer</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: "10px" }}>❌ Annuler</button>
    </form>
  );
};

export default EditNoteForm;
