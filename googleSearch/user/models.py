from django.db import models
from django.contrib.auth.models import User


class Search(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_search',null=False, blank=False )
    search_data = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)


class Meta:
    ordering = ['created_at']
