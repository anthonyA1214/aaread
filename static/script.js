htmlTag = document.documentElement;
themeToggle = document.getElementById("themeToggle");

const toggler = document.getElementById('sidebarCollapse');

if (toggler) {
    toggler.addEventListener('click', () => {
        document.querySelector('#sidebar').classList.toggle('collapsed');
        document.querySelector('.main').classList.toggle('expanded');
    });
};

document.addEventListener("DOMContentLoaded", () => {
    // Check for saved theme in localStorage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        htmlTag.setAttribute("data-bs-theme", savedTheme);
    } else {
        // Default to light mode if no theme is saved
        htmlTag.setAttribute("data-bs-theme", "light");
    }

    // Update the button text/icon based on the current theme
    toggleItems(htmlTag.getAttribute("data-bs-theme"));
});

themeToggle.addEventListener("click", () => {
    // Toggle between light and dark mode
    const currentTheme = htmlTag.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    
    htmlTag.setAttribute("data-bs-theme", newTheme);
    
    // Save the new theme in localStorage
    localStorage.setItem("theme", newTheme);

    // Update the button text/icon
    toggleItems(newTheme);
});

function toggleItems(theme) {
    themeToggle.innerHTML = theme === "dark" 
        ? '<i class="bi bi-sun-fill"></i>' 
        : '<i class="bi bi-moon-stars-fill"></i>';
}

const alertBoxes = document.querySelectorAll('.toast');

setTimeout(() => {
    alertBoxes.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease-in-out';
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.classList.remove('show');
            alert.style.display = 'none';
        }, 500); // Wait for the transition to finish before removing the class
    });
}, 3000); // 3 seconds