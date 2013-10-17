from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.views import generic
from videos.models import Video
from django.db.models import Count
from django.forms import ModelForm
from django.template import RequestContext
import string
import re
import datetime

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

class VideoView(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video

class VideoUploadForm(ModelForm):
	class Meta:
		model = Video
		fields = ('title', 'description', 'url', 'authors', 'keywords', 'journal', 'video')

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
		form = VideoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			f = form.save(commit=False)
                        f.uploader = request.user
                        f.save()
			return render(request, 'videos/upload_success.html')
	else:
		form = VideoUploadForm()
	return render_to_response('videos/upload.html', {'form': form}, context_instance=RequestContext(request))
