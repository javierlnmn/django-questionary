from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)
    passing_score = models.PositiveIntegerField(help_text='Passing Score (%)', validators=[MaxValueValidator(100)])
    slug = models.SlugField(null=False, unique=True)
    
    @property
    def number_of_questions(self):
        return self.items.count()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Quizzes'
    
class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='items')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, related_name='items')
    question_text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text
    
    class Meta:
        ordering = ('order',)
    
class Choice(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.choice_text} for {self.item.question_text}"

class QuizEntry(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_entries')
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_entries')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_completed(self):
        total_questions = self.quiz.items.count()
        answered_questions = self.answers.filter(quiz_entry=self).count()
        return total_questions == answered_questions
    
    @property
    def is_passed(self):
        total_score = 0
        
        quiz_items = self.quiz.items.all()
        passing_score = self.quiz.passing_score
        
        quiz_total_correct_choices = Choice.objects.filter(is_correct=True, item__in=quiz_items).count()
        
        user_answers = Answer.objects.filter(quiz_entry=self, item__in=quiz_items)
        
        for answer in user_answers:
            total_correct_answers = answer.choice_answer.filter(is_correct=True).count()
            total_answers = answer.choice_answer.count()

            total_score += (total_correct_answers - (total_answers - total_correct_answers))
            
        percentage_score = total_score * 100 / quiz_total_correct_choices
        
        return percentage_score > passing_score
    
    def __str__(self):
        return f"Quiz entry to {self.quiz.name} by {self.respondent}"
    
    class Meta:
        verbose_name_plural = 'Quizz Entries'

class Answer(models.Model):
    quiz_entry = models.ForeignKey(QuizEntry, on_delete=models.CASCADE, related_name='answers')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choice_answer = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return f"Answer to {self.item.question_text} by {self.quiz_entry.respondent}"
    
    class Meta:
        ordering = ('item__order',)
