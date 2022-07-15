
#-------------------------------------------------------------------
from django import http
from quiz.serializers import CategorySerializer, QuizSerializer, ReponsesSerializer, ResultSerializer, SavedSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import status

from django import forms  # For the authentification form
from django.shortcuts import redirect, render  # For rendering (displaying) our content
from .models import Quiz , category , questions, reponse , result , saved  # To acquire the data from our models, then render it
from django.contrib.auth.models import User  # For verifying the user's given login info
from django.db.models import Q  # For searching based on multiple critereas
from django.contrib import messages  # For error flash messages 
from django.contrib.auth import authenticate , login , logout  # For user autentification (login/logout)
from django.contrib.auth.decorators import login_required # Forcing the user to login before doing something we specify
from quiz.forms import RegistrationForm
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.http import Http404


#Global counter for visiters to limit the number of quizzes they can play
visits = 0





#landing page
def landing(request):

    if not request.user.is_authenticated:
        return render(request, "quiz/landing.html" )
    else:
        return redirect('index')
    

# home page
def index(request):
    quizs = Quiz.objects.all()
    
    categorie = category.objects.all()
    if request.user.is_authenticated:
      return render(request , "quiz/index.html", {'quiz': quizs, 'category':categorie , 'range':range( 0,5 )})
    else:
        return redirect('landing')



# Login page
def loginPage(request):
    global visits
    categorie = category.objects.all()

    page = 'login'
    # Collecting login informations given by the user
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
    
    #if the user does not exist: 
        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request,'User does not exist')  
  
    #if the user exists:
        user = authenticate(request , username=username , password=password) #We verify his login infos 
    
    #if the infos are correct we log the user in and create a session:
        if user is not None:
            login(request , user , backend='django.contrib.auth.backends.ModelBackend' )
            return redirect('index')

        else:
            messages.error(request,'Incorrect username or password')  
    context = {'page':page , 'category':categorie , 'visits':visits}
    return render(request,"quiz/login_register.html",context)

#user logout
def logoutUser(request):
    global visits
    visits=0 #Resetting the visits counter after each logout 
    logout(request)
    return redirect('landing')


# Registration page
def registerPage(request):
    categorie = category.objects.all()

    form = RegistrationForm() #using the django generated registration form
    if request.method =='POST': #we collect the user's given data
       
        form = RegistrationForm(request.POST) #we pass it to the creation form
        
        if form.is_valid(): #we verify if the form is valid
            user = form.save(commit=False) 
            user.username = user.username.lower() #we lower the user's username
            user.save() #we save the user
            login(request,user, backend='django.contrib.auth.backends.ModelBackend' ) #we log the user in
            return redirect('index') #redirecting the user to the form page to either complete his registration or skip it for later
             
        else:
            messages.error(request, 'An error occurred during your registration. Please try again.')        
    return render(request,'quiz/login_register.html',{'form':form , 'category':categorie})


def userProfile(request,pk):
    categorie = category.objects.all()
    results = result.objects.all()
    user = User.objects.get(username=pk)
    context = {'user':user , 'category':categorie , 'results': results , 'range':range( 0,5 ) }
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect ('login')
        else:
            return render(request,"quiz/profile.html",context)



#search results page
def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    quizs = Quiz.objects.filter(
        Q(category__name__icontains=q) |    
        Q(name__icontains=q)
        )
    
    categorie = category.objects.all()

    return render(request , "quiz/search.html", {'quiz': quizs, 'category':categorie , 'q':q})



# Page with all categories
def categories(request):
    categorie = category.objects.all()
    quizz = Quiz.objects.all()
    
    if request.user.is_authenticated:
        return render(request , "quiz/categories.html",{'category':categorie ,'quiz':quizz})
    else:
        return redirect('landing')


# Page with each category and its quizzes
def category_(request,pk):
    categorie = category.objects.get(name=pk)
    cat = category.objects.all() 
    quizs = Quiz.objects.all()
    if request.user.is_authenticated:
        return render(request, "quiz/category.html", {'categorie':categorie,'quiz':quizs , 'category':cat })
    else:
        return redirect('landing')



