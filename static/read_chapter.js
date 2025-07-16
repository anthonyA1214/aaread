// ========== SETTINGS =========

htmlTag = document.documentElement;
lightModeBtn = document.getElementById('lightModeBtn');
darkModeBtn = document.getElementById('darkModeBtn');

document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlTag.setAttribute('data-bs-theme', savedTheme);
    } else {
        htmlTag.setAttribute('data-bs-theme', 'light');
    }
});

lightModeBtn.addEventListener('click', () => {
    htmlTag.setAttribute('data-bs-theme', 'light');
    localStorage.setItem('theme', 'light');
});

darkModeBtn.addEventListener('click', () => {
    htmlTag.setAttribute('data-bs-theme', 'dark');
    localStorage.setItem('theme', 'dark');
});


// ========== READER UI ==========

const uiElements = document.querySelectorAll('.reader-ui');
const body = document.getElementById('reader-body');
const offCanvasEl = document.getElementById('offcanvasRight');
let isOffCanvasOpen = false;

offCanvasEl.addEventListener('shown.bs.offcanvas', () => {
    isOffCanvasOpen = true;
});

offCanvasEl.addEventListener('hidden.bs.offcanvas', () => {
    isOffCanvasOpen = false;
});

uiElements.forEach(element => {
    element.classList.add('visible');
});

body.addEventListener('click', (e) => {
    if (isOffCanvasOpen) return

    if (e.target.closest('a') || e.target.closest('button')) return

    uiElements.forEach(element => {
        element.classList.toggle('visible');
    });
});

window.addEventListener('scroll', () => {
    const scrollTop = document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight;
    const clientHeight = document.documentElement.clientHeight

    const atTop = scrollTop === 0;
    const atBottom = scrollTop + clientHeight >= scrollHeight - 1;

    if (atTop || atBottom) {
        uiElements.forEach(element => {
            element.classList.add('visible');
        });
    } else {
        uiElements.forEach(element => {
            element.classList.remove('visible');
        });
    }
    
});



