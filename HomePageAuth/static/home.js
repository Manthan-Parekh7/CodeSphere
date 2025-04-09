const codeSamples = [
    `print('Hello, World!')\nfor i in range(5):\n    print(i)\nprint('Done!')\nprint('Python is fun!')`,
    `def add(a, b):\n    result = a + b\n    return result\nprint(add(2, 3))\nprint('Addition complete!')`,
    `for i in range(5):\n    print(i)\nprint('Loop finished')\nprint('Goodbye!')\nprint('End of script!')`,
    `print('Hello, World!')\nfor i in range(5):\n    print(i)\nprint('Python is fun!')`,
    `console.log('Hello, JavaScript!');\nconsole.log('JavaScript is fun!');`,
];

let index = 0;
let isErasing = false;

function typeCode() {
    let codeBlock = document.getElementById("codeDisplay");
    let code = codeSamples[index];
    let i = 0;

    codeBlock.innerHTML = "";
    isErasing = false;

    function type() {
        if (i < code.length) {
            codeBlock.innerHTML = code.substring(0, i + 1);
            i++;
            setTimeout(type, 50);
        } else {
            setTimeout(() => {
                isErasing = true;
                erase();
            }, 2000);
        }
    }

    function erase() {
        if (isErasing && codeBlock.innerHTML.length > 0) {
            codeBlock.innerHTML = codeBlock.innerHTML.slice(0, -1);
            setTimeout(erase, 25);
        } else {
            isErasing = false;
            index = (index + 1) % codeSamples.length;
            setTimeout(typeCode, 500);
        }
    }

    type();
}

document.addEventListener("DOMContentLoaded", typeCode);

// Mobile menu toggle with smooth transition
document.getElementById("menuToggle").addEventListener("click", () => {
    const menu = document.getElementById("mobileMenu");
    menu.classList.toggle("hidden");

    // Apply smooth animation
    setTimeout(() => {
        menu.classList.toggle("active");
    }, 10);
});

// Dark mode toggle
function toggleTheme() {
    const body = document.body;
    const currentTheme = localStorage.getItem("theme") || "light";
    const newTheme = currentTheme === "light" ? "dark" : "light";

    body.classList.toggle("dark", newTheme === "dark");
    localStorage.setItem("theme", newTheme);
    document.getElementById("themeToggle").textContent = newTheme === "dark" ? "☀️" : "🌙";
}

document.addEventListener("DOMContentLoaded", () => {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
        document.getElementById("themeToggle").textContent = "☀️";
    }
});