from django.db import models

# For environment variables
import os
from dotenv import load_dotenv
load_dotenv()

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SearchQuery(models.Model):
    query = models.CharField(max_length=255)

    def __str__(self):
        return self.query
    
class Video(models.Model):
    video_id = models.CharField(max_length=255, default='-', unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    searchQuery = models.ForeignKey(
        SearchQuery, 
        on_delete=models.CASCADE, 
        related_name='videos', 
        default=1
    )

    class Meta:
        ordering = ['-published_at'] 

    def __str__(self):
        return self.title
    

class APIKey(models.Model):
    key = models.TextField(unique=True)
    is_limit_over = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'APIKey'
        verbose_name_plural = 'APIKeys'
    def __str__(self):
        return self.key
    
class FetchHistory(models.Model):
    last_video_id = models.TextField()
    last_fetch_time = models.DateTimeField()
    
    class Meta:
        ordering = ['-last_fetch_time']

    def __str__(self):
        return self.last_video_id