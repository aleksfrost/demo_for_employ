document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.ticker-container');
    const content = document.querySelector('.ticker-content');
    if (!container || !content) return;

    // Проверяем, есть ли вообще текст в бегущей строке
    const originalHtml = content.innerHTML.trim();
    if (!originalHtml) return;  // если строка пустая — выходим

    function ensureWidth() {
        const originalHtml = content.innerHTML.trim();
        if (!originalHtml) return; // если строка пустая — выходим

        const containerWidth = container.clientWidth;
        let currentWidth = content.scrollWidth;
        let newHtml = originalHtml;
        let copies = 1;
        const maxCopies = 10;  // защита от бесконечного цикла

        // Сбрасываем содержимое до оригинала
        content.innerHTML = originalHtml;

        while (currentWidth < containerWidth * 2 && copies < maxCopies) {
            newHtml += originalHtml;
            content.innerHTML = newHtml;
            currentWidth = content.scrollWidth;
            copies++;
        }
    }

    ensureWidth();
    window.addEventListener('resize', ensureWidth);
});