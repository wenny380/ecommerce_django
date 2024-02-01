from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request, category_slug=None):
    category_page = None
    products = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page,
                                          available=True)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, 'home.html', {'category':category_page, 'products': products})

def product(request, category_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=category_slug, slug=product_slug) # two '_' allows us to access the variable. category___slug category from product, slug from the class Category 
	except Exception as e:
		raise e
	return render(request, 'product.html', {'product': product})



def _cart_id(request): #create or save session
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #receive the current session. Before adding the product we verify that it wasn't already add
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) #try to get the basket  from  the current session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id= _cart_id(request)) # if doesn't exist we create a new basket
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) #Getthe product from the basket
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1 #increase the quantity of that product in the basket
        cart_item.save()
    except CartItem.DoesNotExist: #if the product it's not in the basket it's mean we are adding it the first time
        cart_item = CartItem.objects.create(product=product, quantity=1, cart = cart) #so quantity initialyze with 1
        cart_item.save()
    
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter ))

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')
