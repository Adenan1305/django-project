(() => {
    const storageKey = "noodle-shop-theme";
    const savedTheme = localStorage.getItem(storageKey);

    if (savedTheme === "dark") {
        document.documentElement.classList.add("dark-mode");
    }

    function createThemeToggle() {
        let button = document.querySelector("[data-theme-toggle]");
        if (!button) {
            button = document.createElement("button");
            button.type = "button";
            button.dataset.themeToggle = "true";
            button.className = "theme-toggle";
            button.setAttribute("aria-label", "Toggle dark mode");
            button.title = "Toggle dark mode";
            document.body.appendChild(button);
        }

        button.textContent = document.documentElement.classList.contains("dark-mode") ? "☀️" : "🌙";
        button.addEventListener("click", () => {
            const isDark = document.documentElement.classList.toggle("dark-mode");
            localStorage.setItem(storageKey, isDark ? "dark" : "light");
            button.textContent = isDark ? "☀️" : "🌙";
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", createThemeToggle);
    } else {
        createThemeToggle();
    }
})();
