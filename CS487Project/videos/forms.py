from django.forms import ModelForm, TextInput
from models import Video, Comment, Flag

class VideoUploadForm(ModelForm):
	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'journal', 'video')
                widgets = {
                        #'keywords': TextInput
                }

class FlagCreationForm(ModelForm):
    class Meta:
        model = Flag
        fields = ('description', )

class LeaveCommentForm(ModelForm):
        class Meta:
                model = Comment
                fields = ('content', )
