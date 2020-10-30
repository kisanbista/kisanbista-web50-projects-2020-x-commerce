from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import User,Product,Watchlist,Bid,Comment
from .forms import ProductForm
from decimal import Decimal
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html")


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
def create_product(request):
    if request.method == 'GET':
        return render(request, 'auctions/create_product.html',{"form":ProductForm})
    else:
        form = ProductForm(request.POST)
        new_list = form.save(commit = False)
        new_list.user = request.user
        new_list.save()
    
    return redirect('index')

def active_listings(request):
    obj = Product.objects.filter(dateCompleted = None)
    length = len(obj)
    return render(request,"auctions/active_listings.html",{"objects":obj,"length":length})

def listpage(request, product_id):
    obj = get_object_or_404(Product, pk = product_id)
    comment = Comment.objects.filter(product = obj)
    if obj is not None:
        if obj.dateCompleted is None:
            if obj.user == request.user:
                return render(request,"auctions/list_page.html",{"object":obj,"closing":True,"comments":comment})
            else:
                return render(request, "auctions/list_page.html",{"object":obj,"comments":comment})
        else:
            bidders = Bid.objects.filter(product = obj)
            highest_bidding = obj.product_price
            for bidder in bidders:
                if bidder.bidding_price > highest_bidding:
                    highest_bidding = bidder.bidding_price
            if highest_bidding != obj.product_price:
                winner = Bid.objects.get(bidding_price = highest_bidding)
                return render(request, "auctions/list_page.html",{"object":obj,"sold":True,"winner":winner,"comments":comment})
            else:
                return render(request, "auctions/list_page.html",{"object":obj,"sold":True,"comments":comment})



    else:
        return HttpResponse('PAGE NOT FOUND!!!!!!!')

@login_required
def watchlist(request,product_id):
    obj = Product.objects.filter(user = request.user)
    object = get_object_or_404(Product, pk = product_id)
    for o in obj:
        if o.id == product_id:
            return render(request,"auctions/list_page.html",{"object":object,"own1":True,"closing":True})
    wl = Watchlist.objects.filter(user = request.user)
    for w in wl:
        if w.product.id == product_id:
            return render(request,"auctions/list_page.html",{"object":object,"already1":True})
    watchlist,created = Watchlist.objects.get_or_create(product = object,user = request.user)   
    watchlist.save()
    return render(request,"auctions/list_page.html",{"object":object,"added1":True})

@login_required
def viewWatchlist(request):
    obj = Watchlist.objects.filter(user = request.user)
    length = len(obj)
    # pr_ids = []
    # for o in obj:
    #     pr_ids.append(o.product.id)
    # objects = Product.objects.filter(id__in=obj.id)
    return render(request, "auctions/watchlist.html",{"objects":obj,"length":length})

@login_required        
def removeWatchlist(request,product_id):
    obj = Watchlist.objects.filter(id = product_id).delete()
    print(obj)
    return redirect("viewWatchlist")

@login_required
def bidPrice(request, product_id):
    obj = Product.objects.filter(user = request.user)
    object = get_object_or_404(Product, pk = product_id)
    price = request.POST.get("bidPrice")
    for o in obj:
        if o.id == product_id:
            return render(request,"auctions/list_page.html",{"object":object,"own":True,"closing":True})
    bl = Bid.objects.filter(user = request.user)

    for b in bl:
        if b.product.id == product_id:
            bidlist = Bid.objects.filter(product = object,user = request.user).delete()
    bid = Bid.objects.filter(product = object)
    maximum = 0
    if len(bid) != 0:
        for b in bid:
            if b.bidding_price > maximum:
                maximum = b.bidding_price
    if len(bid) == 0:
        if Decimal(price) <= object.product_price:
            # return HttpResponse("Cannot bid price less than actual price")
            return render(request,"auctions/list_page.html",{"object":object,"alert":True})
    else:
        if Decimal(price) <= maximum:
            return render(request,"auctions/list_page.html",{"object":object,"alert2":True})


    bidlist,created = Bid.objects.get_or_create(product = object,user = request.user,bidding_price = price)   
    bidlist.save()
    return render(request,"auctions/list_page.html",{"object":object,"added":True})

@login_required
def closeBid(request, product_id):
    obj = get_object_or_404(Product,pk = product_id, user = request.user)
    if request.method == "POST":
        obj.dateCompleted = timezone.now()
        obj.save()
        return redirect("active_listings")

def closed_listings(request):
    obj = Product.objects.filter(dateCompleted__isnull = False)
    length = len(obj)
    return render(request,"auctions/closed_listings.html",{"objects":obj,"length":length})

def categories(request,category_id):
    if category_id == 1:
        obj = Product.objects.filter(dateCompleted__isnull = True, category = 'kids')
        print(len(obj))
    if category_id == 2:
        obj = Product.objects.filter(dateCompleted__isnull = True, category = 'women')
    if category_id == 3:
        obj = Product.objects.filter(dateCompleted__isnull = True,category = 'electronics')
        print(len(obj))
    if category_id == 4:
        obj = Product.objects.filter(dateCompleted__isnull = True, category = 'groceries')
    if category_id == 5:
        obj = Product.objects.filter(dateCompleted__isnull = True, category = 'other')
    return render(request, "auctions/category.html",{"objects":obj,"length":len(obj)})

@login_required
def comments(request,product_id):
    object = get_object_or_404(Product, pk = product_id)
    description = request.POST.get("comment")
    cl = Comment.objects.filter(user = request.user)
    for c in cl:
        if c.product.id == product_id:
            commentList = Comment.objects.filter(product = object,user = request.user).delete()
            
    commentList = Comment.objects.create(product = object,user = request.user,comment = description)
    commentList.save()
    return redirect('listpage',product_id = product_id)
    


    



