from django.db import models

from app.user.models import User

class ProductFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_feedbacks')
    feedback_text = models.TextField()
    feedback_type = models.CharField(max_length=50, choices=[('suggestion', 'Suggestion'), ('comment', 'Comment'), ('error', 'Error')])
    created_at = models.DateTimeField(auto_now_add=True)