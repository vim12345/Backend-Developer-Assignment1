from rest_framework import serializers
from .models import User, Paragraph

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'dob', 'createdAt', 'modifiedAt')
        read_only_fields = ('id', 'createdAt', 'modifiedAt')

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ('id', 'content')
        read_only_fields = ('id',)

