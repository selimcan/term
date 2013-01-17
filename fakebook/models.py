from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

class Photo(models.Model):
	thumbnail = models.FileField(upload_to='photos')
	original_path = models.URLField(max_length=200, primary_key=True)
	uploadedBy = models.ForeignKey(User, related_name='photo_uploadedBy')
	uploadDate = models.DateField(default=datetime.now)
	comments = models.ManyToManyField(User, through='Comment', related_name='photo_comments', blank=True, null=True)
	votes = models.ManyToManyField(User, through='Vote', related_name='photo_votes', blank=True, null=True)
	
	def numberOfDislikes(self):
		return Vote.objects.filter(photo=self.original_path, likes=False).count()
	
	def numberOfLikes(self):
		return Vote.objects.filter(photo=self.original_path, likes=True).count()
		
	def getComments(self):
		return Comment.objects.filter(photo=self.original_path).order_by('date').all()
		
	def __unicode__(self):
		return u'%s by %s' % (self.thumbnail, self.uploadedBy)
		
class PhotoForm(ModelForm):
	class Meta:
		model = Photo
		fields = ('thumbnail', 'original_path')

class Comment(models.Model):
	username = models.ForeignKey(User, related_name='comments_username')
	photo = models.ForeignKey('Photo', related_name='comments_photo')
	comment = models.CharField(max_length=256)
	date = models.DateField()
	
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('comment', )

class Vote(models.Model):
	username = models.ForeignKey(User, related_name='votes_username')
	photo = models.ForeignKey('Photo', related_name='votes_photo')
	likes = models.BooleanField()

	class Meta:
		unique_together = (("username", "photo"),)
