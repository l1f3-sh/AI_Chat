from django.urls import path
from .views import UserRegistrationView, TokenBalanceView, ChatView, UserLoginView, ChatHistoryView

app_name = 'chat_api'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='Register'),
    path('token_balance/', TokenBalanceView.as_view(), name= 'TokenBalance'),
    path('chat/', ChatView.as_view(), name='Chat'),
    path('login/', UserLoginView.as_view(), name='Login'),
    path('history/', ChatHistoryView.as_view(), name='ChatHistory'),
]
