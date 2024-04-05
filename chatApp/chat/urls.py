from django.urls import path

from chat.views import home,room

urlpatterns = [
    path("home", home , name="home"),
    path("room/<str:room>/", room , name="room"),
]
