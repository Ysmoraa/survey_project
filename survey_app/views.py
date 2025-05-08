from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey, Question, Option, Response, Answer
from .forms import SurveyForm, QuestionForm, OptionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def survey_list(request):
    if request.user.is_staff:
        # Staff ve todas sus encuestas (publicadas y borradores)
        surveys = Survey.objects.filter(created_by=request.user)
    else:
        # Usuarios normales solo ven encuestas publicadas
        surveys = Survey.objects.filter(is_published=True)
    return render(request, 'survey_app/survey_list.html', {'surveys': surveys})

@staff_member_required
def create_survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Crear encuesta sin preguntas iniciales
            survey = form.save(commit=False)
            survey.created_by = request.user
            survey.is_published = False
            survey.save()
            
            # Redirigir a edición con el ID correcto
            return redirect('edit_survey', survey_id=survey.id)
        else:
            # Si el formulario no es válido, mostrar errores
            messages.error(request, "Corrige los errores en el formulario")
    else:
        form = SurveyForm()
    
    return render(request, 'survey_app/create_survey.html', {
        'form': form,
        'edit_mode': False  # Importante para ocultar elementos
    })

@staff_member_required
def publish_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, created_by=request.user)
    survey.is_published = True
    survey.save()
    return redirect('survey_list')

@staff_member_required
def unpublish_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, created_by=request.user)
    survey.is_published = False
    survey.save()
    return redirect('survey_list')

@staff_member_required
def edit_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, created_by=request.user)
    
    if request.method == 'POST':
        try:
            # 1. Actualizar información básica
            survey.title = request.POST.get('title')
            survey.description = request.POST.get('description')
            
            # 2. Manejar estado de publicación
            if 'publish' in request.POST:
                survey.is_published = True
                msg = "Encuesta publicada correctamente"
            else:
                survey.is_published = False
                msg = "Borrador guardado correctamente"
            
            survey.save()
            
            # 3. Procesar preguntas y opciones
            processed_questions = []
            
            # === PREGUNTAS EXISTENTES ===
            for question in survey.questions.all():
                question_text = request.POST.get(f'question_text_{question.id}')
                question_type = request.POST.get(f'question_type_{question.id}')
                
                if question_text and question_text.strip():
                    question.text = question_text.strip()
                    question.question_type = question_type
                    question.save()
                    processed_questions.append(question.id)
                    
                    # === OPCIONES EXISTENTES ===
                    if question_type == 'multiple':
                        existing_option_ids = []
                        option_index = 0
                        
                        while True:
                            option_key = f'option_{question.id}_{option_index}'
                            option_text = request.POST.get(option_key)
                            
                            if option_text is None:
                                break
                            
                            option_text = option_text.strip()
                            if option_text:
                                try:
                                    option = question.options.all()[option_index]
                                    option.text = option_text
                                    option.save()
                                except IndexError:
                                    option = Option.objects.create(
                                        question=question,
                                        text=option_text
                                    )
                                existing_option_ids.append(option.id)
                            
                            option_index += 1
                        
                        # Eliminar opciones que ya no están
                        question.options.exclude(id__in=existing_option_ids).delete()
            
            # === NUEVAS PREGUNTAS ===
            new_questions = [key for key in request.POST if key.startswith('question_text_new_')]
            for key in new_questions:
                q_id = key.replace('question_text_new_', '')
                question_text = request.POST.get(key).strip()
                question_type = request.POST.get(f'question_type_new_{q_id}')
                
                if question_text:
                    question = Question.objects.create(
                        survey=survey,
                        text=question_text,
                        question_type=question_type
                    )
                    processed_questions.append(question.id)
                    
                    # === NUEVAS OPCIONES ===
                    if question_type == 'multiple':
                        option_index = 0
                        while True:
                            option_key = f'option_new_{q_id}_{option_index}'
                            option_text = request.POST.get(option_key)
                            
                            if option_text is None:
                                break
                            
                            option_text = option_text.strip()
                            if option_text:
                                Option.objects.create(
                                    question=question,
                                    text=option_text
                                )
                            option_index += 1
            
            # === ELIMINAR PREGUNTAS NO PROCESADAS ===
            survey.questions.exclude(id__in=processed_questions).delete()
            
            messages.success(request, msg)
            return redirect('edit_survey', survey_id=survey.id)
        
        except Exception as e:
            messages.error(request, f"Error al guardar: {str(e)}")
            return redirect('edit_survey', survey_id=survey.id)
    
    return render(request, 'survey_app/create_survey.html', {
        'survey': survey,
        'edit_mode': True
    })


