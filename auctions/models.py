from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime

class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=datetime.today())
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings')
    image_url = models.CharField(max_length=250, default='https://www.allianceplast.com/wp-content/uploads/2017/11/no-image.png')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    date_created = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return f'${self.amount}; Bidder: {self.bidder}'


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=280)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date_created = models.DateTimeField(default=datetime.today())

    def __str__(self):
        return f'"{self.comment}", {self.commenter}'