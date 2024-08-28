from django.urls import path
from django.views.generic.base import RedirectView
from .views import QuizListView, QuizView, QuizCompletionView

app_name = 'items'

urlpatterns = [
    path('', RedirectView.as_view(url='/quizzes/', permanent=True), name='home'),
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<slug:quiz_slug>/', QuizView.as_view(), name='quiz_view'),
    path('quiz/<slug:quiz_slug>/completion/', QuizCompletionView.as_view(), name='quiz_completion'),
]