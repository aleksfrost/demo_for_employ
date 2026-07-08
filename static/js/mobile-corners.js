(function() {
    function initMobileCorners() {
        const newsBlock = document.querySelector('.center-column');
        const analyticsBlock = document.querySelector('.analytics-panel');
        const headlinesBlock = document.querySelector('.side-column');

        let leftCorner = document.querySelector('.corner-left');
        let rightCorner = document.querySelector('.corner-right');

        if (!leftCorner || !rightCorner) {
            setTimeout(initMobileCorners, 100);
            return;
        }

        function resetToNews() {
            newsBlock.classList.add('active-panel');
            analyticsBlock.classList.remove('active-panel');
            headlinesBlock.classList.remove('active-panel');

            leftCorner.style.display = 'flex';
            rightCorner.style.display = 'flex';
            leftCorner.textContent = 'Аналитика';
            rightCorner.textContent = 'Коротко';
            leftCorner.setAttribute('data-panel', 'analytics');
            rightCorner.setAttribute('data-panel', 'headlines');
        }

        function showAnalytics() {
            newsBlock.classList.remove('active-panel');
            analyticsBlock.classList.add('active-panel');
            headlinesBlock.classList.remove('active-panel');

            leftCorner.style.display = 'none';
            rightCorner.style.display = 'flex';
            rightCorner.textContent = 'Главная';
            rightCorner.setAttribute('data-panel', 'news');
        }

        function showHeadlines() {
            newsBlock.classList.remove('active-panel');
            analyticsBlock.classList.remove('active-panel');
            headlinesBlock.classList.add('active-panel');

            rightCorner.style.display = 'none';
            leftCorner.style.display = 'flex';
            leftCorner.textContent = 'Главная';
            leftCorner.setAttribute('data-panel', 'news');
        }

        const newLeft = leftCorner.cloneNode(true);
        const newRight = rightCorner.cloneNode(true);
        leftCorner.parentNode.replaceChild(newLeft, leftCorner);
        rightCorner.parentNode.replaceChild(newRight, rightCorner);
        leftCorner = newLeft;
        rightCorner = newRight;

        leftCorner.onclick = () => {
            const target = leftCorner.getAttribute('data-panel');
            if (target === 'analytics') showAnalytics();
            else if (target === 'news') resetToNews();
        };

        rightCorner.onclick = () => {
            const target = rightCorner.getAttribute('data-panel');
            if (target === 'headlines') showHeadlines();
            else if (target === 'news') resetToNews();
        };

        resetToNews();
    }

    document.addEventListener('DOMContentLoaded', initMobileCorners);
    window.addEventListener('pageshow', initMobileCorners);
})();