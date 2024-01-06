from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from .models import *
import datetime
from django.contrib import messages

CHOICES =(
    ("digital", "Digital services"),
    ("cosmetics", "Cosmetics and body care"),
    ("food", "Food and beverage"),
    ("furniture", "Furniture and decor"),
    ("health", "Health and wellness"),
    ("household", "Household items"),
    ("other", "Other"),
)
def is_this_user_bet_this_bid(user,item,bid):

    try:
        bid = bid
        if item.current_bid is None:
            bid = 0
        is_it_true = Bid.objects.filter(item=item, user=user, bid=bid).all()
        print(f"{is_it_true[0].user} placed this bid: {is_it_true[0].bid}")
        return True

    except:
        print("NONE")
        return False
class AuctionForm(forms.Form):
    title = forms.CharField(max_length=50, label="Title")
    description = forms.CharField(widget=forms.Textarea,min_length=5)
    start_price = forms.FloatField(min_value=0)
    picture_url = forms.CharField(required=False)
    category=forms.ChoiceField(choices=CHOICES)

    # seller = forms.ForeignKey(User, on_delete=forms.CASCADE, related_name="selling")
class SortForm(forms.Form):
    category = forms.ChoiceField(choices=CHOICES)
class BidForm(forms.Form):
    bid=forms.FloatField(label="Bid:",min_value=0)
def index(request):
    items=Items.objects.filter(is_closed=False)
    return render(request, "auctions/index.html",{
        "items": items,
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
                "message": "Invalid username and/or password."
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


@login_required(login_url='login')
def create(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method=="POST":
        current_user = request.user.id
        form=AuctionForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data['picture_url']
            if data == "":
                data="https://t3.ftcdn.net/jpg/05/52/37/18/360_F_552371867_LkVmqMEChRhMMHDQ2drOS8cwhAWehgVc.jpg"
            new_item=Items(
                title=form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                start_price = form.cleaned_data['start_price'],
                picture_url = data,
                date=datetime.datetime.now().date(),
                time=datetime.datetime.now().time(),
                seller = request.user,
                category=form.cleaned_data['category'],
            )
            new_item.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html", {
                "form": AuctionForm(),
            })

    return render(request,"auctions/create.html",{
        "form": AuctionForm(),
    })

def auction(request,item_id):
    try:
        item = Items.objects.get(id=item_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    is_current_user=False
    seller=False
    if item.seller==request.user:
        seller=True
    if request.user.is_authenticated:
        is_current_user=is_this_user_bet_this_bid(request.user,item,item.current_bid)
    if request.user.is_authenticated and request.method == 'POST':
        form=BidForm(request.POST)
        if form.is_valid():
            bid=form.cleaned_data['bid']
            current_bid=item.current_bid
            if current_bid is None:
                current_bid=0
            if bid > item.start_price and bid > current_bid:
                new_bid=Bid(user=request.user,item=item,
                            bid=float(bid),
                            date=datetime.datetime.now().date(),time=datetime.datetime.now().time())
                new_bid.save()
                item.current_bid = bid
                item.save()
                return HttpResponseRedirect(reverse('auction',args=(item_id,)))
            else:
                messages.error(request, "Your bid has to be greater than starting price/current bid!!!")
    return render(request,"auctions/auction.html",{
        "item": item,
        "form": BidForm(),
        "is_current_user": is_current_user,
        "seller": seller,
    })
@login_required(login_url='login')
def comment(request,item_id):
    item = Items.objects.get(id=item_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        new_comment = Comment(
            body=request.POST.get('body'),
            user=request.user,
            item=item,
            date=datetime.datetime.now().date(),
            time=datetime.datetime.now().time(),
        )
        new_comment.save()
    return HttpResponseRedirect(reverse("auction", args=(item_id,)))
def categories(request):
    form = SortForm(request.GET)
    for _ in request.user.watchlist.all():
        print(_.title)
        print(_.interested_people.all())
    if form.is_valid():
        category = form.cleaned_data['category']
        return render(request,"auctions/categories.html",{
            "form": SortForm(),
            "items":Items.objects.filter(category=category,is_closed=False),
        })
    return render(request,"auctions/categories.html",{
        "form": SortForm(),
    })
@login_required(login_url='login')
def add_watchlist(request,item_id):
    try:
        item = Items.objects.get(pk=item_id)
        item.interested_people.add(request.user)
    except:
        pass
    return HttpResponseRedirect(reverse('index'))
@login_required(login_url='login')
def delete_watchlist(request,item_id):
    item=Items.objects.get(pk=item_id)
    request.user.watchlist.remove(item)
    return HttpResponseRedirect(reverse('index'))

def watchlist(request):
    return render(request,"auctions/watchlist.html")

@login_required(login_url='login')
def close_the_bid(request,item_id):

    item_to_close=Items.objects.get(pk=item_id)
    if request.user == item_to_close.seller:
        item_to_close.is_closed=True
        item_to_close.save()
    return HttpResponseRedirect(reverse('auction',args=(item_id,)))
@login_required(login_url='login')
def add_like(request,comment_id,item_id):
    comment=Comment.objects.get(pk=comment_id)
    comment.likes.add(request.user)
    comment.save()
    return HttpResponseRedirect(reverse('auction', args=(item_id,)))
@login_required(login_url='login')
def remove_like(request,comment_id,item_id):
    comment=Comment.objects.get(pk=comment_id)
    comment.likes.remove(request.user)
    comment.save()
    return HttpResponseRedirect(reverse('auction', args=(item_id,)))