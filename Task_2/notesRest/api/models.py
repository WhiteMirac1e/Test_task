from django.db import models


class Note(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    note = models.CharField(max_length=120)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return self.note
