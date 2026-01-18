from django.shortcuts import render, redirect
from .models import UserModel, JournalEntry
from django.contrib import messages

# Home page
def home(request):
    return render(request, 'frontpage.html')

from django.db import IntegrityError

def user_register(request):
    if request.method == "POST":
        try:
            user = UserModel(
                name=request.POST.get('name'),
                password=request.POST.get('password'),
                email=request.POST.get('email'),
                age=request.POST.get('age'),
                phone=request.POST.get('phone')
            )
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Email already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            
    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = UserModel.objects.filter(name=username).first()
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                return redirect('projectpart2')  # Redirect to your page
            else:
                messages.error(request, "Invalid username or password")
        except UserModel.DoesNotExist:
            messages.error(request, "Invalid username or password")
        return redirect('login')
    return render(request, 'login.html')


def user_logout(request):
    request.session.flush()
    return redirect('login')

def projectpart2_view(request):
    return render(request, 'projectpart2.html')


def pdashboard_view(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Fetch user's journal entries
    entries = JournalEntry.objects.filter(user_id=user_id).order_by('-created_at')
    
    selected_mood = request.GET.get("mood", None)
    return render(request, 'pdashboard.html', {"mood": selected_mood, "entries": entries})

def add_journal_entry(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        mood = request.POST.get('mood')
        
        JournalEntry.objects.create(
            user_id=user_id,
            title=title,
            content=content,
            mood=mood
        )
        messages.success(request, "Journal entry added successfully!")
        return redirect('pdashboard')
    return redirect('pdashboard')

def wellness_hub_view(request):
    return render(request, 'wellness_hub.html')

def connect_doctor_view(request):
    return render(request, 'connect_doctor.html')

