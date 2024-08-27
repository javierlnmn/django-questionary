from django.urls import path
from django.views.generic.base import RedirectView
from .views import QuizListView, QuizView, QuizCompletionView

app_name = 'items'

urlpatterns = [
    path('', RedirectView.as_view(url='/quizzes/', permanent=True), name='home'),
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:quiz_id>/', QuizView.as_view(), name='quiz_view'),
    path('quiz/<int:quiz_id>/completion/', QuizCompletionView.as_view(), name='quiz_completion'),
]