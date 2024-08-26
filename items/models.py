from django.db import models
from users.models import CustomUser

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

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

    def __str__(self):
        return f"Response to {self.quiz.name} by {self.respondent_id}"
    
    class Meta:
        verbose_name_plural = 'Quizz Entries'

class Answer(models.Model):
    response = models.ForeignKey(QuizEntry, on_delete=models.CASCADE, related_name='answers')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    choice_answer = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return f"Answer to {self.item.question_text} by {self.response.respondent_id}"
