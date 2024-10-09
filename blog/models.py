from django.db import models

class Post(models.Model):
    id_name = models.SlugField(max_length=50,unique=True)
    created_at = models.DateTimeField("date published", auto_now_add=True)
    updated_at = models.DateTimeField("date updated", null=True, auto_now=True)
    ready = models.BooleanField(default=True)
    display = models.BooleanField(default=True)
    post_type =  models.CharField(max_length=100, default='m')
    priority = models.IntegerField(default=0)
    display_name = models.CharField("display name", max_length=200)
    description = models.CharField(max_length=1_000, null=True)
    flags = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.display_name
    
    def is_ready(self):
        return bool(self.flags.get('ready'))
    
    def is_displayed(self):
        return bool(self.flags.get('display'))

    
class Book(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=60, blank=True, default='')
    pub_year = models.CharField(max_length=10, blank=True, default='')
    publisher = models.CharField(max_length=100, blank=True, default='')
    
    def __str__(self):
        return self.title
    