# page with all quizzes
def allquizzes(request):
    quizs = Quiz.objects.all()  
    categorie = category.objects.all() 
    if request.user.is_authenticated:
        return render(request, "quiz/allquizzes.html", {'quiz':quizs, 'category':categorie}) 
    else:
        return redirect('landing')

# page with each quiz

def quiz(request,pk):
    global visits
    if request.method== 'GET':
        visits+=1
        if not request.user.is_authenticated:
            if visits > 3:
                return redirect('login')
    categorie = category.objects.all() 
    quizs = Quiz.objects.get(name=pk)
    context = {'quiz':quizs , 'category':categorie}
    return render(request , "quiz/quiz.html" , context)



#Acquiring the quiz data (questios/answers) to display it on the page
def quiz_data(request,pk):
    quiz = Quiz.objects.get(name=pk)
    questions = []
    for q in quiz.get_questions():
        answers=[]
        for a in q.get_reponse():
            answers.append(a.description)
        questions.append( {str(q):answers} ) 
    
    return JsonResponse(
        {
            'data':questions,
            'time':quiz.duration,
        }
    ) 





#------- Solution to is_ajax() being undefined in the latest versions of django-----

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ajax_test(request):
    if is_ajax(request= request):
        message = "This is ajax"
    else:
        message = "Not ajax"
    return HttpResponse(message)
#-----------------------------------------------------------------------
def save_quiz(request, pk):
    # print(request.POST)
    if is_ajax(request=request):
        questions_ = []
        data = request.POST
        data_ = dict(data.lists())
        
        data_.pop('csrfmiddlewaretoken')
        
       

        for k in data_.keys():
            print('key: ',k)
            question= questions.objects.get(description=k)
            questions_.append(question)
        print(questions_)

       

        user = request.user
        quiz=Quiz.objects.get(name = pk)
        
        score = 0
        results = []
        correct_answer = None


        for q in questions_:
            selected_Answer = request.POST.get(q.description)

            if selected_Answer != "":
                question_answers= reponse.objects.filter(questions=q)
                for a in question_answers:
                    if selected_Answer == a.description:
                        if a.correct:
                            score +=1
                            correct_answer = a.description

                    else:
                        if a.correct:
                            correct_answer = a.description

                results.append({ str(q):{'correct_answer': correct_answer,'answered': selected_Answer }})
            
            else:
                results.append({str(q): 'not answered'})
        
        if request.user.is_authenticated:
            result.objects.create(quiz=quiz , user=user, score=score)

        return JsonResponse({ 'score': score, 'results': results })

  


#Form page
def form(request ):
    
    return render(request , "quiz/forms.html") 


#Quiz History page
def history(request,pk):
    Saved = saved
    results = result.objects.all()
    user = User.objects.get(username=pk)
    context = {'user':user, "results":results,"saved":Saved }
    return render(request,"quiz/history.html",context)

#Editing user's informations page
def edit(request,pk):
    user = User.objects.get(username=pk)
    categorie = category.objects.all() 
    return render(request, "quiz/Edit.html", {'user': user , 'category':categorie})


#saved quizzes
def savedQuizzes(request,pk): 
    Saved = saved.objects.all()
    user = User.objects.get(username=pk)
    categorie = category.objects.all() 
    context = {'user':user, "saved":Saved ,'category':categorie}

    return render(request, "quiz/saved.html", context)


# Save API
# @api_view(['GET','POST'])
def save(request,pk):
    try:
        save = saved.objects.filter(id=pk)
    except saved.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     save = saved.objects.all()
    #     serializer = SavedSerializer(save, many=True)
    #     return Response(serializer.data)
    
    # if request.method == 'GET':

    #     if request.user.is_authenticated:
    #         username = request.user
    #     Q= saved.quiz.name
    #     saved.objects.create(quiz=Q)
    #     
        
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Log in to save quizzes')
            return redirect('quizzes')

        elif request.user.is_authenticated:
            S=saved.objects.all()
            Q=Quiz.objects.get(id=pk)
            username = request.user
            exist=0
            for i in S:
                if i.quiz == Q and i.user == username:
                    exist=1
              

        if exist ==0:    
            saved.objects.create(quiz=Q,user=username)
            messages.error(request, 'Quiz succesfully saved')
        else:
            messages.error(request, 'You already saved this quiz')
        return redirect(request.META.get('HTTP_REFERER'))

        




