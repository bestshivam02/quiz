from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Course)
admin.site.register(Question)
admin.site.register(ScoreBoard)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'course')
    list_per_page = 4
    search_fields = ('quiz',)
    list_filter = ('user',)


admin.site.register(Quiz, QuizAdmin)
