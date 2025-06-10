from django.shortcuts import render,redirect
from .forms import ImageUploadForm, VideoUploadForm
from .models import UploadedImage, UploadedVideo,User
from .cnn_model import compare_images
from .video_processing import extract_frames
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from .models import User
from functools import wraps

# Custom login required decorator
def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')  # Redirect to login if not authenticated
        return view_func(request, *args, **kwargs)
    return wrapper

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        User.objects.create(username=username, password=password)  # Store plain password
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')

    return render(request, 'app/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id  # Store session
            return redirect('upload_reference')
        except User.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, 'app/login.html')

def logout(request):
    auth_logout(request)  # Log out user
    request.session.flush()
    return redirect('login')



@login_required_custom
def upload_reference(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            UploadedImage.objects.all().delete()  # Store only one reference
            form.save()
            # return render(request, "app/upload.html", {"form": form, "message": "Reference Image Uploaded!"})
            return redirect(choose)
        
    else:
        form = ImageUploadForm()
    return render(request, "app/upload.html", {"form": form})

@login_required_custom
def upload_check_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            ref_image = UploadedImage.objects.first()  # Reference image
            if ref_image:
                similarity = compare_images(ref_image.image.path, new_image.image.path)
                result = "Match" if similarity > 0.6 else "Not a Match"
                return render(request, "app/result.html", {"result": result, "similarity": similarity})
    else:
        form = ImageUploadForm()
    return render(request, "app/check.html", {"form": form})

@login_required_custom
def upload_check_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save()
            ref_image = UploadedImage.objects.first()

            if ref_image:
                output_folder = "media/video_frames"
                frames = extract_frames(new_video.video.path, output_folder)

                best_similarity = 0
                for frame in frames:
                    similarity = compare_images(ref_image.image.path, frame)
                    best_similarity = max(best_similarity, similarity)

                result = "Match" if best_similarity > 0.6 else "Not a Match"
                return render(request, "app/result.html", {"result": result, "similarity": best_similarity})
    else:
        form = VideoUploadForm()
    return render(request, "app/videoupload.html", {"form": form})


@login_required_custom
def choose(request):
    return render(request,"chooose.html")
