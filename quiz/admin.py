from django.contrib import admin
from .models import Quiz , questions , category , reponse , result , saved




class ReponseInline(admin.TabularInline):
    model = reponse

class QuestionAdmin(admin.ModelAdmin):
    inlines= [ReponseInline]

admin.site.register(Quiz)
admin.site.register(questions,QuestionAdmin)
admin.site.register(category)
admin.site.register(reponse)
admin.site.register(result)
admin.site.register(saved)


    
    
