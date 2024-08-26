from django.contrib import admin
from .models import Quiz, ItemType, Item, Choice, QuizEntry, Answer


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')
    inlines = [ItemInline]
    list_filter = ('name',)

@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description')
    search_fields = ('name', 'code')
    list_filter = ('name',)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'item_type', 'order', 'quiz')
    search_fields = ('question_text',)
    list_filter = ('quiz', 'item_type')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('item', 'choice_text', 'is_correct')
    search_fields = ('choice_text',)
    list_filter = ('item',)

@admin.register(QuizEntry)
class QuizEntryAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'respondent', 'submitted_at')
    search_fields = ('quiz__name', 'respondent__username')
    list_filter = ('quiz', 'respondent', 'submitted_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'item')
    search_fields = ('response__respondent__username', 'item__question_text')
    list_filter = ('response__quiz', 'item')

