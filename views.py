from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()
    return render(request, 'onlinecourse/exam.html', {
        'course': course,
        'questions': questions,
    })


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()
    total = questions.count()
    correct = 0
    selected_ids = {}

    for question in questions:
        choice_key = request.POST.get(f'choice_{question.id}')
        if choice_key:
            try:
                selected = Choice.objects.get(pk=choice_key, question=question)
                Submission.objects.update_or_create(
                    question=question,
                    user=request.user,
                    defaults={'selected_choice': selected}
                )
                if selected.is_correct:
                    correct += 1
                selected_ids[question.id] = int(choice_key)
            except Choice.DoesNotExist:
                continue

    grade = int((correct / total) * 100) if total > 0 else 0
    passed = grade >= 50

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'grade': grade,
        'score': grade,
        'correct': correct,
        'total': total,
        'passed': passed,
        'selected_ids': selected_ids,
    })


@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()
    submissions = Submission.objects.filter(user=request.user, question__course=course)
    correct = sum(1 for s in submissions if s.selected_choice.is_correct)
    total = questions.count()
    grade = int((correct / total) * 100) if total > 0 else 0
    passed = grade >= 50

    selected_ids = {}
    for s in submissions:
        selected_ids[s.question_id] = s.selected_choice_id

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'grade': grade,
        'score': grade,
        'correct': correct,
        'total': total,
        'passed': passed,
        'submissions': submissions,
        'selected_ids': selected_ids,
    })
