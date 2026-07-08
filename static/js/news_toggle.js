document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-news-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.news-card');
            const newsId = card.getAttribute('data-news-id');
            const preview = card.querySelector('.news-preview');
            const full = card.querySelector('.news-full');

            if (full.style.display === 'none') {
                preview.style.display = 'none';
                full.style.display = 'block';
                this.textContent = 'Свернуть';

                // Проверяем, что newsId есть
                if (newsId) {
                    fetch(`/news/view/${newsId}/`);
                } else {
                    console.error('newsId не найден');
                }
            } else {
                preview.style.display = 'block';
                full.style.display = 'none';
                this.textContent = 'Развернуть';
            }
        });
    });
});