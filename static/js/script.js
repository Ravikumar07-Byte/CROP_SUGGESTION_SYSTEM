document.addEventListener('DOMContentLoaded', () => {
    // Page transition logic
    const homePage = document.getElementById('home-page');
    const optionsPage = document.getElementById('options-page');
    const cropSuggestionPage = document.getElementById('crop-suggestion-page');
    const startBtn = document.getElementById('start-btn');
    const cropSuggestionOption = document.getElementById('crop-suggestion-option');
    // backToOptionsBtn and backToHomeBtn are handled by inline onclick in index.html,
    // but their functionality is provided by the global showPage function.

    // Function to show a page and hide others
    // This function is also defined globally in index.html for onclick attributes
    window.showPage = function(pageToShow) {
        [homePage, optionsPage, cropSuggestionPage].forEach(page => {
            if (page) { // Check if page element exists
                page.classList.remove('active');
            }
        });
        if (pageToShow) {
            pageToShow.classList.add('active');
        }
    };

    // Initial page load
    showPage(homePage);

    // Event listeners for page navigation (using IDs)
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            showPage(optionsPage);
        });
    }

    if (cropSuggestionOption) {
        cropSuggestionOption.addEventListener('click', () => {
            showPage(cropSuggestionPage);
        });
    }

    // Background animation elements
    const leafContainer = document.getElementById('leaf-container');
    const grainContainer = document.getElementById('grain-container');

    function createFallingElements(container, type, count, iconClass = '') {
        if (!container) return; // Ensure container exists

        for (let i = 0; i < count; i++) {
            const element = document.createElement('div');
            element.classList.add(type);
            if (iconClass) {
                element.innerHTML = `<i class="${iconClass}"></i>`;
            }
            element.style.left = `${Math.random() * 100}vw`;
            element.style.animationDuration = `${Math.random() * 5 + 5}s`; // 5-10 seconds
            element.style.animationDelay = `${Math.random() * 5}s`;
            element.style.opacity = `${Math.random() * 0.4 + 0.1}`; // 0.1-0.5
            container.appendChild(element);
        }
    }

    createFallingElements(leafContainer, 'leaf', 15, 'fas fa-leaf');
    createFallingElements(grainContainer, 'grain', 20);
});
