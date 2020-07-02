from django.contrib import admin
from .models import Question, Answer, Contact, Account

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('question',)}

admin.site.register(Account)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Contact)
