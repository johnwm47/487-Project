from django.forms import ModelForm, TextInput
from models import Video, Comment

class VideoUploadForm(ModelForm):
	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'journal', 'video')
                widgets = {
                        #'keywords': TextInput
                }

class LeaveCommentForm(ModelForm):
        class Meta:
                model = Comment
                fields = ('content', )
