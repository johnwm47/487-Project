from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from videos.models import Video

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

class VideoView(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video

def videoCount(request, pk):
        video = get_object_or_404(Video, pk=pk)
        video.viewCount += 1
        video.save()
        return HttpResponse(status=200)

def searchResult(request):
        if 'query' in request.GET and request.GET['query']:
                q = request.GET['query']
                return render(request, 'videos/search_results.html', {'query': q})
        else:
                return render(request, 'videos/search.html')
