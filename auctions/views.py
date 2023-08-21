from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Item, Bid
from .forms import BidForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

def index(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, "auctions/index.html", context)


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
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
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

@login_required
def bid(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            if bid_amount > item.current_bid:
                new_bid = Bid(item=item, bidder=request.user, bid_amount=bid_amount)
                new_bid.save()
                item.current_bid = bid_amount
                messages.success(request, 'Your bid has been placed!')
                return redirect('item', item_id=item.id)
            else:
                messages.error(request, 'Your bid must be higher than the current bid.')
    else:
        form = BidForm()
    context = {'form': form, 'item': item}    
    return render(request, 'auctions/bid.html', context)

@login_required
def additem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.current_bid = item.starting_price
            item.save()
            return redirect('index')
        else:
            print(form.errors)
            context = {'form': form, 'message': 'Your item submission is invalid.'}
    else:
        form = ItemForm()
        context = {'form': form}
    return render(request, 'auctions/additem.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=uuid.UUID(str=item_id))
    return render(request, "auctions/item_detail.html", {"item": item})                