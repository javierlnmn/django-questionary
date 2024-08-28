from django import template
from items.models import QuizEntry, Answer

register = template.Library()

@register.simple_tag
def is_quiz_completed_by_user(quiz, user):
    quiz_entry = QuizEntry.objects.filter(quiz=quiz, respondent=user).first()
    if not quiz_entry:
        return False
    total_questions = quiz.items.count()
    answered_questions = Answer.objects.filter(quiz_entry=quiz_entry).count()
    return total_questions == answered_questions

@register.simple_tag
def is_quiz_passed_by_user(quiz, user):
    quiz_entry = QuizEntry.objects.filter(quiz=quiz, respondent=user).first()
    return quiz_entry.is_passed

@register.simple_tag
def remaining_items_by_user(quiz, user):
    quiz_entry = QuizEntry.objects.filter(quiz=quiz, respondent=user).first()
    if not quiz_entry: 
        return 0
    quiz_items = quiz_entry.quiz.items.count()
    answered_items = quiz_entry.answers.count()
    return 0 if quiz_items == answered_items or answered_items == 0 else quiz_items - answered_items