#abdel
#-----------------------OUR_API---------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------


@api_view(['GET', 'POST'])
def QUIZ_LIST_API(request):
    #GET
    if request.method == 'GET':
        quiz = Quiz.objects.all()
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
         serializer = QuizSerializer(data=request.data)
         if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status.HTTP_201_CREATED)
         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def QUIZ_LIST_API_PK(request, pk):
   # good use for any querys

    try:
        quiz = Quiz.objects.filter(id=pk)
    except Quiz.DoesNotExist:
        return Response (status=status.HTTP_404_NOT_FOUND)
 
    print(quiz)

    #GET
    if request.method == 'GET':
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)

    #PUT : UPDATE
    elif request.method == 'PUT':
        serializer = QuizSerializer(quiz, data= request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    if request == 'DELETE':
        quiz.delete()
        return Response("msg")


    #return Response("the object is deleted", status=status.HTTP_204_NO_CONTENT)


#----------------------------------CATEGORY API ---------------------------------------------------------------------


@api_view(['GET', 'POST'])
def Category_LIST_API(request):
     #GET
    if request.method == 'GET':
         catg = category.objects.all()
         serializer = CategorySerializer(catg, many=True)
         return Response(serializer.data)

    elif request.method == 'POST':
           serializer = CategorySerializer(data = request.data)
           if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
           return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT','DELETE'])

def category_LIST_API_PK(request, pk):
   # good use for any querys

    try :
     catg = category.objects.filter(id=pk)
    except category.DoesNotExist:
        return Response (status= status.HTTP_404_NOT_FOUND)


    #GET
    if request.method == 'GET':
        serializer = CategorySerializer(catg, many=True)
        return Response(serializer.data)


    #PUT : UPDATE
    elif request.method == 'PUT':
        serializer = CategorySerializer(catg, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    if request == 'DELETE':
        catg.delete()
        return Response("message here", status=status.HTTP_204_NO_CONTENT)      



#-------------------------------------------------------------------------------------------


@api_view(['GET','POST'])
def Response_LIST_API(request):
   # good use for any querys
    #GET
    if request.method == 'GET':
        resp = reponse.objects.all()
        serializer = ReponsesSerializer(resp, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
         serializer = ReponsesSerializer(data=request.data)
         if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status.HTTP_201_CREATED)
         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
def Response_LIST_API_PK(request, pk):
   # good use for any querys

    try:
     resp = reponse.objects.filter(id=pk)
    except reponse.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #GET
    if request.method == 'GET':
        serializer = ReponsesSerializer(resp, many=True)
        return Response(serializer.data)

    #PUT : UPDATE
    elif request.method == 'PUT':
         serializer = ReponsesSerializer(resp, data=request.data)

         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

         return Response(serializer.errors)

    if request == 'DELETE':
        resp.delete()
        return Response("deleted succefuly ")


    



#--------------------------------------------------------------------------------


@api_view(['GET', 'POST'])
def Result_LIST_API(request):
     #GET
    if request.method == 'GET':
         reslt = result.objects.all()
         serializer = ResultSerializer(reslt, many=True)
         return Response(serializer.data)

    elif request.method == 'POST':
         serializer = ResultSerializer(data=request.data)

         if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status.HTTP_201_CREATED)
         return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
def Result_LIST_API_PK(request, pk):
    # good use for any querys

    try:
     rslt = result.objects.filter(id=pk)
    except result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #GET
    if request.method == 'GET':
        serializer = ResultSerializer(rslt, many=True)
        return Response(serializer.data)

    #PUT : UPDATE
    elif request.method == 'PUT':
        serializer = ResultSerializer(rslt, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    if request == 'DELETE':
        rslt.delete()
        return Response("deleted succefuly ")

# ----------------------------------------------------------
