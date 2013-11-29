from django.forms import ModelForm, TextInput
from models import *

class VideoUploadForm(ModelForm):
	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'journal', 'video')
                widgets = {
                        #'keywords': TextInput
                }

class FlagCommentForm(ModelForm):
    class Meta:
        model = FlagComment
        fields = ('description', )

class FlagVideoForm(ModelForm):
    class Meta:
        model = FlagVideo
        fields = ('description', )

class LeaveCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class BeakerRatingForm(ModelForm):
    class Meta:
        model = BeakerRating
        fields = ('rating',)

class StarRatingForm(ModelForm):
    class Meta:
        model = StarRating
        fields = ('rating',)
