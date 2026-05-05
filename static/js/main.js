document.addEventListener("DOMContentLoaded", () => {
    initPageReveal();
    initButtonRipple();
    initNavbarShadow();
    //initTypingEffect();
    initSuccessAutoHide();
    initChatScroll();
    initFormLoadingStates();
    initPracticeButtons();
    initProgressAnimations();
});

/* Smooth entrance animation */
function initPageReveal() {
    const elements = document.querySelectorAll(
        ".hero-left, .device-card, .feature-card, .stat-card, .glass-panel, .recommendation-card, .chat-window, .dashboard-panel, .floating-card"
    );

    elements.forEach((el, index) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(18px)";
        el.style.transition = "0.6s ease";

        setTimeout(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }, 120 * index);
    });
}

/* Professional button click feedback */
function initButtonRipple() {
    const buttons = document.querySelectorAll("button, .primary-btn, .secondary-btn, .rec-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            this.style.transform = "scale(0.97)";
            setTimeout(() => {
                this.style.transform = "";
            }, 150);
        });
    });
}

/* Navbar shadow while scrolling */
function initNavbarShadow() {
    const navbar = document.querySelector(".navbar");
    if (!navbar) return;

    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.classList.add("navbar-active");
        } else {
            navbar.classList.remove("navbar-active");
        }
    });
}

/* AI typing effect */
//function initTypingEffect() {
    const responseText = document.querySelector(".premium-response p, .response-card p");

    if (!responseText) return;

    const originalText = responseText.innerText.trim();

    if (!originalText || originalText.length < 20) return;

    responseText.innerText = "";

    let index = 0;

    function typeText() {
        if (index < originalText.length) {
            responseText.innerText += originalText.charAt(index);
            index++;
            setTimeout(typeText, 18);
        }
    }

    typeText();
}

/* Auto hide saved messages */
function initSuccessAutoHide() {
    const messages = document.querySelectorAll(".success-message");

    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = "0";
            message.style.transform = "translateY(-8px)";
            message.style.transition = "0.5s ease";
        }, 3500);
    });
}

/* Keep chat near bottom */
function initChatScroll() {
    const chatWindow = document.querySelector(".chat-window");

    if (!chatWindow) return;

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

/* Form submit loading feedback */
function initFormLoadingStates() {
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", () => {
            const button = form.querySelector("button[type='submit'], button");

            if (!button) return;

            button.dataset.originalText = button.innerText;
            button.innerText = "Processing...";
            button.disabled = true;
            button.classList.add("loading-btn");
        });
    });
}

/* Practice button behavior */
function initPracticeButtons() {
    const buttons = document.querySelectorAll(".rec-btn");

    buttons.forEach(button => {
        button.addEventListener("click", event => {
            event.preventDefault();

            const card = button.closest(".recommendation-card");
            const title = card ? card.querySelector("h3")?.innerText : "Practice";

            showToast(`${title} started. Take a calm breath and begin.`);
        });
    });
}

/* Animate progress bars */
function initProgressAnimations() {
    const bars = document.querySelectorAll(".progress-bar div");

    bars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = "0";

        setTimeout(() => {
            bar.style.transition = "1s ease";
            bar.style.width = width;
        }, 400);
    });
}

/* Toast notification */
function showToast(message) {
    let toast = document.createElement("div");
    toast.className = "toast-message";
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 50);

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}
function initScoreMeter() {
    const card = document.querySelector(".score-meter-card");
    if (!card) return;

    const targetScore = parseInt(card.dataset.score || "0");
    const circle = card.querySelector(".score-progress");
    const number = document.getElementById("scoreValue");

    const radius = 68;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = circumference;

    setTimeout(() => {
        const offset = circumference - (targetScore / 100) * circumference;
        circle.style.strokeDashoffset = offset;
    }, 300);

    let current = 0;
    const speed = 18;

    const counter = setInterval(() => {
        if (current >= targetScore) {
            clearInterval(counter);
        } else {
            current++;
            number.innerText = current;
        }
    }, speed);
}

document.addEventListener("DOMContentLoaded", initScoreMeter);
function initPractice() {
    const startBtn = document.getElementById("startPracticeBtn");
    const stopBtn = document.getElementById("stopPracticeBtn");
    const container = document.getElementById("practiceContainer");

    const stepText = document.getElementById("practiceStep");
    const timerText = document.getElementById("practiceTimer");
    const circle = document.querySelector(".breathing-circle");

    if (!startBtn) return;

    let interval;

    startBtn.addEventListener("click", () => {
        container.style.display = "block";
        let phase = 0;

        const phases = [
            { text: "Inhale", time: 4 },
            { text: "Hold", time: 4 },
            { text: "Exhale", time: 6 }
        ];

        function runPhase() {
            const current = phases[phase];
            let timeLeft = current.time;

            stepText.innerText = current.text;

            if (current.text === "Inhale") {
                circle.classList.add("expand");
            } else {
                circle.classList.remove("expand");
            }

            timerText.innerText = `${timeLeft}s`;

            interval = setInterval(() => {
                timeLeft--;
                timerText.innerText = `${timeLeft}s`;

                if (timeLeft <= 0) {
                    clearInterval(interval);
                    phase = (phase + 1) % phases.length;
                    runPhase();
                }
            }, 1000);
        }

        runPhase();
    });

    stopBtn.addEventListener("click", () => {
        clearInterval(interval);
        container.style.display = "none";
    });
}

document.addEventListener("DOMContentLoaded", initPractice);