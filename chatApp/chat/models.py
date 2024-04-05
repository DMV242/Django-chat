from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

# Create your models here.


class Room(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="Le nom ne doit contenir que des lettres et des chiffres.",
                code="invalid_champ",
            ),
        ],
        error_messages={"unique": "Une room avec  ce nom existe déjà."},
    )

    def __str__(self) -> str:
        return "Room " + self.name


class Message(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE)
    sended_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name=("image"), upload_to="images/", blank=True)

    def __str__(self) -> str:
        return "Message de " + self.author.get_username() + f"-{self.sended_date}"
