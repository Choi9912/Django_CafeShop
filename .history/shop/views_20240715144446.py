from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Product,  Order, Category, Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import OrderForm, ProductForm
# Create your views here.



def index(request):
    products = Product.objects.order_by('-pub_date')
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}

    return render(request, 'shop/index.html', context)




def order_list(request, pk):
    categories = Category.objects.all()
    user = User.objects.get(pk=pk)
    orders = Order.objects.filter(user=user)
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'user': user, 'orders': orders, 'categories': categories}
    return render(request, 'shop/order_list.html', context)


def show_category(request, category_id):
    categories = Category.objects.all()
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category).order_by('pub_date')
    lank_products = Product.objects.filter(category=category).order_by('-hit')[:4]
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'lank_products': lank_products, 'products': products, 'category': category, 'categories': categories}
    return render(request, 'shop/category.html', context)



def product_detail(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(pk=pk)
    category = Category.objects.get(pk=product.category.pk)
    Product.objects.filter(pk=pk).update(hit=product.hit+1)
    point = int(product.price * 0.01)
    quantity_list = []
    for i in range(1, product.quantity) :
        quantity_list.append(i)
    context = {"quantity_list": quantity_list, "product": product, "point": point, "category": category, "categories": categories}
    return render(request, 'shop/product_detail.html', context)


def cart(request, pk):
    categories = Category.objects.all()
    user = User.objects.get(pk=pk)
    cart = Cart.objects.filter(user=user)
    paginator = Paginator(cart, 10)
    page = request.GET.get('page')
    try:
        cart = paginator.page(page)
    except PageNotAnInteger:
        cart = paginator.page(1)
    except EmptyPage:
        cart = paginator.page(paginator.num_pages)
    context = {'user': user, 'cart': cart, 'categories': categories}
    return render(request, 'shop/cart.html', context)

def delete_cart(request, pk):
    user = request.user
    cart = Cart.objects.filter(user=user)
    quantity = 0

    if request.method == 'POST':
        pk = int(request.POST.get('product'))
        product = Product.objects.get(pk=pk)
        for i in cart:
            if i.products == product :
                quantity =  i.quantity

        if quantity > 0 :
            product = Product.objects.filter(pk=pk)
            cart = Cart.objects.filter(user=user, products__in=product)
            cart.delete()
            return redirect('shop:cart', user.pk)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Product, Order, Category, Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import OrderForm, ProductForm

# Other view functions...

@login_required
def cart_action(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.method == "POST":
        selected_products = request.POST.getlist('products')
        action = request.POST.get('action')
        
        if action == 'delete':
            # Handle deletion of selected products from cart
            Cart.objects.filter(user=user, products__id__in=selected_products).delete()
            messages.success(request, 'Selected items have been deleted from your cart.')
            return redirect('shop:cart', user.pk)
        
        elif action == 'checkout':
            # Redirect to checkout page with selected products
            selected_products_str = ','.join(selected_products)
            return redirect(f"{reverse('shop:checkout')}?products={selected_products_str}")

    return redirect('shop:cart', user.pk)

@login_required
def checkout(request):
    user = request.user
    categories = Category.objects.all()
    products_ids = request.GET.get('products', '').split(',')
    products = Product.objects.filter(id__in=products_ids)
    
    # Calculate total price
    total_price = sum(product.price for product in products)

    if request.method == "POST":
        # Handle order form submission here
        form = OrderForm(request.POST)
        if form.is_valid():
            for product in products:
                order = form.save(commit=False)
                order.user = user
                order.products = product
                order.save()
            messages.success(request, 'Order placed successfully.')
            return redirect('shop:order_list', user.pk)
    
    else:
        form = OrderForm(initial={'amount': total_price})

    return render(request, 'shop/checkout.html', {
        'form': form,
        'products': products,
        'total_price': total_price,
        'categories': categories,
    })

@login_required
def cart_or_buy(request, pk):
    quantity = int(request.POST.get('quantity'))
    product = Product.objects.get(pk=pk)
    user = request.user
    categories = Category.objects.all()
    initial = {'name': product.name, 'amount': product.price, 'quantity': quantity}
    cart = Cart.objects.filter(user=user)
    if request.method == 'POST':
        if 'add_cart' in request.POST:
            for i in cart :
                if i.products == product:
                    product = Product.objects.filter(pk=pk)
                    Cart.objects.filter(user=user, products__in=product).update(quantity=F('quantity') + quantity)
                    messages.success(request,'장바구니 등록 완료')
                    return redirect('shop:cart', user.pk)

            Cart.objects.create(user=user, products=product, quantity=quantity)
            messages.success(request, '장바구니 등록 완료')
            return redirect('shop:cart', user.pk)

        elif 'buy' in request.POST:
            form = OrderForm(request.POST, initial=initial)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = user
                order.quantity = quantity
                order.products = product
                order.save()
                return redirect('shop:order_list', user.pk)

            else:
                form = OrderForm(initial=initial)

            return render(request, 'shop/order_pay.html', {
                'form': form,
                'quantity': quantity,
                'iamport_shop_id': 'iamport',  # FIXME: 가맹점코드
                'user': user,
                'product': product,
                'categories': categories,
            })