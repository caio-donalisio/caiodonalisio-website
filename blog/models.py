from django.db import models

def default_flags():
    return dict(ready=True, display=False, type='m', priority=0)

class Post(models.Model):
    id_name = models.SlugField(max_length=50,unique=True)
    create_date = models.DateTimeField("date published")
    update_date = models.DateTimeField("date updated", null=True, auto_now=True)
    flags = models.JSONField(default=default_flags)
    display_name = models.CharField("display name", max_length=200)
    description = models.CharField(max_length=1_000, null=True)
    
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
    author = models.CharField(max_length=60)
    pub_year = models.CharField(max_length=10)
    publisher = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    