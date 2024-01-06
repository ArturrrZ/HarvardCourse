from django.contrib.auth.models import AbstractUser
from django.db import models
CHOICES =(
    ("digital", "Digital services"),
    ("cosmetics", "Cosmetics and body care"),
    ("food", "Food and beverage"),
    ("furniture", "Furniture and decor"),
    ("health", "Health and wellness"),
    ("household", "Household items"),
    ("other", "Other"),
)

class User(AbstractUser):
    watchlist=models.ManyToManyField("Items", blank=True, null=True,related_name="interested_people")
    likes=models.ManyToManyField("Comment",blank=True,null=True,related_name="likes")

    def __str__(self):
        return f"{self.username}"

class Items(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    start_price=models.FloatField()
    picture_url=models.TextField(null=True, blank=True)

    seller=models.ForeignKey(User, on_delete=models.CASCADE, related_name="selling")
    date=models.DateField()
    time=models.TimeField()
    category=models.CharField(max_length=100,choices=CHOICES)
    current_bid=models.FloatField(blank=True,null=True) #reference to BIDS NULLABEL TRUE
    is_closed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"



class Comment(models.Model):
    body=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item=models.ForeignKey(Items,on_delete=models.CASCADE,related_name="comments")
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return f"{self.user} to {self.item}"
class Bid(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    item=models.ForeignKey(Items,on_delete=models.CASCADE,related_name="bids")
    bid=models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return f"{self.bid}$ to {self.item}"