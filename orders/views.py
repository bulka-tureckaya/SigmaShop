from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import send_created
from django.urls import reverse
from django.shortcuts import render, redirect

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        print(form.data)
        if form.is_valid():
            order = form.save(commit=False)
            
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            send_created(order, form)
            request.session['order_id'] = order.id
            return redirect(reverse('payments:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})

