(function() {
  const likeBtn = document.getElementById('like-btn');
  const dislikeBtn = document.getElementById('dislike-btn');
  if (!likeBtn || !dislikeBtn) return;

  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  function send(action, id) {
    console.log(`Sending ${action} for quote ID: ${id}`);
    fetch(`/like/${id}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: new URLSearchParams({ action }).toString()
    })
    .then(async (r) => {
      if (!r.ok) {
        const text = await r.text().catch(() => '');
        throw new Error(`HTTP ${r.status} ${text}`);
      }
      return r.json();
    })
    .then((data) => {
      console.log('Response:', data);
      document.getElementById('like-count').textContent = data.likes;
      document.getElementById('dislike-count').textContent = data.dislikes;
      const ratingEl = document.getElementById('rating');
      if (ratingEl) ratingEl.textContent = data.rating;
    })
    .catch((err) => {
      console.error('Error:', err);
      alert('Произошла ошибка. Попробуйте снова.');
    });
  }

  likeBtn.addEventListener('click', () => send('like', likeBtn.dataset.id));
  dislikeBtn.addEventListener('click', () => send('dislike', dislikeBtn.dataset.id));
})();