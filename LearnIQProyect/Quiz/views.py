from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Question, Answer, QuizResult
from .forms import QuizForm
import random

@login_required
def take_quiz(request):
    # Obtener 3 preguntas aleatorias de cada tipo
    visual_questions = list(Question.objects.filter(question_type='visual'))
    auditory_questions = list(Question.objects.filter(question_type='auditory'))
    kinesthetic_questions = list(Question.objects.filter(question_type='kinesthetic'))
    questions = visual_questions + auditory_questions + kinesthetic_questions
    random.shuffle(questions)
    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            print("Form cleaned data:", form.cleaned_data)
            user = request.user
            result, created = QuizResult.objects.get_or_create(user=user)

            # Resetear los puntajes
            result.visual_score = 0
            result.auditory_score = 0
            result.kinesthetic_score = 0

            for question in questions:
                answer_id = form.cleaned_data.get(f'question_{question.id}')
                if answer_id:
                    try:
                        selected_answer = Answer.objects.get(id=answer_id)
                        if selected_answer.is_correct:
                            if question.question_type == 'visual':
                                result.visual_score += 1
                            elif question.question_type == 'auditory':
                                result.auditory_score += 1
                            elif question.question_type == 'kinesthetic':
                                result.kinesthetic_score += 1
                    except Answer.DoesNotExist:
                        continue

            result.save()
            return redirect('results')
        else:
            print("Form errors:", form.errors)  # Para depuración
            print("Form cleaned data:", form.cleaned_data)  # Para depuración
    else:
        form = QuizForm(questions=questions)

    return render(request, 'Quiz/take_quiz.html', {'form': form, 'questions': questions})

@login_required
def results(request):
    result = QuizResult.objects.filter(user=request.user).last()
    if not result:
        return HttpResponse("No quiz results found.")
    return render(request, 'Quiz/results.html', {'result': result})
