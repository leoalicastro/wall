from django.shortcuts import render, redirect 
from .models import User, Message, Comment
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpassword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(request.POST['password'])
        print(hashedpassword)
        new_user = User.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = hashedpassword
        )
        request.session['user_id'] = new_user.id
        return redirect('/wall')
    
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            user = User.objects.get(username = request.POST['logusername'])
            request.session['user_id'] = user.id
            return redirect('/wall')
    else:
        return redirect('/')

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "users": user,
        "messages": Message.objects.all().order_by('-created_at'),
        "comments": Comment.objects.all(),
        "this_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'wall.html', context)

def message(request):
    if request.method=="POST":
        message = Message.objects.create(
            new_message = request.POST['new_message'],
            poster = User.objects.get(id=request.session['user_id'])
        )
    return redirect('/wall')

def comment(request, message_id):
    poster_comment = User.objects.get(id=request.session['user_id'])
    message_comment = Message.objects.get(id=message_id)
    Comment.objects.create(
        new_comment=request.POST['new_comment'],
        poster_comment=poster_comment,
        message_comment=message_comment
    )
    return redirect('/wall')

def delete(request, message_id):
    delete = Message.objects.get(id=message_id)
    delete.delete()
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')
# Create your views here.
