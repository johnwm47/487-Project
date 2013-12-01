from django.db.models import Q
from django.forms import ModelForm, TextInput, CharField
from models import *

class CSField(CharField):
    def to_python(self, value):
        strings = value.split()
        qset = Q()
        for s in strings:
            qset = qset | Q(keyword=s)
        print(Keyword.objects.filter(qset))
        return Keyword.objects.filter(qset)

class VideoUploadForm(ModelForm):
        #keywords = CSField()

	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'journal', 'video')

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
