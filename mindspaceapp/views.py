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
            name = request.POST.get('name', '').strip()
            password = request.POST.get('password', '').strip()
            email = request.POST.get('email', '').strip()
            age = request.POST.get('age', '').strip()
            phone = request.POST.get('phone', '').strip()

            user = UserModel(
                name=name,
                password=password,
                email=email,
                age=age,
                phone=phone
            )
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Email already exists.")
        except Exception as e:
            print(f"Register Error: {e}")
            messages.error(request, f"An error occurred: {str(e)}")
            
    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            
            user = UserModel.objects.filter(name=username).first()
            
            if user and user.password == password:
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                return redirect('projectpart2')
            
            messages.error(request, "Invalid username or password")
            return redirect('login')
            
        except Exception as e:
            print(f"Login Error: {e}")
            messages.error(request, "A system error occurred during login. Please try again.")
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


from .models import Doctor, Appointment

def urgent_doctors_view(request):
    # Fetch doctors marked as 'Urgent Care'
    doctors = Doctor.objects.filter(is_urgent_care=True)
    return render(request, 'urgent_doctors.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        
        doctor = Doctor.objects.get(id=doctor_id)
        date_time = request.POST.get('date_time')
        
        Appointment.objects.create(
            user_id=user_id,
            doctor=doctor,
            date_time=date_time
        )
        messages.success(request, f"Appointment confirmed with {doctor.name}!")
        return redirect('pdashboard')
    return redirect('urgent_doctors')

