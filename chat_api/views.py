from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import Chat, User
from django.contrib.auth import login, get_user_model

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            #create a token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token' : token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    renderer_classes = APIView.renderer_classes
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.data['token']:
            user = get_user_model().objects,get(username=request.data['username'])
            login(request, user)
        return response




class ChatView(CreateAPIView):
    #Use DRF's permission class to ensure the user is authenticated

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        message = request.data.get('message')

        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        if user.tokens < 100:
            return Response({'error': 'Insufficient tokens'}, status=status.HTTP_402_PAYMENT_REQUIRED) 

        user.tokens -= 100
        user.save()

        ai_response = f"This is a dummy AI response to your message: '{message}'" 
        Chat.objects.create(user=user, message=message, response=ai_response)

        return Response({'response': ai_response}, status=status.HTTP_200_OK)
    
class TokenBalanceView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'tokens': request.user.tokens}, status=status.HTTP_200_OK)