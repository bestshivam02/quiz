from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Course)
admin.site.register(Question)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'score', 'created_at')
    list_per_page = 4
    list_filter = ('user',)
admin.site.register(ScoreBoard, ScoreAdmin)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'course')
    list_per_page = 4
    search_fields = ('quiz',)
    list_filter = ('user',)


admin.site.register(Quiz, QuizAdmin)
