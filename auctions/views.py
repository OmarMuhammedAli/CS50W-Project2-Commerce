from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import * 


def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        watchlist = Watchlist.objects.get(watcher=user)
        wcount = len(watchlist.listing.all())
    except:
        wcount = 0
    return render(request, "auctions/index.html", {
        'auction_listings': AuctionListing.objects.filter(is_active=True).all().order_by('date_created'),
        'wcount': wcount
    })


@login_required(login_url="login")
def create_listing(request):
    if request.method == 'POST':
        form = CreateNewListting(request.POST)
        user = User.objects.filter(username=request.user.username).first()
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image_url = form.cleaned_data['image_url']
            if len(image_url) < 1:
                image_url = 'https://www.allianceplast.com/wp-content/uploads/2017/11/no-image.png'
            category = Category.objects.get(pk=int(request.POST['category']))
            
            listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, posted_by=user, category=category)
            listing.save()
            return HttpResponseRedirect(reverse('index'))


    user = User.objects.get(username=request.user.username)
    try: 
        watchlist = Watchlist.objects.get(watcher=user)
    except:
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    return render(request, 'auctions/create_listing.html', {
        'form': CreateNewListting(),
        'categories': Category.objects.all(),
        'wcount': len(watchlist.listing.all())
    })


@login_required(login_url="login")
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    try: 
        watchlist = Watchlist.objects.get(watcher=user)
    except (UnboundLocalError, Watchlist.DoesNotExist):
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    #listing_in_watchlist = [w.listing for w in watchlist]
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist.listing.all(),
        'wcount': len(watchlist.listing.all())
    })


@login_required(login_url="login")
def toggle_watchlist(request, listing_id):
    user = User.objects.get(username=request.user.username)
    try:
        watchlist = Watchlist.objects.get(watcher=user)
    except:
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    
    is_watched = bool(Watchlist.objects.filter(watcher=user, listing=AuctionListing.objects.get(pk=listing_id)))
    if is_watched:
        watchlist.listing.remove(AuctionListing.objects.get(pk=listing_id))
        
    else:
        watchlist.listing.add(AuctionListing.objects.get(pk=listing_id))
        
    return HttpResponseRedirect(reverse('watchlist'))



@login_required(login_url="login")
def categories(request):
    user = User.objects.get(username=request.user.username)
    try: 
        watchlist = Watchlist.objects.get(watcher=user)
    except:
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all(),
        'wcount': len(watchlist.listing.all())
    })


@login_required(login_url="login")
def category_listings(request, category_id):
    user = User.objects.get(username=request.user.username)
    try: 
        watchlist = Watchlist.objects.get(watcher=user)
    except:
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    category = Category.objects.get(pk=category_id)
    listings = category.listings.all()
    return render(request, 'auctions/category_listings.html', {
        'category': category,
        'wcount': len(watchlist.listing.all()),
        'listings': listings
    })


@login_required(login_url="login")
def listing_page(request, listing_id):
    user = User.objects.get(username=request.user.username)
    try: 
        watchlist = Watchlist.objects.get(watcher=user)
    except:
        watchlist = Watchlist()
        watchlist.watcher = user
        watchlist.save()
    listing = AuctionListing.objects.get(pk=listing_id)
    is_owner = bool(listing.posted_by == user)
    is_watched = bool(Watchlist.objects.filter(watcher=user, listing=listing))
    comments = Comment.objects.filter(listing=listing).all()
    try:
        bid = Bid.objects.get(bidder=user)
    except:
        Bid(bidder=user, amount=0.0, listing=listing)
        return render(request, 'auctions/listing.html', {
            'wcount': len(watchlist.listing.all()),
            'listing': listing,
            'is_watched': is_watched,
            'is_owner': is_owner,
            'comments': comments
        })
    highest_amount = Bid.objects.aggregate(Max('amount'))['amount__max']
    highest_bid = Bid.objects.get(amount=highest_amount)
    is_winner = bool(highest_bid.bidder == user)
    return render(request, 'auctions/listing.html', {
        'wcount': len(watchlist.listing.all()),
        'listing': listing,
        'is_watched': is_watched,
        'is_owner': is_owner,
        'is_winner': is_winner,
        'comments': comments
    })


@login_required(login_url="login")
def add_bid(request, listing_id):
    get_bid = request.POST['new_bid']
    listing = AuctionListing.objects.get(pk=listing_id)
    
    if len(get_bid) < 1:
        messages.add_message(request, messages.ERROR, "Please enter a bid", extra_tags='new_bid')
        return HttpResponseRedirect(reverse('listing_page', args=(listing_id, )))
    amount = float(get_bid)
    if amount <= listing.starting_bid or amount <= listing.highest_bid:
        messages.add_message(request, messages.ERROR, f"Please enter a bid higher than ${max(listing.highest_bid, listing.starting_bid)}", extra_tags='new_bid')
        return HttpResponseRedirect(reverse('listing_page', args=(listing_id, )))
    bidder = User.objects.get(username=request.user.username)
    
    new_bid = Bid(listing=listing, amount=amount, bidder=bidder)
    new_bid.save()
    listing.highest_bid = amount
    listing.save()
    return HttpResponseRedirect(reverse('listing_page', args=(listing_id, )))    


@login_required(login_url="login")
def close_auction(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse('listing_page', args=(listing_id, )))


@login_required(login_url="login")
def add_comment(request, listing_id):
    new_comment = request.POST['new_comment']
    user = User.objects.get(username=request.user.username)
    listing = AuctionListing.objects.get(pk=listing_id)
    Comment(comment=new_comment, commenter=user, listing=listing).save()
    return HttpResponseRedirect(reverse('listing_page', args=(listing_id, )))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


