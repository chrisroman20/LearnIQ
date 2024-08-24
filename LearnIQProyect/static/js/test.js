let questions = [];
let currentQuestion = 0;
let startTime;
let timerInterval;
let results = [];

fetch('/static/js/Preguntas.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al cargar las preguntas');
        }
        return response.json();
    })
    .then(data => {
        data.modules.forEach(module => {
            questions.push(...module.questions.map(question => ({
                ...question,
                type: module.type 
            })));
        });
    })
    .catch(error => console.error('Error al cargar las preguntas:', error));

function startQuiz() {
    const introContainer = document.getElementById('intro-container');

    // Inicia la transición
    introContainer.style.opacity = '0';
    introContainer.style.pointerEvents = 'none';  // Evita cualquier interacción

    setTimeout(() => {
        // Después de la transición, oculta el contenedor completamente
        introContainer.style.display = 'none';

        // Muestra el cuestionario
        document.getElementById('quiz-wrapper').style.display = 'block';
        loadQuestion();
        startTimer();
    }, 1000);  // Tiempo correspondiente a la duración de la transición
}

function loadQuestion() {
    if (currentQuestion < questions.length) {
        document.getElementById("question").innerText = questions[currentQuestion].text;
        document.getElementById("media-container").innerHTML = questions[currentQuestion].media || "";

        const buttonsContainer = document.getElementById("buttons-container");
        buttonsContainer.innerHTML = "";
        questions[currentQuestion].options.forEach((option, index) => {
            const button = document.createElement("button");
            button.className = "btn btn-primary btn-lg mb-2 w-100";
            button.textContent = option;
            button.onclick = () => selectAnswer(index);
            buttonsContainer.appendChild(button);
        });
    } else {
        const learningStyle = determineLearningStyle(results);
        document.getElementById("quiz-container").innerHTML = `<h2>¡Cuestionario finalizado!</h2><p>Tu estilo de aprendizaje predominante es: ${learningStyle}</p>`;
    }
}


function startTimer() {
    let timeLeft = 15;
    const timerBar = document.getElementById("timer-bar");

    timerBar.style.width = "100%";
    timerBar.style.backgroundColor = "green";
    startTime = new Date();

    clearInterval(timerInterval); 
    timerInterval = setInterval(() => {
        timeLeft--;
        const percentage = (timeLeft / 15) * 100;
        timerBar.style.width = percentage + "%";
        timerBar.style.backgroundColor = `rgb(${255 - (percentage * 2.55)}, ${percentage * 2.55}, 0)`;

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            recordResponseTime(null);
            nextQuestion();
        }
    }, 1000);
}


function selectAnswer(answerIndex) {
    clearInterval(timerInterval); 
    recordResponseTime(answerIndex);
    nextQuestion();
}

function recordResponseTime(answerIndex) {
    const responseTime = (new Date() - startTime) / 1000;
    const isCorrect = answerIndex === questions[currentQuestion].correct_option;

    results.push({
        question: questions[currentQuestion].text,
        selectedOption: answerIndex !== null ? questions[currentQuestion].options[answerIndex] : "Sin respuesta",
        correctOption: questions[currentQuestion].options[questions[currentQuestion].correct_option],
        isCorrect: isCorrect,
        responseTime: responseTime,
        type: questions[currentQuestion].type 
    });

    console.log(`Tiempo de respuesta para la pregunta ${currentQuestion + 1}: ${responseTime}s : ${isCorrect ? 'Correcto' : 'Incorrecto'}`);
}


function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < questions.length) {
        loadQuestion();
        startTimer();
    } else {
        console.log('Resultados finales:', JSON.stringify(results, null, 2)); // Imprime los resultados finales antes de mostrar el resultado
        showResult(); 
    }
}

document.getElementById('start-button').addEventListener('click', startQuiz);




function calculateTPM(responses) {
    return responses.reduce((sum, response) => sum + response.responseTime, 0) / responses.length;
}

function calculatePAM(responses) {
    const correctAnswers = responses.filter(response => response.isCorrect).length;
    return (correctAnswers / responses.length) * 100;
}
function calculateIA(PAM, TPM, weight = 1) {
    return (PAM / TPM) * weight;
}
function determineLearningStyle(results) {
    const visualResponses = results.filter(response => response.type === "visual");
    const auditoryResponses = results.filter(response => response.type === "auditivo");
    const kinestheticResponses = results.filter(response => response.type === "kinestesico");

    // Calcular los índices de afinidad para cada tipo
    const visualIA = calculateIA(calculatePAM(visualResponses), calculateTPM(visualResponses));
    const auditoryIA = calculateIA(calculatePAM(auditoryResponses), calculateTPM(auditoryResponses));
    const kinestheticIA = calculateIA(calculatePAM(kinestheticResponses), calculateTPM(kinestheticResponses));

    console.log('Visual IA:', visualIA);
    console.log('Auditory IA:', auditoryIA);
    console.log('Kinesthetic IA:', kinestheticIA);

    const maxIA = Math.max(visualIA, auditoryIA, kinestheticIA);

    if (maxIA === visualIA) return "visual";
    if (maxIA === auditoryIA) return "auditivo";
    return "kinestesico";
}

function info() {
    const learningStyle = determineLearningStyle(results);
    if (learningStyle === "visual") {
        return "Las personas con un estilo de aprendizaje visual prefieren aprender a través de imágenes, gráficos, diagramas, mapas, y cualquier otro material que se pueda ver. Tienen facilidad para recordar lo que ven más que lo que oyen.";
    } else if (learningStyle === "auditivo") {
        return "Los aprendices auditivos aprenden mejor cuando la información se presenta en forma hablada o escuchada. Prefieren las explicaciones orales y pueden recordar mejor las palabras oídas en lugar de las escritas.";
    } else {
        return "Los aprendices kinestésicos prefieren aprender haciendo. Les resulta más fácil retener información cuando están físicamente involucrados en el proceso de aprendizaje, mediante la manipulación de objetos o actividades prácticas.";
    }
}

