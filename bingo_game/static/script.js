
runGame = () => {
    document.querySelectorAll('.word-btn').forEach((element) => {
        element.onclick = (event) => {
            event.target.classList.add('active');
        };
    })

    code = ``;

    for (var min = 15; min <= 60; min++) {
        code += `<option value="${min}">${min} Minutes</option>`;
    }

    document.getElementById('timer-select').innerHTML = code;
};

document.addEventListener("DOMContentLoaded", runGame);