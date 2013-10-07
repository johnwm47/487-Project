from django.shortcuts import render
from django.views import generic
from videos.models import Video

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

class VideoView(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video

def searchResult(request):
        if 'query' in request.GET and request.GET['query']:
                q = request.GET['query']
                return render(request, 'videos/search_results.html', {'query': q})
        else:
                return render(request, 'videos/search.html')