function gif() {
    const learningStyle = determineLearningStyle(results);
    if (learningStyle === "visual") {
        return `<div class="container text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" fill="#353683" class="bi bi-eye-fill" viewBox="0 0 16 16">
                        <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0"/>
                        <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8m8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/>
                    </svg>
                </div>
                `;
    } else if (learningStyle === "auditivo") {
        return `
        <div class="container text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" fill="#be823db9" class="bi bi-ear-fill" viewBox="0 0 16 16">
                <path d="M8.5 0A5.5 5.5 0 0 0 3 5.5v7.047a3.453 3.453 0 0 0 6.687 1.212l.51-1.363a4.6 4.6 0 0 1 .67-1.197l2.008-2.581A5.34 5.34 0 0 0 8.66 0zM7 5.5v2.695q.168-.09.332-.192c.327-.208.577-.44.72-.727a.5.5 0 1 1 .895.448c-.256.513-.673.865-1.079 1.123A9 9 0 0 1 7 9.313V11.5a.5.5 0 0 1-1 0v-6a2.5 2.5 0 0 1 5 0V6a.5.5 0 0 1-1 0v-.5a1.5 1.5 0 1 0-3 0"/>
            </svg>
          </div>
        `;
    } else {
        return `
        <div class="container text-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" fill="#28a745" class="bi bi-person-arms-up" viewBox="0 0 16 16">
                <path d="M8 3a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/>
                <path d="m5.93 6.704-.846 8.451a.768.768 0 0 0 1.523.203l.81-4.865a.59.59 0 0 1 1.165 0l.81 4.865a.768.768 0 0 0 1.523-.203l-.845-8.451A1.5 1.5 0 0 1 10.5 5.5L13 2.284a.796.796 0 0 0-1.239-.998L9.634 3.84a.7.7 0 0 1-.33.235c-.23.074-.665.176-1.304.176-.64 0-1.074-.102-1.305-.176a.7.7 0 0 1-.329-.235L4.239 1.286a.796.796 0 0 0-1.24.998l2.5 3.216c.317.316.475.758.43 1.204Z"/>
            </svg>
        </div>`;
    }
}
function showResult() {
    const learningStyle = determineLearningStyle(results);

    const visualResponses = results.filter(response => response.type === "visual");
    const auditoryResponses = results.filter(response => response.type === "auditivo");
    const kinestheticResponses = results.filter(response => response.type === "kinestesico");

    // Calcular los índices de afinidad para cada tipo
    const visualIA = calculateIA(calculatePAM(visualResponses), calculateTPM(visualResponses));
    const auditoryIA = calculateIA(calculatePAM(auditoryResponses), calculateTPM(auditoryResponses));
    const kinestheticIA = calculateIA(calculatePAM(kinestheticResponses), calculateTPM(kinestheticResponses));


    const correctAnswers = results.filter(result => result.isCorrect);
    const visualScore = correctAnswers.filter(result => result.type === "visual").length;
    const auditoryScore = correctAnswers.filter(result => result.type === "auditivo").length;
    const kinestheticScore = correctAnswers.filter(result => result.type === "kinestesico").length;

    console.log('Visual Score:', visualScore);
    console.log('Auditory Score:', auditoryScore);
    console.log('Kinesthetic Score:', kinestheticScore);


    // Crear la URL con los parámetros para la solicitud del gráfico
    const url = new URL('/App/score/', window.location.origin);
    url.searchParams.append('visual', visualIA);
    url.searchParams.append('auditivo', auditoryIA);
    url.searchParams.append('kinestesico', kinestheticIA);

    const infoText = info();
    const gifText = gif();
    document.getElementById("quiz-container").innerHTML = `

<h2 class="text-center mt-2" style="color:#28a745;">Cuestionario finalizado!</h2>
<div class="container-fluid">
<div class="row">
<div class="col-md-6 text-center order-1 order-md-2 align-content-center p-3">
<img id="learning-style-graph" src="" alt="Gráfico de estilos de aprendizaje" />
</div>
<div class="col-md-6 order-2 order-md-1 text-center p-3">
<h3>Tu estilo de aprendizaje predominante es: ${learningStyle}</h3>
<p>${infoText}</p>
<div>${gifText}</div>
<a><button class="btn btn-primary btn-lg mt-2" onclick="window.location.href='/App/learning_styles/'">Más información</button></a>
</div>
</div>
</div>
    `;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el gráfico: ' + response.statusText);
            }
            return response.blob();
        })
        .then(blob => {
            const graphUrl = URL.createObjectURL(blob);
            document.getElementById('learning-style-graph').src = graphUrl;
            saveData(visualIA,auditoryIA,kinestheticIA)
        })
        .catch(error => console.error('Error al cargar el gráfico:', error));
}


function saveData(visualIA, auditoryIA, kinestheticIA) {
const csrfToken = document.querySelector('[name=csrf_token]').value;
console.log(csrfToken)
    fetch('/App/Test/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, 
        },
        body: JSON.stringify({ visualIA, auditoryIA, kinestheticIA }),
    }).then(response => {
        if (!response.ok) {
            const toastLiveExample = document.getElementById('liveToastBad');
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
            toastBootstrap.show();
            throw new Error(response);
        } else {
            const toastLiveExample = document.getElementById('liveToastGood');
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample);
            toastBootstrap.show();
            console.log(response);
        }
    }).catch(error => console.error('Error al guardar los datos:', error));
}


