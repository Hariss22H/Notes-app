document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const id = btn.dataset.id;
      if (!confirm('Delete this note?')) return;
      const resp = await fetch(`/api/note/${id}`, { method: 'DELETE' });
      if (resp.ok) {
        const el = document.getElementById(`note-${id}`);
        if (el) el.remove();
        else window.location.reload();
      } else {
        alert('Could not delete note');
      }
    });
  });
});
