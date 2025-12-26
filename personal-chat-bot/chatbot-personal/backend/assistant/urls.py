from django.urls import path
from assistant import views

urlpatterns = [
    # API endpoints
    path('chat/history/', views.get_chat_history, name='chat_history'),  # GET /api/chat/history/
    path('chat/', views.chat, name='chat'),  # POST /api/chat/
    path('memory/', views.get_memory, name='memory'),  # GET /api/memory/
    # HTML view - should be last to avoid conflicts
    path('', views.chat_view, name='chat_view'),  # GET / or /api/
]

