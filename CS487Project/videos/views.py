from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from videos.models import Video
from django.db.models import Count
import string
import re

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

class VideoView(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video

class UploaderView(generic.TemplateView):
	template_name = 'videos/upload.html'
	model = Video

        @method_decorator(permission_required('videos.add_video'))
        def dispatch(self, *args, **kwargs):
                return super(UploaderView, self).dispatch(*args, **kwargs)

class VideoUploadForm(forms.Form):
	title = forms.CharField(max_length=100)
	authors = forms.CharField()
	url = forms.URLField()
	journal = forms.CharField()
	keywords = forms.CharField()
	video = forms.FileField()

def videoCount(request, pk):
        video = get_object_or_404(Video, pk=pk)
        video.viewCount += 1
        video.save()
        return HttpResponse(status=200)

def searchResult(request):
        results = Video.objects
        context = {}
        if 'query' in request.GET and request.GET['query']:
                q = request.GET['query']
                context['query'] = q
		qlist = unicode.split(q)
		r = None
		for query in qlist:
			print query
			if r is None:
				r = results.filter(keywords__keyword=query)
			else:
				r = r | results.filter(keywords__keyword=query)
		results = r.annotate(matches=Count('keywords')).order_by('-matches')

	if 'jquery' in request.GET and request.GET['jquery']:
                context['jquery'] = request.GET['jquery']
		results = results.filter(journal__name=request.GET['jquery'])

	if 'aquery' in request.GET and request.GET['aquery']:
                context['aquery'] = request.GET['aquery']
		results = results.filter(authors__name=request.GET['aquery'])

        if context != {}:
                context['results'] = results
        return render(request, 'videos/search.html', context)

@permission_required('videos.add_video')
def uploadFile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			title = form.cleaned_data['title']
			regex = re.compile(',')
			authors = regex.split(form.cleaned_data['authors'])
			journal = form.cleaned_data['journal']
			keywords = regex.split(form.cleaned_data['keywords'])
			url = form.cleaned_data['url']
			video = form.cleaned_data[video]
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', {'form': form})
