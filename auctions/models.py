from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=600, default='This is where the description of the item goes.')
    starting_price = models.DecimalField(max_digits=8, decimal_places=2)
    current_bid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField()
    highest_bid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.highest_bid is None or self.highest_bid < self.current_bid:
            self.highest_bid = self.current_bid
        super().save(*args, **kwargs)    

class Bid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
