document.addEventListener('DOMContentLoaded', function() {
    // Typing effect
    const texts = [
        "Architecte de solutions digitales",
        "Expert Python & Flask",
        "Le succès vient en transformant vos idées en réalité numérique avec passion et rigueur.",
        "Créateur d'expériences mémorables",
        
    ];
    let count = 0;
    let index = 0;
    let currentText = '';
    let letter = '';
    let isDeleting = false;
    const typingElement = document.querySelector('.typing-text');

    function type() {
        if (!typingElement) return;
        if (count === texts.length) {
            count = 0;
        }
        currentText = texts[count];
        if (isDeleting) {
            letter = currentText.substring(0, index - 1);
            index--;
        } else {
            letter = currentText.substring(0, index + 1);
            index++;
        }
        typingElement.innerHTML = letter;
        if (!isDeleting && index === currentText.length) {
            isDeleting = true;
            setTimeout(type, 2000);
        } else if (isDeleting && index === 0) {
            isDeleting = false;
            count++;
            setTimeout(type, 500);
        } else {
            setTimeout(type, isDeleting ? 50 : 100);
        }
    }
    type();

    // GSAP animations
    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray('.fade-up').forEach(el => {
        gsap.from(el, {
            scrollTrigger: { trigger: el, start: 'top 80%', toggleActions: 'play none none reverse' },
            y: 50,
            opacity: 0,
            duration: 0.8,
            ease: 'power2.out'
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const progress = document.getElementById('boot-progress');
    const matrixZone = document.getElementById('matrix-rain');
    const bootLogs = document.getElementById('boot-logs');
    const codeArea = document.getElementById('code-area');
    const typewriter = document.getElementById('typewriter');
    
    let width = 0;

    // 1. Générateur de chiffres Matrix
    function generateMatrixEffect() {
        const chars = "0123456789ABCDEF!@#$%^&*";
        let text = "";
        for(let i=0; i<150; i++) {
            text += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        matrixZone.textContent = text;
    }

    const matrixInterval = setInterval(generateMatrixEffect, 50);

    // 2. Barre de progression
    const bootInterval = setInterval(() => {
        if (width >= 100) {
            clearInterval(bootInterval);
            clearInterval(matrixInterval);
            
            // Transition vers le code propre
            setTimeout(() => {
                bootLogs.style.transition = "opacity 0.5s";
                bootLogs.style.opacity = "0";
                setTimeout(() => {
                    bootLogs.style.display = 'none';
                    codeArea.style.display = 'block';
                    startTyping(); // Ta fonction d'écriture habituelle
                }, 500);
            }, 300);
        } else {
            width += Math.random() * 3;
            if(width > 100) width = 100;
            progress.style.width = width + '%';
        }
    }, 80);

    // 3. Ton code final (Python style pour Kairos)
    const codeLines = [
        "# Initialisation du moteur Kairos\n",
        "import tech_vision as tv\n\n",
        "def transform_idea(idea):\n",
        "    project = tv.create(idea)\n",
        "    project.optimize(seo=True, speed=100)\n",
        "    return project.deploy()\n\n",
        "transform_idea('Votre Projet Web');"
    ];

    let lineIdx = 0, charIdx = 0;

    function startTyping() {
        if (lineIdx < codeLines.length) {
            let line = codeLines[lineIdx];
            if (charIdx < line.length) {
                typewriter.textContent += line.charAt(charIdx);
                charIdx++;
                setTimeout(startTyping, 25);
            } else {
                lineIdx++;
                charIdx = 0;
                setTimeout(startTyping, 250);
            }
        } else {
            document.getElementById('vscode-toast').classList.add('show');
        }
    }
});