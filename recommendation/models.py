from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    value = models.FloatField()

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    score = models.FloatField()  

class Product(models.Model):
    item_id = models.IntegerField(unique=True)  # Unique identifier for each product
    name = models.CharField(max_length=255)
    description = models.TextField()
    item_image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Image field

    def __str__(self):
        return self.name

