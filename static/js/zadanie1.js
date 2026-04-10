let questions = [];
let currentQuestion = 0;
let errorsCount = 0;
const errorsList = [];
const wrongQuestions = [];
const form = document.getElementById("quizForm");
const questionText = document.getElementById("questionText");
const optionsDiv = document.getElementById("options");
const result = document.getElementById("result");

fetch("/api/questions")
    .then(response => response.json())
    .then(data => {
        questions = data;
        loadQuestion(currentQuestion);
    })
    .catch(error => console.error("Ошибка:", error));

function loadQuestion(index) {
    result.textContent = "";
    questionText.textContent = `${index+1}/${questions.length}: ${questions[index].question}`;
    optionsDiv.innerHTML = "";
    questions[index].options.forEach((option, i) => {
        const input = document.createElement("input");
        input.type = "radio";
        input.id = "option" + i;
        input.name = "answer";
        input.value = i;
        if (i === 0) input.required = true;
        const label = document.createElement("label");
        label.htmlFor = "option" + i;
        label.textContent = option;
        optionsDiv.appendChild(input);
        optionsDiv.appendChild(label);
        optionsDiv.appendChild(document.createElement("br"));
    });
}

form.addEventListener("submit", event => {
    event.preventDefault();
    const selectedOptionIndex = parseInt(form.answer.value);
    if (selectedOptionIndex !== questions[currentQuestion].correct) {
        errorsCount++;
        errorsList.push(currentQuestion + 1);
        wrongQuestions.push(questions[currentQuestion].question);
    }
    currentQuestion++;
    if (currentQuestion >= questions.length) {
        displayResult();
    } else {
        loadQuestion(currentQuestion);
    }
});

function displayResult() {
    let message = "";
    const score = 10 - errorsCount;
    const topicsErrors = {};
    errorsList.forEach(qIndex => {
        const topic = questions[qIndex - 1].topic;
        topicsErrors[topic] = (topicsErrors[topic] || 0) + 1;
    });
    if (errorsCount > 0) {
        message += `<p style='color: red; font-size: large; text-align: center;'>Тест завершен!</p>`;
        message += `<p style='color: red; font-size: large; text-align: center;'>Количество ошибок: ${errorsCount}.</p>`;
        message += `<p style='color: red; font-size: large; text-align: center;'>Баллы: ${score} из 10.</p>`;
        message += `<p style='color: red; text-align: center; text-decoration: underline;'>Обратите внимание на следующие тематические разделы!</p>`;
        let counter = 1;
        for (const [topic] of Object.entries(topicsErrors)) {
            message += `<p style='color: black; font-size: large; text-align: center;'>${counter++}) ${topic}</p>`;
        }
        message += `<p style='color: red; font-size: large; text-align: center; text-decoration: underline;'>Повторите данные разделы и попробуйте пройти тест снова!</p>`;
        message += `<p style='text-align: center; margin-top: 20px;'>`;
        message += `<button onclick=\'location.reload()\' style='padding: 10px 20px; font-size: large;'>Пройти снова</button>`;
        message += `</p>`;
    } else {
        message += `<p style='color: green; font-size: large; text-align: center;'>Тест завершен без ошибок!</p>`;
        message += `<p style='color: green; font-size: large; text-align: center;'>Баллы: 10 из 10.</p>`;
        message += `<p style='color: green; font-size: large; text-align: center;'>Можно переходить к следующему заданию.</p>`;
    }
    result.innerHTML = message;
    form.style.display = "none";
}