from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import os
from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
import assemblyai as aai
import openai
import google.generativeai as genai
from .models import Post


# Create your views here.
@login_required(login_url="/login")
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data["link"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({ 'error': 'Invalid data sent' }, status=400)
        
        # get yt title
        title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({ 'error': 'Failed to get transcription' }, status=500)
        
        # use Gemini to generate Blog
        blog_content = generate_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({ 'error': 'Failed to generate blog content' }, status=500)
        
        # save blog in database
        new_blog_article = Post.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content
        )

        new_blog_article.save()

        # return blog article as a response
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({ 'error': 'Invalid request method' }, status=405)
    
def yt_title(link):
    yt = YouTube(link)
    return yt.title

def download_audio(link):
    yt = YouTube(link, on_progress_callback = on_progress)
    print(yt.title)
 
    ys = yt.streams.get_audio_only()
    out_file = ys.download(mp3=True, output_path=settings.MEDIA_ROOT)
    return out_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    #aai.settings.api_key = "56e501049ede46c188fbfaee8c01db66"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text

def generate_blog_from_transcript(transcription):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    #genai.configure(api_key="AIzaSyDYO0pXXn9ouRfpcXOAu7h7q_w6xs7lD74")

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(f"Write a blog article from the following transcript\n\n{transcription}\n\nBlog should not exceed 1000 words.")
    #print(response.text)
    return response.text

def post_list(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'post-list.html', { 'posts': posts })

def post_details(request, id):
    post = Post.objects.get(id = id)
    if request.user == post.user:
        return render(request, 'post-details.html', { 'post': post })
    else:
        return redirect('/')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            errorMsg = "Invalid username or password"
            return render(request, 'login.html', { 'errorMsg': errorMsg })
    return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpwd = request.POST["cpwd"]

        if password == cpwd:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                errorMsg = "Error in creating account"
                return render(request, 'signup.html', { 'errorMsg': errorMsg })
        else:
            errorMsg = "Password didn't match"
            return render(request, 'signup.html', { 'errorMsg': errorMsg })
        
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')