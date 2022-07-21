# 데이터를 주고받는 양식 지정
from dataclasses import fields
from rest_framework import serializers
from .models import Todo

class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'complete', 'important')

class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'created', 'complete', 'important')


class TodoCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'important')


