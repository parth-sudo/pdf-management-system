# Generated by Django 3.2.2 on 2023-07-06 07:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='users_shared_with',
            field=models.ManyToManyField(related_name='shared_pdfs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
