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
        // Extraer preguntas de todos los módulos
        data.modules.forEach(module => {
            questions.push(...module.questions.map(question => ({
                ...question,
                type: module.type // Añadir el tipo de módulo a cada pregunta
            })));
        });
        console.log('Preguntas cargadas:', questions); // Para verificar que las preguntas se cargaron correctamente
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

    clearInterval(timerInterval); // Asegúrate de detener cualquier temporizador anterior
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
    clearInterval(timerInterval); // Detén el temporizador inmediatamente
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
        type: questions[currentQuestion].type // Asegúrate de que el tipo está incluido
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
        showResult(); // Mostrar el resultado y el gráfico al finalizar
    }
}




// Asignar el evento de clic al botón de comenzar
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
    // Filtrar las respuestas por tipo de módulo
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

    // Determinar el estilo de aprendizaje predominante
    const maxIA = Math.max(visualIA, auditoryIA, kinestheticIA);

    if (maxIA === visualIA) return "visual";
    if (maxIA === auditoryIA) return "auditivo";
    return "kinestesico";
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
    // Calcular el puntaje para cada tipo basándote solo en las respuestas correctas
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

    // Mostrar el mensaje de resultado y el gráfico
    document.getElementById("quiz-container").innerHTML = `
        <h2>¡Cuestionario finalizado!</h2>
        <p>Tu estilo de aprendizaje predominante es: ${learningStyle}</p>
        <img id="learning-style-graph" src="" alt="Gráfico de estilos de aprendizaje" />
    `;

    // Solicitar el gráfico al servidor
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
        })
        .catch(error => console.error('Error al cargar el gráfico:', error));
}
