from unicodedata import category
from django.urls import path 
from . import views


urlpatterns = [
     
    #abdel __ API URLS 
    path('API/QUIZ/', views.QUIZ_LIST_API),
    path("API_PK/QUIZ/<str:pk>", views.QUIZ_LIST_API_PK),
    
    path('API/CAT/', views.Category_LIST_API),
    path('API_PK/CAT/<str:pk>', views.category_LIST_API_PK),

    path('API/REP/', views.Response_LIST_API),
    path('API_PK/REP/<str:pk>', views.Response_LIST_API_PK),
 
    path('API/RES/', views.Result_LIST_API),
    path('API_PK/RES/<str:pk>', views.Result_LIST_API_PK),


# saved oth
    path('apiSaved/<str:pk>',views.save , name="saveAPI"),

    path('' , views.landing , name ="landing"),

    path('home', views.index ,name="index" ),

    path('categories/',views.categories , name="categories"),

    path('quiz/<str:pk>/',views.quiz , name="quiz"),
    
    path('category/<str:pk>/' , views.category_,name="category"),

    path('login/',views.loginPage, name="login"),

    path('logout/',views.logoutUser, name="logout"),

    path('register/',views.registerPage, name="register"),

    path('profile/<str:pk>/',views.userProfile, name="profile"),

    path('search/',views.search , name="search"),

    path('allquizzes/' , views.allquizzes ,name="quizzes"),

    path('quiz/<str:pk>/data/' , views.quiz_data , name="quiz-data"),

    path('quiz/<str:pk>/save/' ,views.save_quiz , name="quiz-save" ),

    path('profile/<str:pk>/edit' , views.edit , name='edit'),
   
    path('form/',views.form, name="form"),

    path('profile/<str:pk>/history', views.history , name='history' ),

    path('profile/<str:pk>/saved', views.savedQuizzes , name='saved' ),



    #API LINKS : 
    path('API/QUIZ/', views.QUIZ_LIST_API)


    
]