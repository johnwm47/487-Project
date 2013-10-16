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
		results = None
		for query in qlist:
			print query
			if results is None:
				results = Video.objects.filter(keywords__keyword=query)
			else:
				results = results | Video.objects.filter(keywords__keyword=query)
		sresults = results.annotate(matches=Count('keywords')).order_by('-matches')
		if 'jquery' in request.GET and request.GET['jquery']:
			sresults = sresults.filter(journal__name=jquery)
		if 'aquery' in request.GET and request.GET['aquery']:
			sresults = sresults.filter(authors__name=aquery)
                return render(request, 'videos/search_results.html', {'query': q, 'results': sresults} )
	elif 'jquery' in request.GET and request.GET['jquery']:
		results = Video.objects.filter(journal__name=jquery)
		if 'aquery' in request.GET and request.GET['aquery']:
			results = results.filter(authors__name=aquery)
		return render(request, 'videos/search_results.html', {'query': q, 'results': results} )
	elif 'aquery' in request.GET and request.GET['aquery']:
		results = Video.objects.filter(authors__name=aquery)
        else:
                return render(request, 'videos/search.html')
	
@permission_required('videos.add_video')
def uploadFile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', {'form': form})
