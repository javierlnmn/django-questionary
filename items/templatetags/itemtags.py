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