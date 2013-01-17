from django.contrib import admin

from fakebook.models import User
from fakebook.models import Photo

class CommentsInline(admin.TabularInline):
	model = Photo.comments.through

class VotesInline(admin.TabularInline):
	model = Photo.votes.through

class PhotoAdmin(admin.ModelAdmin):
	inlines = [CommentsInline, VotesInline]

admin.site.register(Photo, PhotoAdmin)
