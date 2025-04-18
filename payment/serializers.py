from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class EventSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'