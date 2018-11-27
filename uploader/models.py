from django.db import models
from django.forms import ModelForm


class Document(models.Model):
    upload_id = models.AutoField(primary_key=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
