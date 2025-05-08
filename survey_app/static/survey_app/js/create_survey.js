document.addEventListener('DOMContentLoaded', function() {
    const questionsList = document.getElementById('questionsList');
    const addQuestionBtn = document.getElementById('addQuestionBtn');

    let newQuestionCounter = 0;

    function setupQuestionEvents(questionElement) {
        const typeSelect = questionElement.querySelector('.question-type-select');
        const removeBtn = questionElement.querySelector('.remove-question-btn');
        const currentType = questionElement.dataset.questionType;

        if (typeSelect) {
            typeSelect.addEventListener('change', function() {
                updateQuestionDetails(this);
            });

            if (currentType) {
                updateQuestionDetails(typeSelect, true);  // true para mantener opciones existentes
            }
        }

        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                if (confirm('¿Eliminar esta pregunta?')) {
                    questionElement.remove();
                }
            });
        }
    }

    function updateQuestionDetails(selectElement, preserveOptions = false) {
        const questionDiv = selectElement.closest('.question-item');
        const detailsDiv = questionDiv.querySelector('.tipo-detalle');
        const questionId = questionDiv.dataset.questionId;
        const questionType = selectElement.value;

        detailsDiv.innerHTML = '';

        if (questionType === 'multiple') {
            const optionsContainer = document.createElement('div');
            optionsContainer.classList.add('options-container');
            optionsContainer.innerHTML = `
                <p class="font-weight-bold">Opciones de respuesta *</p>
                <div class="option-inputs"></div>
                <button type="button" class="btn btn-sm btn-outline-primary add-option-btn">
                    <i class="fas fa-plus"></i> Añadir otra opción
                </button>
            `;

            const optionInputs = optionsContainer.querySelector('.option-inputs');

            // Si se está editando y hay opciones ya cargadas
            if (preserveOptions) {
                const existingInputs = questionDiv.querySelectorAll('.option-group input');
                existingInputs.forEach((input, index) => {
                    const optionGroup = document.createElement('div');
                    optionGroup.className = 'input-group mb-2 option-group';
                    optionGroup.innerHTML = `
                        <input type="text" name="option_${questionId}_${index}" class="form-control" value="${input.value}" required>
                        <div class="input-group-append">
                            <button type="button" class="btn btn-outline-danger remove-option-btn" ${index < 2 ? 'disabled' : ''}>
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                    optionInputs.appendChild(optionGroup);
                    setupRemoveOption(optionGroup);
                });
            } else {
                // Si es nueva pregunta, agrega dos opciones por defecto
                for (let i = 0; i < 2; i++) {
                    const optionGroup = document.createElement('div');
                    optionGroup.className = 'input-group mb-2 option-group';
                    optionGroup.innerHTML = `
                        <input type="text" name="option_${questionId}_${i}" class="form-control" placeholder="Opción ${i + 1}" required>
                        <div class="input-group-append">
                            <button type="button" class="btn btn-outline-danger remove-option-btn" disabled>
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                    optionInputs.appendChild(optionGroup);
                }
            }

            optionsContainer.querySelector('.add-option-btn').addEventListener('click', function() {
                addOption(optionInputs, questionId);
            });

            detailsDiv.appendChild(optionsContainer);
        }
    }

    function addOption(container, questionId) {
        const index = container.querySelectorAll('.option-group').length;
        const optionGroup = document.createElement('div');
        optionGroup.className = 'input-group mb-2 option-group';
        optionGroup.innerHTML = `
            <input type="text" name="option_${questionId}_${index}" class="form-control" placeholder="Opción ${index + 1}" required>
            <div class="input-group-append">
                <button type="button" class="btn btn-outline-danger remove-option-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        container.appendChild(optionGroup);
        setupRemoveOption(optionGroup);
    }

    function setupRemoveOption(optionGroup) {
        const removeBtn = optionGroup.querySelector('.remove-option-btn');
        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                optionGroup.remove();
            });
        }
    }

    function addNewQuestion() {
        newQuestionCounter++;
        const questionId = 'new_' + newQuestionCounter;

        const html = `
            <div class="question-item card mb-3" data-question-id="${questionId}">
                <div class="card-body">
                    <div class="form-group">
                        <label class="font-weight-bold">Texto de la pregunta *</label>
                        <input type="text" name="question_text_${questionId}"
                               class="form-control" placeholder="¿Cuál es tu opinión sobre...?" required>
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold">Tipo de pregunta *</label>
                        <select name="question_type_${questionId}" class="form-control question-type-select">
                            <option value="">-- Selecciona un tipo --</option>
                            <option value="text">Texto Libre</option>
                            <option value="multiple">Opción Múltiple</option>
                            <option value="escala">Escala de Valoración (1-5)</option>
                        </select>
                    </div>
                    <div class="tipo-detalle"></div>
                    <div class="text-right mt-3">
                        <button type="button" class="btn btn-danger btn-sm remove-question-btn">
                            <i class="fas fa-trash-alt"></i> Eliminar Pregunta
                        </button>
                    </div>
                </div>
            </div>
        `;

        questionsList.insertAdjacentHTML('beforeend', html);
        setupQuestionEvents(questionsList.lastElementChild);
    }

    // Eventos iniciales
    document.querySelectorAll('.question-item').forEach(setupQuestionEvents);
    addQuestionBtn.addEventListener('click', addNewQuestion);
});

