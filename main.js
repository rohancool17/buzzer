document.addEventListener('DOMContentLoaded', () => {
    const buzzer = document.getElementById('buzzer');
    const screen1 = document.getElementById('screen1');
    const screen2 = document.getElementById('screen2');

    buzzer.addEventListener('click', () => {
        // Step 1: Change buzzer color to blue
        buzzer.classList.remove('red');
        buzzer.classList.add('blue');

        // Step 2: Transition to the next screen after a short delay
        setTimeout(() => {
            screen1.classList.remove('active');
            screen2.classList.add('active');
            
            // Trigger animations on screen 2
            const fadeElements = screen2.querySelectorAll('.fade-in');
            fadeElements.forEach(el => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            });
        }, 800); // 800ms delay to feel the click
    });
});
