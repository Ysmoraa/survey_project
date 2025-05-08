document.addEventListener('DOMContentLoaded', function() {
    const chartContainers = document.querySelectorAll('.chart-container canvas');
    
    chartContainers.forEach(canvas => {
        const questionType = canvas.dataset.questionType;
        const { labels, data } = getChartData(canvas, questionType);
        
        renderPieChart(canvas, labels, data);
    });
});

function getChartData(canvas, questionType) {
    let labels = [];
    let data = [];

    if (questionType === 'text') {
        const answers = canvas.dataset.answers.split('|||').filter(Boolean);
        const answerCounts = {};
        
        answers.forEach(answer => {
            const key = answer.toLowerCase().trim();
            answerCounts[key] = (answerCounts[key] || 0) + 1;
        });
        
        labels = Object.keys(answerCounts);
        data = Object.values(answerCounts);
        
    } else if (questionType === 'multiple') {
        const options = canvas.dataset.options.split('|||').filter(Boolean);
        
        options.forEach(optionStr => {
            const [text, count] = optionStr.split(':::');
            labels.push(text);
            data.push(parseInt(count));
        });
        
    } else if (questionType === 'escala') {
        const ratings = canvas.dataset.ratings.split('|||').filter(Boolean);
        
        ratings.forEach(ratingStr => {
            const [value, count] = ratingStr.split(':::');
            labels.push(`${value} estrellas`);
            data.push(parseInt(count));
        });
    }

    return { labels, data };
}

function renderPieChart(canvas, labels, data) {
    const backgroundColors = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#5a5c69', '#858796', '#3a3b45'
    ].slice(0, data.length);

    new Chart(canvas.getContext('2d'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribución de respuestas',
                    font: { size: 16 }
                },
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        boxWidth: 12
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((context.raw / total) * 100);
                            return `${context.label}: ${context.raw} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}