@login_required
def respond_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, is_published=True)
    
    if request.method == 'POST':
        response = Response.objects.create(survey=survey, respondent=request.user if request.user.is_authenticated else None)
        
        for question in survey.questions.all():
            answer_value = request.POST.get(f'question_{question.id}')
            
            if question.question_type == 'text':
                Answer.objects.create(
                    response=response,
                    question=question,
                    text_answer=answer_value
                )
            elif question.question_type == 'multiple':
                option = Option.objects.get(id=answer_value)
                Answer.objects.create(
                    response=response,
                    question=question,
                    option_answer=option
                )
            elif question.question_type == 'escala':
                Answer.objects.create(
                    response=response,
                    question=question,
                    rating_answer=answer_value
                )
        
        return render(request, 'survey_app/respond_survey.html', {
            'survey': survey,
            'thank_you': True
        })
    
    return render(request, 'survey_app/respond_survey.html', {'survey': survey})

@login_required
def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    
    if not (request.user.is_staff or request.user == survey.created_by):
        return HttpResponseForbidden("No tienes permiso para ver estos resultados")
    
    total_responses = Response.objects.filter(survey=survey).count()
    
    questions = []
    for question in survey.questions.all():
        question_data = {
            'id': question.id,
            'text': question.text,
            'question_type': question.question_type,
            'text_answers': [],
            'options': [],
            'rating_distribution': []
        }
        
        if question.question_type == 'text':
            question_data['text_answers'] = list(
                Answer.objects.filter(question=question)
                .exclude(text_answer='')
                .values_list('text_answer', flat=True)
            )
            
        elif question.question_type == 'multiple':
            # Corregido: usando 'answer' en lugar de 'answers'
            question_data['options'] = question.options.annotate(
                answer_count=Count('answer')  # ← Cambio clave aquí
            ).all()
            
        elif question.question_type == 'escala':
            for i in range(1, 6):
                count = Answer.objects.filter(
                    question=question,
                    rating_answer=i
                ).count()
                percentage = round((count / total_responses) * 100) if total_responses > 0 else 0
                question_data['rating_distribution'].append({
                    'value': i,
                    'count': count,
                    'percentage': percentage
                })
                
        questions.append(question_data)
    
    return render(request, 'survey_app/results.html', {
        'survey': survey,
        'questions': questions,
        'total_responses': total_responses
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@require_POST
@staff_member_required
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, created_by=request.user)
    survey.delete()
    return redirect('admin_survey')

@staff_member_required
def admin_survey(request):
    surveys = Survey.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'survey_app/admin_survey.html', {'surveys': surveys})

def save_survey(request, survey_id=None):
    if request.method == "POST":
        survey = Survey.objects.get(id=survey_id) if survey_id else Survey()
        survey.title = request.POST.get('title')
        survey.description = request.POST.get('description')
        survey.save()

        # Guardar preguntas y opciones
        question_ids = []
        for key in request.POST.keys():
            if key.startswith('question_text_'):
                question_id = key.split('_')[-1]
                question_text = request.POST.get(f'question_text_{question_id}')
                question_type = request.POST.get(f'question_type_{question_id}')
                question = Question.objects.create(
                    survey=survey,
                    text=question_text,
                    question_type=question_type
                )
                question_ids.append(question.id)
                  # Opciones de respuesta
            option_index = 0
            while True:
                option_key = f'option_{question.id}_{option_index}'
                option_text = request.POST.get(option_key)
                if option_text is None:
                    break
                if option_text:
                    Option.objects.create(
                        question=question,
                        text=option_text
                    )
                option_index += 1

            # Eliminar opciones que no estén en el formulario
            question.options.exclude(id__in=[opt.id for opt in Option.objects.filter(question=question)]).delete()
    
    return redirect('survey_list')  # Redirige después de guardar
    
    return render(request, 'survey_app/create_survey.html', {'survey': survey, 'edit_mode': True})