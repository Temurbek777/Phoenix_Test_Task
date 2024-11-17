from django.db import models

# Create your models here.
''''
Модель News для хранения Новостей в базе данных
'''
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField(max_length=600)
    views_count = models.PositiveIntegerField(default=0)
    publish_date = models.DateTimeField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title