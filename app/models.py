from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from .extra_functions import random_string_generator

class PDF(models.Model):
    title = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    file = models.FileField(default = 'blank', upload_to='pdf_files')
    users_shared_with = models.ManyToManyField(User, related_name='shared_pdfs')
    timestamp = models.DateTimeField(default = now)
    guest_code = models.CharField(max_length=6, blank=True, default=random_string_generator())

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    description = RichTextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name="pdf_post")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return f'{self.description[0:10]} ... by {self.author.username}'
