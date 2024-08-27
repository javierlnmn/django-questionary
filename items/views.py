from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quiz, Item, Choice, Answer, QuizEntry

class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 10
    
class QuizView(LoginRequiredMixin, View):
    
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        items = quiz.items.all()
        
        answered_items = Answer.objects.filter(quiz_entry__quiz=quiz, quiz_entry__respondent=request.user).values_list('item_id', flat=True)
        next_item = items.exclude(id__in=answered_items).first()

        if not next_item:
            return redirect('items:quiz_completion', quiz_id=quiz.id)
        
        context = {
            'quiz': quiz,
            'current_item': next_item,
            'choices': next_item.choices.all(),
        }
        return render(request, 'items/quiz_question.html', context)
    
    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        
        quiz_entry, created = QuizEntry.objects.get_or_create(
            quiz=quiz, 
            respondent=request.user
        )
        
        choice_ids = request.POST.getlist('choices')
        
        answer, _ = Answer.objects.get_or_create(
            quiz_entry=quiz_entry,
            item=item
        )
        
        answer.choice_answer.set(choice_ids)
        
        return redirect('items:quiz_view', quiz_id=quiz.id)
    

class QuizCompletionView(LoginRequiredMixin, TemplateView):
    template_name = 'items/quiz_completion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        quiz_id = self.kwargs.get('quiz_id')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        quiz_entry = get_object_or_404(QuizEntry, quiz=quiz, respondent=self.request.user)
        
        
        context['quiz'] = quiz
        context['quiz_entry'] = quiz_entry
        return context