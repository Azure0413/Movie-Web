from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from myapp.forms import LoginForm, MovieForm
from myapp.models import CustomUser, Movie, Rating
from django.contrib import messages
from django.utils import timezone

def index_page(request):
    search_query = request.GET.get('search', '')
    movies = Movie.objects.filter(movie_name__icontains=search_query)
    users = CustomUser.objects.all()
    ratings = Rating.objects.all()

    context = {
        'movies': movies,
        'users': users,
        'ratings': ratings
    }
    
    return render(request, 'index.html', context)

def add_view(request):
    return render(request, 'add.html')

def insert_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_page')
    else:
        form = MovieForm()
    return render(request, 'add.html', {'form': form})

def update_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_name = request.POST.get('movie_name')
        movie_description = request.POST.get('description')
        movie_image = request.FILES.get('image')
        
        print(f"ID: {movie_id}, Name: {movie_name}, Description: {movie_description}, Image: {movie_image}")
        
        if movie_id and movie_name and movie_description:
            movie = get_object_or_404(Movie, id=movie_id)
            movie.movie_name = movie_name
            movie.description = movie_description
            if movie_image:
                movie.image = movie_image
            
            movie.save()
            return redirect('index_page')

    return render(request, 'add.html')

def delete_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = get_object_or_404(Movie, id=movie_id)
            ratings = Rating.objects.filter(movie=movie)
            ratings.delete()
            movie.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def insert_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_age = request.POST.get('user_age')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if username and password and user_age:
            CustomUser.objects.create(
                username=username,
                password=make_password(password),
                user_age=user_age,
                is_admin=is_admin
            )
            return redirect('index_page')
    return render(request, 'add.html')

def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_age = request.POST.get('user_age')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if user_id and username and user_age:
            user = get_object_or_404(CustomUser, id=user_id)
            user.username = username
            
            if password:
                user.password = make_password(password)
            user.user_age = user_age
            user.is_admin = is_admin
            user.save()
            return redirect('index_page')
    return render(request, 'add.html')

def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, id=user_id)
            ratings = Rating.objects.filter(user=user)
            ratings.delete()
            user.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def insert_rating(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        
        if user_id and movie_id and rating_value:
            user = get_object_or_404(CustomUser, id=user_id)
            movie = get_object_or_404(Movie, id=movie_id)
            Rating.objects.create(
                user=user,
                movie=movie,
                rating=rating_value
            )
            return redirect('index_page')
    return render(request, 'add.html')

def insert_ratings(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        
        if user_id and movie_id and rating_value:
            user = get_object_or_404(CustomUser, id=user_id)
            movie = get_object_or_404(Movie, id=movie_id)
            existing_rating = Rating.objects.filter(user=user, movie=movie).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.save()
                messages.success(request, "Your rating has been updated.")
            else:
                Rating.objects.create(
                    user=user,
                    movie=movie,
                    rating=rating_value
                )
                messages.success(request, "Your rating has been added.")
            return redirect('page')
    return render(request, 'add.html')


def update_rating(request):
    if request.method == 'POST':
        rating_id = request.POST.get('rating_id')
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        
        if rating_id and user_id and movie_id and rating_value:
            rating = get_object_or_404(Rating, id=rating_id)
            user = get_object_or_404(CustomUser, id=user_id)
            movie = get_object_or_404(Movie, id=movie_id)
            rating.user = user
            rating.movie = movie
            rating.rating = rating_value
            rating.save()
            return redirect('index_page')
    return render(request, 'add.html')

def delete_rating(request):
    if request.method == 'POST':
        rating_id = request.POST.get('rating_id')
        if rating_id:
            rating = get_object_or_404(Rating, id=rating_id)
            rating.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def page(request):
    search_query = request.GET.get('search', '')
    movies = Movie.objects.filter(movie_name__icontains=search_query)
    users = CustomUser.objects.all()
    ratings = Rating.objects.all().order_by('-rating') 

    context = {
        'movies': movies,
        'users': users,
        'ratings': ratings
    }
    
    return render(request, 'main.html', context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if username == 'admin':
                    return redirect("index_page")
                else:
                    return redirect("page")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def register(request):
    registration_successful = False
    if request.method == 'POST':
        username = request.POST.get('username')
        user_age = request.POST.get('user_age')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_admin = (username == 'admin')
        
        if not (username and password1 and password2 and user_age):
            messages.error(request, "Please fill all the data!")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif password1 != password2:
            messages.error(request, "Passwords do not match!")
        else:
            CustomUser.objects.create(
                username=username,
                password=make_password(password1),
                user_age=user_age,
                is_admin=is_admin,
                last_login=timezone.now()
            )
            registration_successful = True
            messages.success(request, "Registration successful!")

    return render(request, 'register.html', {'registration_successful': registration_successful})