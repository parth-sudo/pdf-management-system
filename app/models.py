from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class PDF(models.Model):
    title = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    file = models.FileField(default = 'blank', upload_to='pdf_files')
    users_shared_with = models.ManyToManyField(User, related_name='shared_pdfs')

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    description = models.TextField(blank = False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE, related_name="pdf_post")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return f'{self.author.username}s comment -{self.pk}'
