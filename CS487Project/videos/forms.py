from django.db.models import Q
from django.forms import *
from models import *

class MultiKeywordField(CharField):
    def __init__(self, sep_char=None):
        super(MultiKeywordField, self).__init__()
        self.sep_char = sep_char

    def prepare_value(self, value):
        if isinstance(value, unicode):
            return value
        elif value == None:
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
        if isinstance(value, unicode):
            return value
        elif value == None:
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

        journal_name = CharField(max_length=100)
        journal_year = IntegerField(min_value=0)
        journal_edition = IntegerField(min_value=0)

        def save(self, commit=True):
            obj = super(VideoUploadForm, self).save(commit=False)
            obj.journal = Journal.objects.get_or_create(name=self.cleaned_data['journal_name'], year=self.cleaned_data['journal_year'], edition=self.cleaned_data['journal_edition'])[0]
            if commit:
                obj.save()
                self.save_m2m()
            return obj                

	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'video')

class FlagCommentForm(ModelForm):
    class Meta:
        model = FlagComment
        fields = ('description', )

class FlagVideoForm(ModelForm):
    class Meta:
        model = FlagVideo
        fields = ('description', )

class BeakerRatingForm(ModelForm):
    class Meta:
        model = BeakerRating
        fields = ('rating',)

class StarRatingForm(ModelForm):
    class Meta:
        model = StarRating
        fields = ('rating',)
