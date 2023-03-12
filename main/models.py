from django.db import models
from django.contrib.auth.models import User

class UserRecipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_value = models.JSONField()
    is_public = models.BooleanField(default=False)
    image_link = models.URLField()
# Create your models here.
