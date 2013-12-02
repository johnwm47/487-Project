from django.db.models import Q
from django.forms import ModelForm, TextInput, CharField
from models import *

class MultiKeywordField(CharField):
    def __init__(self, sep_char=None):
        super(MultiKeywordField, self).__init__()
        self.sep_char = sep_char

    def prepare_value(self, value):
        if value == None:
            return ""
        elif self.sep_char == None:
            return " ".join(value)
        else:
            return self.sep_char.join(value)

    def to_python(self, value):
        strings = value.split(self.sep_char)
        qset = Q()
        for s in strings:
            t = s.strip()
            Keyword.objects.get_or_create(keyword=t)
            qset = qset | Q(keyword=t)
        return Keyword.objects.filter(qset)

class MultiAuthorField(CharField):
    def __init__(self, sep_char=None):
        super(MultiAuthorField, self).__init__()
        self.sep_char = sep_char

    def prepare_value(self, value):
        if value == None:
            return ""
        else:
            l = [Author.objects.get(pk=v).__unicode__() for v in value]
            if self.sep_char == None:
                return " ".join(l)
            else:
                return self.sep_char.join(l)

    def to_python(self, value):
        strings = value.split(self.sep_char)
        qset = Q()
        for s in strings:
            t = s.strip()
            Author.objects.get_or_create(name=t)
            qset = qset | Q(name=t)
        return Author.objects.filter(qset)

class VideoUploadForm(ModelForm):
        keywords = MultiKeywordField()
        authors = MultiAuthorField(sep_char=",")

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
