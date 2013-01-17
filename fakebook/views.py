# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from datetime import datetime

from fakebook import models

def index(request):
	photos = models.Photo.objects.order_by('-uploadDate')[:15];
	photoForm = models.PhotoForm()
	commentForm = models.CommentForm()
	context = {'photos': photos, 'photoForm': photoForm, 'commentForm': commentForm}
	return render(request, 'index.html', context)

def user(request, username):
	photos = models.Photo.objects.filter(uploadedBy=User.objects.get(username=username)).order_by('-uploadDate');
	user = User.objects.get(username=username)
	
#	photos = Photo.objects.filter(comments__comments_username=User.objects.get(username=username))
	photoForm = models.PhotoForm()
	commentForm = models.CommentForm()
	context = {'photos': photos,'photoForm': photoForm, 'commentForm': commentForm, 'username': username, 'last_name': user.last_name}
	return render(request, 'user.html', context)
	
def comments(request, username):
#	photos = models.Photo.objects.filter(uploadedBy=User.objects.get(username=username)).order_by('-uploadDate');
	photos = models.Photo.objects.filter(comments__comments_username=User.objects.get(username=username)).order_by('-uploadDate').distinct()
	photoForm = models.PhotoForm()
	commentForm = models.CommentForm()
	context = {'photos': photos,'photoForm': photoForm, 'commentForm': commentForm, 'username': username}
	return render(request, 'comments.html', context)


def photo(request, photo):
	photo = models.Photo.objects.get(original_path__exact=photo);
	context = {'photo': photo}
	return render(request, 'photo.html', context)

#def comment(request, photo):
#	photo = get_object_or_404(models.Photo, original_path=photo)
#	now = datetime.now()
#	if request.user.is_authenticated():
#		models.Comment.objects.create(username=request.user, photo=photo, comment=request.POST['comment'], date=now)
#		html = "<html><head><title>Success</title></head><body><script>alert('Comment sent successfully.'); window.close();</script>"
#		return HttpResponse(html)
#	else:
#		return HttpResponse('not logged in')

def comment(request, photo):
	if request.method == 'POST':
		photo = get_object_or_404(models.Photo, original_path=photo)
		now = datetime.now()
		comment = models.Comment(username=request.user, photo=photo, date=now)
		form = models.CommentForm(request.POST, request.FILES, instance=comment)
		
		if request.user.is_authenticated():
			if form.is_valid():
				form.save()
				html = "<html><head><title>Success</title></head><body><script>alert('Comment sent successfully.'); window.close();</script>"
				return HttpResponse(html)
			else:
				html = "<html><head><title>Success</title></head><body><script>alert('You can't send an empty comment.'); window.close();</script>"
				return HttpResponse(html)
		else:
			return HttpResponse('not logged in')
			
		
def upload(request):
	if request.method == 'POST':
		now = datetime.now()
		photo = models.Photo(uploadedBy=request.user, uploadDate=now)
		form = models.PhotoForm(request.POST, request.FILES, instance=photo)
		if form.is_valid():
			form.save()
			html = "<html><head><title>Success</title></head><body><script>alert('The photo is uploaded successfully.'); window.close();</script>"
			return HttpResponse(html)
		else:
			html = "<html><head><title>Success</title></head><body><script>alert('Please upload the thumbnail and paste the original link of the photo.'); window.close();</script>"
			return HttpResponse(html)

		
def vote(request, photo, like):
	photo = get_object_or_404(models.Photo, original_path=photo)
	if request.user.is_authenticated():
		if models.Vote.objects.filter(username=request.user, photo=photo):
			vote = models.Vote.objects.filter(username=request.user, photo=photo)[0]
			vote.likes = like
			vote.save()
			html = "<html><head><title>Success</title></head><body><script>alert('Vote changed successfully.'); window.close();</script>"
		else:
			html = "<html><head><title>Success</title></head><body><script>alert('Vote sent successfully.'); window.close();</script>"
			models.Vote.objects.create(username=request.user, photo=photo, likes=like)
		
		return HttpResponse(html)
	else:
		return HttpResponse('not logged in')
		
def log_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			html = "<html><head><title>Success</title></head><body><script>alert('Logged in successfully.'); window.close();</script>"
			return HttpResponse(html)
		else:
			return HttpResponse('disabled user')
	else:
		return HttpResponse('invalid login')
        
def log_out(request):
    logout(request)
    html = "<html><head><title>Success</title></head><body><script>alert('Logged out successfully.'); window.close();</script>"
    return HttpResponse(html)

		
		