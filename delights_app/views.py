from django.shortcuts import redirect, render, HttpResponse
from django.apps import apps
User = apps.get_model('login_app', 'User')
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Avg


def home(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    if not 'basket' in request.session:
        request.session['basket'] = 0
    return render(request, 'home.html')

def cupcakes(request): 
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'cupcakes': Catigory.objects.get(id=1),
    }
    return render(request, 'cupcakes.html', context)

def cupcake(request, cupcake_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    cupcake_ratings= Delight.objects.get(id= cupcake_id).delight_ratings.all()
    if not cupcake_ratings:
        round_rate= 0
    else:    
        rate= cupcake_ratings.aggregate(rate= Avg('rating'))
        print(rate)
        x= rate
        y= x['rate']
        round_rate= round(y*2)/2
    context={
        'cupcake': Delight.objects.get(id= cupcake_id),
        'rate': round_rate,
    }
    return render(request, 'cupcake.html', context)

def tarts(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'tarts': Catigory.objects.get(id=2),
    }
    return render(request, 'tarts.html', context)

def tart(request, tart_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    tart_ratings= Delight.objects.get(id= tart_id).delight_ratings.all()
    if not tart_ratings:
        round_rate= 0
    else:    
        rate= tart_ratings.aggregate(rate= Avg('rating'))
        print(rate)
        x= rate
        y= x['rate']
        round_rate= round(y*2)/2
    context={
        'tart': Delight.objects.get(id= tart_id),
        'rate': round_rate,
    }
    return render(request, 'tart.html', context)

def cookies(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'cookies': Catigory.objects.get(id=3),
    }
    return render(request, 'cookies.html', context)

def cookie(request, cookie_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    cookie_ratings= Delight.objects.get(id= cookie_id).delight_ratings.all()
    if not cookie_ratings:
        round_rate= 0
    else:    
        rate= cookie_ratings.aggregate(rate= Avg('rating'))
        print(rate)
        x= rate
        y= x['rate']
        round_rate= round(y*2)/2
    context={
        'cookie': Delight.objects.get(id= cookie_id),
        'rate': round_rate,
    }
    return render(request, 'cookie.html', context)

def all(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'all_delights': Delight.objects.all().order_by('?'),
        'count': Delight.objects.all().count,
    }
    return render(request, 'all.html', context)

def add_delight(request, delight_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    catigory= Delight.objects.get(id= delight_id).catigory.type
    temp_del_oreder= TempDelight.objects.create(temp_delight= Delight.objects.get(id= delight_id), qty= request.POST['qty'])
    request.session['basket'] += int(request.POST['qty'])
    print(temp_del_oreder)
    return redirect(f'/delights/{catigory}/{delight_id}')

def check_out(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    temp_items= TempDelight.objects.all()
    total_price= 0
    for item in temp_items:
        total_price+= item.temp_delight.price * item.qty
    x= total_price
    tax= round(x* 12/100,2)
    price_with_tax= round(x+ tax, 2)
    context={
        'temp_items': TempDelight.objects.all(),
        'tax': tax,
        'final_price': price_with_tax,
    }    
    return render(request, 'Check_out.html', context)

def order(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    temp_items= TempDelight.objects.all()
    if request.session['basket']==0:
        return redirect('/delights')
    total_price= 0
    for item in temp_items:
        total_price+= item.temp_delight.price * item.qty
    x= total_price
    tax= round(x* 12/100,2)
    price_with_tax= round(x+ tax, 2)
    this_order= Order.objects.create(paid_amount= price_with_tax, ordered_by= User.objects.get(id= request.session['user_id']))
    order_id= this_order.id
    for item in temp_items:
        DelightOrder.objects.create(delight= item.temp_delight, quantity= item.qty, order= this_order)
    TempDelight.objects.all().delete()
    request.session['basket']= 0
    return redirect(f'/delights/place_order/{order_id}')

def place_order(request, order_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'order': Order.objects.get(id=order_id)
    }

    return render(request, 'order.html', context)

def user_account(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    context={
        'orders': Order.objects.filter(ordered_by= User.objects.get(id=user_id)),
    }
    return render(request, 'user.html', context)

def update(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user= User.objects.get(id= request.session['user_id'])
    errors = User.objects.update_validator(request.POST, user)
    request.session['send']= "update"
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/delights/{user.id}')
    else:
        if request.POST['first_name'] != "":
            user.first_name = request.POST['first_name']
            request.session['first_name']= request.POST['first_name']
        if request.POST['last_name'] != "":
            user.last_name = request.POST['last_name']
            request.session['last_name']= request.POST['last_name']
        if request.POST['email'] != "" and request.POST['email'] != user.email:
            user.email = request.POST['email']
            request.session['email']= request.POST['email']
        user.save()
        return redirect(f'/delights/{user.id}')

def review(request, delight_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    catigory= Delight.objects.get(id= delight_id).catigory.type
    Review.objects.create(review= request.POST['review'], uploaded_by= User.objects.get(id=request.session['user_id']), review_for= Delight.objects.get(id= delight_id))
    return redirect(f'/delights/{catigory}/{delight_id}')

def rate(request, delight_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    catigory= Delight.objects.get(id= delight_id).catigory.type
    user= User.objects.get(id= request.session['user_id'])
    delight= Delight.objects.get(id= delight_id)
    rated= Rating.objects.filter(rated_by= user).filter(rate_for= delight)
    if rated:
        return redirect(f'/delights/{catigory}/{delight_id}')
    else:  
        Rating.objects.create(rating= request.POST['rate'], rated_by= User.objects.get(id=request.session['user_id']), rate_for= Delight.objects.get(id= delight_id))
        return redirect(f'/delights/{catigory}/{delight_id}')

def edit(request, delight_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    delight= TempDelight.objects.get(id= delight_id)
    x= delight.qty
    delight.qty= request.POST['new_qty']
    delight.save()
    if x > int(request.POST['new_qty']):
        request.session['basket']-= (x-int(request.POST['new_qty']))
    else:
        request.session['basket']+= abs((x-int(request.POST['new_qty'])))
    return redirect('/delights/check_out')
2
def remove(request, delight_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    delight= TempDelight.objects.get(id= delight_id)
    request.session['basket']-= delight.qty
    delight.delete()
    return redirect('/delights/check_out')

def logout(request):
    request.session.clear()
    TempDelight.objects.all().delete()
    return redirect('/')

