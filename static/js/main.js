// ====== Theme Toggle ======
function getTheme() {
    return localStorage.getItem('theme') || 'auto';
}

function applyTheme(theme) {
    var body = document.body;
    var btn = document.querySelector('.theme-toggle');
    body.classList.remove('dark-mode', 'light-mode');

    if (theme === 'dark') {
        body.classList.add('dark-mode');
        if (btn) btn.textContent = '☀️';
    } else if (theme === 'light') {
        body.classList.add('light-mode');
        if (btn) btn.textContent = '🌙';
    } else {
        // auto: follow system, show icon for manual switch
        if (btn) btn.textContent = '🌙';
    }
}

function toggleTheme() {
    var current = getTheme();
    var next;
    if (current === 'auto') {
        // Check system preference
        var isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        next = isDark ? 'light' : 'dark';
    } else if (current === 'dark') {
        next = 'light';
    } else {
        next = 'dark';
    }
    localStorage.setItem('theme', next);
    applyTheme(next);
}

// ====== Init ======
document.addEventListener('DOMContentLoaded', function () {
    // Apply saved theme
    applyTheme(getTheme());

    // Mobile nav toggle
    var toggle = document.querySelector('.nav-toggle');
    var links = document.querySelector('.nav-links');

    if (toggle && links) {
        toggle.addEventListener('click', function () {
            links.classList.toggle('open');
        });
    }
});
