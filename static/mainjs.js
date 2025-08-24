 import confetti from 'https://cdn.skypack.dev/canvas-confetti';

// Allow Enter key to jump between inputs
document.addEventListener("DOMContentLoaded", function() {
    var inputs = document.querySelectorAll("input");

    inputs.forEach(function(input, index) {
        input.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
            }
        });
    });
});

let result;
const submit = document.getElementById("calculate-btn");

// ✅ Corrected FLAMES logic
submit.addEventListener("click", function calculate() {
    let king_name = document.getElementById("king-name").value.toLowerCase().replace(/\s+/g, "");
    let queen_name = document.getElementById("queens-name").value.toLowerCase().replace(/\s+/g, "");

    // Turn names into arrays
    let kingArr = king_name.split("");
    let queenArr = queen_name.split("");

    // Cancel out common characters properly
    for (let i = 0; i < kingArr.length; i++) {
        let index = queenArr.indexOf(kingArr[i]);
        if (index !== -1) {
            kingArr.splice(i, 1);
            queenArr.splice(index, 1);
            i--; // step back after splice
        }
    }

    let count = kingArr.length + queenArr.length;

    let flames = ["Friends", "Love", "Affection", "Marriage", "Enemies", "Siblings"];
    let index = 0;

    // Rotate and remove until one left
    while (flames.length > 1) {
        index = (index + count - 1) % flames.length;
        flames.splice(index, 1);
    }

    result = flames[0];
});

// Render the result with animation
submit.addEventListener("click", function render() {
    var king_name = document.getElementById("king-name").value;
    var queen_name = document.getElementById("queens-name").value;
    let text_area = document.getElementById("text_area");

    text_area.innerHTML = " ";
    text_area.innerHTML = '<img data-src="/static/images/heart.png" id="heart" loading="lazy" />';

    let img = document.querySelector('img[data-src]');

    if ('IntersectionObserver' in window) {
        let observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let img = entry.target;
                    img.src = img.dataset.src;
                    observer.unobserve(img);
                }
            });
        });

        observer.observe(img);
    } else {
        img.src = img.dataset.src;
    }

    // Use setTimeout instead of setInterval (fires once after 3.5s)
    setTimeout(function () {
        text_area.innerHTML = " ";
        text_area.innerHTML = `<p class="rendered_king_name">${king_name}</p>`;
        text_area.innerHTML += '<p class="rendered_para">and</p>';
        text_area.innerHTML += `<p class="rendered_queen_name">${queen_name}</p>`;
        text_area.innerHTML += '<p class="rendered_para">will be</p>';
        text_area.innerHTML += `<p class="rendered_result">${result}</p>`;
        text_area.innerHTML += '<p class="rendered_para">Forever</p>';
        confetti();
        text_area.innerHTML += '<button id="retry-btn">Try Again</button>';
        document.getElementById('retry-btn').addEventListener('click', function retry() {
            location.href = location.href;
        });
    }, 3500);
});
