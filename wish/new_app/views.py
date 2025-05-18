from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'users.html')

def add_user(request):
    if request.method != 'POST':
        return redirect('/users')
    errors = User.objects.user_validator(request.POST)
    if errors:
        for v in errors.values():
            messages.error(request, v)
        return redirect('/users')
    fn = request.POST['first_name']
    ln = request.POST['last_name']
    em = request.POST['email']
    bd = request.POST['birthday']
    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=fn, last_name=ln, email=em, birthday=bd, password=hash_pw)
    logged_in_user = User.objects.last()
    request.session['user_id'] = logged_in_user.id
    request.session['first_name'] = logged_in_user.first_name
    request.session['last_name'] = logged_in_user.last_name
    return redirect('/wishes')


def user_login(request):
    if request.method != 'POST':
        return redirect('/users')
    errors = User.objects.login_validator(request.POST)
    if errors:
        for v in errors.values():
            messages.error(request, v)
        return redirect('/users')
    user = User.objects.filter(email=request.POST['email']).first()
    request.session['user_id'] = user.id
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    return redirect('/wishes')

def user_logout(request):
    request.session.flush()
    return redirect('/')

def user_edit(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    if not user:
        return redirect('/')
    context = {
        'user': user[0]
    }
    return render(request, 'edit_user.html', context)

def user_update(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    if not user:
        return redirect('/')
    errors = User.objects.update_validator(request.POST)
    if errors:
        for v in errors.values():
            messages.error(request, v)
        return redirect(f'/users/{user[0].id}/dashboard')
    if request.method != 'POST':
        return redirect(f'/users/{user[0].id}/dashboard')
    if request.session['user_id'] == user[0].id:
        user[0].first_name = request.POST['first_name']
        user[0].last_name = request.POST['last_name']
        user[0].email = request.POST['email']
        user[0].birthday = request.POST['birthday']
        if request.POST['password'] == '':
            user[0].save()
            return redirect(f'/users/{user[0].id}/dashboard')
        else:
            password = request.POST['password']
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user[0].password = hash_pw
            user[0].save()
            return redirect(f'/users/{id}/dashboard')

def dashboard(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=id) 
    context = {
        'user': user,
    }
    return render(request,'dashboard.html', context)

def wishes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'wish_list': Wish.objects.all(),
    }
    return render(request, 'wishes.html', context)

def new_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'add_wish.html')

def add_wish(request):
    errors = Wish.objects.basic_validator(request.POST)
    if errors:
        for v in errors.values():
            messages.error(request, v)
        return redirect('/wishes/add')
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    user = User.objects.filter(id=request.session['user_id']).first()
    if not user:
        return redirect('/')
    i = request.POST['item']
    d = request.POST['description']
    Wish.objects.create(item=i, description=d, is_granted=0, wisher_id=user.id)
    return redirect('/wishes')

def wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        wish = Wish.objects.filter(id=request.POST['wish_id'])
        if len(wish) != 1:
            return redirect('/wishes')
        request.session['wish_id'] = wish[0].id
    context = {
        'wish': wish[0],
    }
    return render(request, 'wish.html', context)

def update_wish(request):
    wish_id = request.session['wish_id']
    wish = Wish.objects.filter(id=wish_id)
    if len(wish) != 1:
        return redirect('/wishes')
    errors = Wish.objects.basic_validator(request.POST)
    if errors:
        for v in errors.values():
            messages.error(request, v)
        return redirect('/wishes')
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        if request.session['user_id'] == wish[0].wisher_id:
            wish = Wish.objects.get(id=wish_id)
            print(wish.item)
            print(request.POST['item'])
            wish.item = request.POST['item']
            print(wish.item)
            wish.description = request.POST['description']
            wish.save()
            return redirect('/wishes')
        return redirect('/wishes')

def delete_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        wish = Wish.objects.filter(id=request.POST['wish_id'])
        if len(wish) != 1:
            return redirect('/wishes')
        wish.delete()
        return redirect('/wishes')

def granted_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        wish = Wish.objects.filter(id=request.POST['wish_id'])
        if len(wish) != 1:
            return redirect('/wishes')
        wish[0].is_granted = 1
        wish[0].save()
        wish[0].granter.add(request.session['user_id'])
        return redirect('/wishes')

def like_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    if not user:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        wish = Wish.objects.filter(id=request.POST['wish_id'])
        if len(wish) != 1:
            return redirect('/wishes')
        wish[0].likers.add(user[0])
        return redirect('/wishes')

def unlike_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    if not user:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/wishes')
    else:
        wish = Wish.objects.filter(id=request.POST['wish_id'])
        if len(wish) != 1:
            return redirect('/wishes')
        wish[0].likers.remove(user[0])
        return redirect('/wishes')

def stat(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': user[0],
        'granted_wishes': Wish.objects.filter(is_granted=1),
        'user_granted_list': Wish.objects.filter(is_granted=1, wisher_id=user[0].id),
        'user_pending_list': Wish.objects.filter(is_granted=0, wisher_id=user[0].id),
        'all_wishes': Wish.objects.all()
    }
    return render(request, 'stat.html', context)