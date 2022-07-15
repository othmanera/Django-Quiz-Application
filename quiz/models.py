from contextlib import nullcontext
from operator import truediv
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User 
import random
from django import forms



class category(models.Model):

    name = models.CharField(max_length=30)
    images = models.CharField(max_length=2048 , null=True)
   #abdel
    description = models.CharField(max_length=500, null=True,blank=True)
    # backgroundimg = models.CharField(max_length=2048 , null=True)
    # img_id = models.IntegerField(null=True)
    #  user_rating = forms.IntegerField(widget=Stars)


    def __str__(self) :
        return self.name
    

class Quiz(models.Model):
    
    name = models.CharField(max_length=30)
    category = models.ForeignKey(category , on_delete=models.SET_NULL , null=True )
    description = models.CharField(max_length=500,blank=True)
    duration = models.IntegerField(null=True,help_text="Time in minutes")
    images = models.CharField(max_length=2048 , null=True)
    level = models.CharField(max_length=50, null=True , blank = True)

    updated=models.DateTimeField(auto_now=True)
    file = models.FileField(blank=True)
    

    def __str__(self) :
        return f"{self.name}--{self.category}"
        
    
    def get_questions(self):
        question = list(self.questions_set.all())
        random.shuffle(question)
        return question


class questions(models.Model):
    description = models.CharField(max_length=500)
    Quiz = models.ForeignKey(Quiz , on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    images = models.CharField(max_length=2048 , null=True, blank=True)

    def __str__(self) :
        return self.description

    def get_reponse(self):
        return self.reponse_set.all()

class reponse(models.Model):
    description = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)
    questions = models.ForeignKey(questions , on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f"Q: {self.questions.description}? | A: {self.description} | correct?: {self.correct}"

class result(models.Model):
    quiz = models.ForeignKey(Quiz , on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    # time = models.IntegerField()
    
    def __str__(self) :
        return f"user : {self.user} | quiz: {self.quiz} | score: {self.score}"

class saved(models.Model):
    quiz = models.ForeignKey(Quiz , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) :
        return f"user : {self.user} | quiz: {self.quiz}"

