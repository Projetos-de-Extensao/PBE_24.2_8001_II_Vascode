from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, default="N/A")
    last_name = models.CharField(max_length=50, default="N/A")
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
