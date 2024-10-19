from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()

    class Meta:
        ordering = ['-published_at'] 

    def __str__(self):
        return self.title
    

class APIKey(models.Model):
    key = models.TextField()
    is_limit_over = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'APIKey'
        verbose_name_plural = 'APIKeys'
    def __str__(self):
        return self.key