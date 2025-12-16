from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Subject, Question
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


SUBJECTS = ['C', 'Python', 'Java', 'JavaScript']


def home(request):
    subjects = Subject.objects.all()
    return render(request, 'quiz/home.html', {'subjects': subjects})


def quiz_c(request):
    subject = get_object_or_404(Subject, name="C Programming Language")
    questions = Question.objects.filter(subject=subject)
    if request.method == "POST":
        return submit_quiz(request, questions, subject, 'c_result.html')
    return render(request, 'quiz/c_quiz.html', {'subject': subject, 'questions': questions})


def quiz_python(request):
    subject = get_object_or_404(Subject, name="Python")
    questions = Question.objects.filter(subject=subject)
    if request.method == "POST":
        return submit_quiz(request, questions, subject, 'python_result.html')
    return render(request, 'quiz/python_quiz.html', {'subject': subject, 'questions': questions})


def quiz_java(request):
    subject = get_object_or_404(Subject, name="Java Programming Language")
    questions = Question.objects.filter(subject=subject)
    if request.method == "POST":
        return submit_quiz(request, questions, subject, 'java_result.html')
    return render(request, 'quiz/java_quiz.html', {'subject': subject, 'questions': questions})


def quiz_js(request):
    subject = get_object_or_404(Subject, name="JavaScript")
    questions = Question.objects.filter(subject=subject)
    if request.method == "POST":
        return submit_quiz(request, questions, subject, 'javascript_result.html')
    return render(request, 'quiz/javascript_quiz.html', {'subject': subject, 'questions': questions})


def submit_quiz(request, questions, subject, template_name):
    score = 0
    results = []
    for question in questions:
        selected = request.POST.get(str(question.id))
        correct = (selected == question.correct_option)

        results.append({
            'question': question.question_text,
            'selected': selected,
            'correct_answer': question.correct_option,
            'is_correct': correct,
            'options': {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d,
            }
        })

        if correct:
            score += 1

    context = {
        'subject': subject,
        'score': score,
        'total': len(questions),
        'results': results,
    }
    return render(request, f'quiz/{template_name}', context)


def next_subject(request, subject_name):
    try:
        index = SUBJECTS.index(subject_name)
    except ValueError:
        return redirect('home')

    if index + 1 < len(SUBJECTS):
        next_subject_name = SUBJECTS[index + 1]
        if next_subject_name == 'Python':
            return redirect('quiz_python')
        elif next_subject_name == 'Java':
            return redirect('quiz_java')
        elif next_subject_name == 'JavaScript':
            return redirect('quiz_js')
    else:
        return redirect('end_quiz')

    return redirect('home')


def download_pdf(request, subject_name):
    from reportlab.lib.units import inch

    clean_name = subject_name.lower().replace(" ", "_")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{clean_name}.result.pdf"'

    pdf = SimpleDocTemplate(response, pagesize=letter,
                            leftMargin=1*inch, rightMargin=1*inch,
                            topMargin=0.7*inch, bottomMargin=0.7*inch)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1A1A1A'),
        alignment=TA_CENTER,
        spaceAfter=25
    )

    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        alignment=0,
        spaceAfter=8
    )

    message_style = ParagraphStyle(
        'MessageStyle',
        parent=styles['Normal'],
        fontSize=13,
        alignment=0,
        spaceAfter=15
    )

    feedback_style = ParagraphStyle(
        'FeedbackStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#2E2E2E'),
        leading=18,
        alignment=0,
        spaceAfter=25
    )

    subject_titles = {
        "C Programming Language": "C Quiz Result",
        "Python": "Python Quiz Result",
        "Java Programming Language": "Java Quiz Result",
        "JavaScript": "JavaScript Quiz Result",
    }
    title = subject_titles.get(subject_name, f"{subject_name} Quiz Result")
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.5*inch))

    score = int(request.GET.get('score', 0))
    total = int(request.GET.get('total', 30))
    elements.append(Paragraph(f"<b>Your Score:</b> {score}/{total}", score_style))
    elements.append(Spacer(1, 5))

    if score >= 15:
        msg = "<font color='green'>🎉 Congratulations! You passed the test!</font>"
    else:
        msg = "<font color='red'>Better luck next time.</font>"
    elements.append(Paragraph(msg, message_style))
    elements.append(Spacer(1, 15))

    if score >= 25:
        feedback = "Excellent performance! Keep it up!"
    elif 15 <= score < 25:
        feedback = "Good job! But surely a little more practice will help you reach perfection."
    else:
        feedback = "You can do better! Review your weak areas and try again."

    elements.append(Paragraph(f"<b>Feedback:</b> {feedback}", feedback_style))

    pdf.build(elements)
    return response


def end_quiz(request):
    return render(request, 'quiz/end_quiz.html')

