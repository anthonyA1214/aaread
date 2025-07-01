htmlTag = document.documentElement;
themeToggle = document.getElementById("themeToggle");

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