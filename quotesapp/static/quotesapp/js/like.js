(function() {
  const likeBtn = document.getElementById('like-btn');
  const dislikeBtn = document.getElementById('dislike-btn');
  if (!likeBtn || !dislikeBtn) return;

  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  function send(action, id) {
    axios.post(`/like/${id}/`, new URLSearchParams({action}), {
      headers: {'X-CSRFToken': csrftoken}
    }).then(r => {
      const data = r.data;
      document.getElementById('like-count').textContent = data.likes;
      document.getElementById('dislike-count').textContent = data.dislikes;
      const ratingEl = document.getElementById('rating');
      if (ratingEl) ratingEl.textContent = data.rating;
    }).catch(() => {
      // опционально можно показать сообщение
    });
  }

  likeBtn.addEventListener('click', () => send('like', likeBtn.dataset.id));
  dislikeBtn.addEventListener('click', () => send('dislike', dislikeBtn.dataset.id));
})();