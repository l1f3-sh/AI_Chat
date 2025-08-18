from django.urls import path
from .views import UserRegistrationView, TokenBalanceView, ChatView, UserLoginView

app_name = 'chat_api'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token_balance/', TokenBalanceView.as_view(), name= 'Token Balance'),
    path('chat/', ChatView.as_view(), name='Chat'),
    path('login/', UserLoginView.as_view(), name='Login'),
]
