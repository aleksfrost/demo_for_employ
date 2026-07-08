// static/js/reactions.js

// Палитра эмодзи (20 штук, включая какашку)
const EMOJI_PALETTE = [
    '👍', '👎', '❤️', '🔥', '🥰', '😁', '😢', '😱', '🤯', '🤔',
    '🎉', '👀', '💯', '🔝', '😎', '👏', '🤝', '💔', '🍓',
];

let currentNewsId = null;

// Функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Показать палитру эмодзи
function showEmojiPalette() {
    // Удалить старую палитру если есть
    const oldPalette = document.getElementById('emoji-palette');
    if (oldPalette) oldPalette.remove();

    // Создать новую палитру
    const palette = document.createElement('div');
    palette.id = 'emoji-palette';
    palette.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        padding: 8px;
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        z-index: 10000;
        background-color: white;
    `;

    EMOJI_PALETTE.forEach(emoji => {
        const btn = document.createElement('button');
        btn.textContent = emoji;
        btn.style.cssText = `
            width: 40px;
            height: 40px;
            border: none;
            background: none;
            font-size: 24px;
            cursor: pointer;
            border-radius: 8px;
            transition: background 0.2s;
        `;
        btn.onmouseover = () => btn.style.background = '#f0f0f0';
        btn.onmouseout = () => btn.style.background = 'none';
        btn.onclick = () => sendReaction(emoji);
        palette.appendChild(btn);
    });

    document.body.appendChild(palette);

    // Закрыть при клике вне
    setTimeout(() => {
        document.addEventListener('click', function closePalette(e) {
            if (!palette.contains(e.target)) {
                palette.remove();
                document.removeEventListener('click', closePalette);
            }
        });
    }, 100);
}

// Отправить реакцию на сервер
function sendReaction(emoji) {
    fetch(`/react/${currentNewsId}/${emoji}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ action: 'add' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateReactionsDisplay(currentNewsId, data.reactions);
        }
    })
    .finally(() => {
        document.getElementById('emoji-palette')?.remove();
    });
}

// Обновить отображение реакций
function updateReactionsDisplay(newsId, reactions) {
    const card = document.querySelector(`.news-card[data-news-id="${newsId}"]`);
    if (!card) return;

    let reactionsContainer = card.querySelector('.reactions-container');
    if (!reactionsContainer) {
        reactionsContainer = document.createElement('div');
        reactionsContainer.className = 'reactions-container';
        reactionsContainer.style.cssText = `
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #f0f0f0;
        `;
        card.querySelector('.news-footer').after(reactionsContainer);
    }

    // Очистить и заполнить заново
    reactionsContainer.innerHTML = '';

    Object.entries(reactions).forEach(([emoji, count]) => {
        if (count > 0) {
            const span = document.createElement('span');
            span.style.cssText = `
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 4px 8px;
                background: #f8f9fa;
                border-radius: 20px;
                font-size: 14px;
            `;
            span.textContent = `${emoji} ${count}`;
            reactionsContainer.appendChild(span);
        }
    });
}

// Инициализация после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    // Навесить обработчики на карточки новостей
    document.querySelectorAll('.news-card').forEach(card => {
        card.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            currentNewsId = this.dataset.newsId;
            showEmojiPalette(e.pageX, e.pageY);
        });
    });
});