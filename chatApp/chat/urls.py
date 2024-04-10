from django.urls import path

from chat.views import RoomDeleteView, home, room

urlpatterns = [
    path("home/", home, name="home"),
    path("room/<str:room>/", room, name="room"),
    path("room/<slug:room>/delete/", RoomDeleteView.as_view(), name="delete_room"),
]
