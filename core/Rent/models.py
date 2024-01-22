from django.db import models
from django.contrib.auth.models import User
import random
import string


class Resource(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=100)
    resource_description = models.TextField()
    resource_image = models.ImageField(upload_to="resource")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.resource_name
    
    
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, default='9131852123') 
    unique_id = models.CharField(max_length=11, primary_key=True)  # Increased max_length to accommodate "CFP-" + 7 characters
    # other fields for your Customer model

    def generate_unique_id(self):
        chars = string.ascii_letters + string.digits
        while True:
            unique_suffix = ''.join(random.choice(chars) for _ in range(7))
            unique_id = f"CFP-{unique_suffix}"  # Add "CFP-" prefix
            if not Customer.objects.filter(unique_id=unique_id).exists():
                self.unique_id = unique_id
                break
