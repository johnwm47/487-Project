from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from videos.models import Video
from django.db.models import Count

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

class VideoView(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video

@permission_required('videos.add_video')
def uploaderView(request):
        return render(request, 'videos/upload.html')

class UploaderView(generic.TemplateView):
	template_name = 'videos/upload.html'
	model = Video

        @method_decorator(permission_required('videos.add_video'))
        def dispatch(self, *args, **kwargs):
                return super(UploaderView, self).dispatch(*args, **kwargs)

def videoCount(request, pk):
        video = get_object_or_404(Video, pk=pk)
        video.viewCount += 1
        video.save()
        return HttpResponse(status=200)

def searchResult(request):
        if 'query' in request.GET and request.GET['query']:
                q = request.GET['query']
		qlist = unicode.split(q)
		print qlist
		results = None
		for query in qlist:
			print query
			print type(Video.keywords)
			if results is None:
				results = Video.objects.filter(keywords=query)
			else:
				results = results | Video.objects.filter(keywords=query)
		sresults = results.order_by(Count('keywords'))
                return render(request, 'videos/search_results.html', {'query': q})
        else:
                return render(request, 'videos/search.html')
