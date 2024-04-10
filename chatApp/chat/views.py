from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from chat.forms import RoomForm
from chat.models import Message, Room
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home(request):
    rooms = Room.objects.all().order_by("-id")
    if request.GET.get("page") is not None:
        page = int(request.GET["page"])
        paginator = Paginator(rooms, 6).get_page(page)
    else:
        paginator = Paginator(rooms, 6).get_page(1)
    context = {"form": RoomForm, "rooms": paginator}

    if request.method == "POST":
        roomForm = RoomForm(request.POST)
        if roomForm.is_valid():
            Room.objects.create(
                name=roomForm.cleaned_data["name"], creator=request.user
            )
            messages.success(request, "Room created successfully")
            return redirect("home")
        else:
            message = str(roomForm.errors).split("<li>")[2].split(".")[0]

            context.update({"errors": message})
            return render(request, "chat/home.html", context=context)

    return render(request, "chat/home.html", context=context)


@login_required
def room(request, room):
    room = Room.objects.filter(name=room).get()
    messsages = Message.objects.filter(room=room)
    context = {"room": room.name, "messages": messsages}
    return render(request, "chat/room.html", context=context)


class RoomDeleteView(DeleteView, SuccessMessageMixin, LoginRequiredMixin):
    model = Room
    success_url = reverse_lazy("home")
    template_name = "chat/detele_room.html"
    slug_field = "slug"
    slug_url_kwarg = "room"
    success_message = "Room supprimé avec succès"
