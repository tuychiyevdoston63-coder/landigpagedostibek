document.addEventListener('DOMContentLoaded', () => {
    
    // 1. LOADING SCREEN
    const loader = document.getElementById('loader');
    setTimeout(() => {
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 500);
    }, 1500);

    // 2. MOUSE TRAIL EFFECT (CURSOR GLOW)
    const glow = document.querySelector('.cursor-glow');
    document.addEventListener('mousemove', (e) => {
        glow.style.left = `${e.clientX}px`;
        glow.style.top = `${e.clientY}px`;
    });

    // 3. STICKY NAVBAR & PROGRESS BAR
    const navbar = document.querySelector('.navbar');
    const scrollBar = document.getElementById('scrollBar');

    window.addEventListener('scroll', () => {
        // Sticky class
        if (window.scrollY > 50) {
            navbar.classList.add('nav-scrolled');
        } else {
            navbar.classList.remove('nav-scrolled');
        }

        // Progress bar calc
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        scrollBar.style.width = `${scrolled}%`;
    });

    // 4. TYPING EFFECT IN HERO
    const words = ["Yaratamiz.", "Inovatsiya Qilamiz.", "Mukammallashtiramiz."];
    let i = 0;
    let timer;

    function typingEffect() {
        let word = words[i].split("");
        var loopTyping = function() {
            if (word.length > 0) {
                document.querySelector('.typing-text').innerHTML += word.shift();
            } else {
                setTimeout(deletingEffect, 2000);
                return false;
            }
            timer = setTimeout(loopTyping, 100);
        };
        loopTyping();
    }

    function deletingEffect() {
        let word = words[i].split("");
        var loopDeleting = function() {
            if (word.length > 0) {
                word.pop();
                document.querySelector('.typing-text').innerHTML = word.join("");
            } else {
                if (words.length > (i + 1)) i++;
                else i = 0;
                setTimeout(typingEffect, 500);
                return false;
            }
            timer = setTimeout(loopDeleting, 50);
        };
        loopDeleting();
    }
    typingEffect();

    // 5. SCROLL REVEAL ANIMATION
    const revealElements = document.querySelectorAll('.scroll-reveal');
    const revealOnScroll = () => {
        for (let i = 0; i < revealElements.length; i++) {
            let windowHeight = window.innerHeight;
            let elementTop = revealElements[i].getBoundingClientRect().top;
            let elementVisible = 150;

            if (elementTop < windowHeight - elementVisible) {
                revealElements[i].classList.add('revealed');
            }
        }
    };
    window.addEventListener('scroll', revealOnScroll);

    // 6. COUNTER ANIMATION
    const counters = document.querySelectorAll('.counter');
    const speed = 200;

    const startCounters = () => {
        counters.forEach(counter => {
            const animate = () => {
                const value = +counter.getAttribute('data-target');
                const data = +counter.innerText;
                const time = value / speed;
                if (data < value) {
                    counter.innerText = Math.ceil(data + time);
                    setTimeout(animate, 1);
                } else {
                    counter.innerText = value + "+";
                }
            }
            animate();
        });
    }
    // Oddiy ishlashi uchun vaqtinchalik ishga tushirish (buni Scroll Intersection Observer bilan mukammal qilish mumkin)
    setTimeout(startCounters, 2000);

    // 7. PORTFOLIO FILTER
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const filterValue = button.getAttribute('data-filter');

            portfolioItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});
