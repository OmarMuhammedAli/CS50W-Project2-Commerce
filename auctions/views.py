from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import * 


def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        watchlist = Watchlist.objects.filter(watcher=user).all()
    except:
        watchlist = []
    return render(request, "auctions/index.html", {
        'auction_listings': AuctionListing.objects.filter(is_active=True).all().order_by('date_created'),
        'wcount': len(watchlist)
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
    watchlist = Watchlist.objects.filter(watcher=user).all()
    return render(request, 'auctions/create_listing.html', {
        'form': CreateNewListting(),
        'categories': Category.objects.all(),
        'wcount': len(watchlist)
    })


@login_required(login_url="login")
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(watcher=user).all()
    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
        'wcount': len(watchlist)
    })


@login_required(login_url="login")
def categories(request):
    user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(watcher=user).all()
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.all(),
        'wcount': len(watchlist)
    })


@login_required(login_url="login")
def category_listings(request, category_id):
    user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(watcher=user).all()
    category = Category.objects.get(pk=category_id)
    listings = category.listings.all()
    return render(request, 'auctions/category_listings.html', {
        'category': category,
        'wcount': len(watchlist),
        'listings': listings
    })


@login_required(login_url="login")
def listing_page(request, listing_id):
    user = User.objects.get(username=request.user.username)
    watchlist = Watchlist.objects.filter(watcher=user).all()
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, 'auctions/listing.html', {
        'wcount': len(watchlist),
        'listing': listing
    })



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


