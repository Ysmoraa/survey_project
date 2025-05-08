// survey_app/static/survey_app/js/respond_survey.js
document.addEventListener('DOMContentLoaded', function() {
    const questions = document.querySelectorAll('.question');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const progressBar = document.getElementById('progress');
    
    let currentQuestion = 0;
    
    // Mostrar la primera pregunta
    showQuestion(currentQuestion);
    
    // Event listeners para los botones
    prevBtn.addEventListener('click', showPreviousQuestion);
    nextBtn.addEventListener('click', showNextQuestion);
    
    function showQuestion(index) {
        // Ocultar todas las preguntas
        questions.forEach(question => {
            question.style.display = 'none';
        });
        
        // Mostrar la pregunta actual
        questions[index].style.display = 'block';
        
        // Actualizar la barra de progreso
        updateProgressBar(index);
        
        // Actualizar visibilidad de los botones
        prevBtn.style.display = (index === 0) ? 'none' : 'block';
        nextBtn.style.display = (index === questions.length - 1) ? 'none' : 'block';
        submitBtn.style.display = (index === questions.length - 1) ? 'block' : 'none';
    }
    
    function showNextQuestion() {
        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            showQuestion(currentQuestion);
        }
    }
    
    function showPreviousQuestion() {
        if (currentQuestion > 0) {
            currentQuestion--;
            showQuestion(currentQuestion);
        }
    }
    
    function updateProgressBar(index) {
        const progress = ((index + 1) / questions.length) * 100;
        progressBar.style.width = `${progress}%`;
    }
});