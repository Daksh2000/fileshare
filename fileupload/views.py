# fileupload/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import FileUploadForm
from django.http import HttpResponse
import os
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'fileupload/register.html', {'form': form})


@login_required
def home_view(request):
    # Fetch the files uploaded by the logged-in user
    user_files = File.objects.filter(uploaded_by=request.user)

    return render(request, 'fileupload/home.html', {
        'user_files': user_files
    })


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.uploaded_by_id = request.user.pk
            file_instance.save()
            # Optionally compress and set file type here
            return redirect('file-list')
    else:
        form = FileUploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})

@login_required
def file_list(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'fileupload/file_list.html', {'files': files})

@login_required
def delete_file(request, pk):
    file = File.objects.get(pk=pk)
    if file.user == request.user:
        file.delete()
        return redirect('file-list')
    else:
        return HttpResponse("Unauthorized", status=401)


@login_required
def share_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    if file.user == request.user:
        file.generate_public_url()
        return redirect('file-list')
    return HttpResponse("Unauthorized", status=401)

def public_file(request, public_url):
    file = get_object_or_404(File, public_url=public_url)
    return render(request, 'fileupload/public_file.html', {'file': file})