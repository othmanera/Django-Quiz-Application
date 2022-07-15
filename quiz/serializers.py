from rest_framework import serializers
from rest_framework import routers, serializers, viewsets
from quiz.models import category, Quiz, questions, reponse , result , saved
from django.contrib.auth.models import User
from django.urls import path, include
from django.contrib.auth.models import User
from unicodedata import name
from urllib import response
from django.urls import path, include




'''

# Serializers define the API representation.

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# Routers provide an easy way of automatically determining the URL conf.
# look to understand this 
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


'''

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = questions
        fields = '__all__'


class ReponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = reponse
        fields = '__all__'



# ViewSets define the view behavior.

# we can not add this to secure the responses ; 
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = result
        fields = '__all__'


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = saved
        fields = '__all__'