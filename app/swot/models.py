from django.db import models

from app.user.models import User

class SWOTAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swot_analyses')
    strengths = models.TextField()
    weaknesses = models.TextField()
    opportunities = models.TextField()
    threats = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)