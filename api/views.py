from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Paragraph
from .serializers import ParagraphSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer

class SearchParagraphView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParagraphSerializer

    def get_queryset(self):
        word_to_search = self.request.query_params.get('word', '')
        paragraphs = Paragraph.objects.filter(content__icontains=word_to_search)[:10]
        return paragraphs

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user_id': user.id,
            'token': token.key,
        }, status=status.HTTP_201_CREATED)

class UserLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user_id': user.id,
            'token': token.key,
        }, status=status.HTTP_200_OK)

class MyAuthenticatedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Your view logic here
        return Response({'message': 'Authenticated view'})


# Create your views here.
