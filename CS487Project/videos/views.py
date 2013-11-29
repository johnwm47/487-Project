from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.views import generic
from models import Video, Flag, Comment
from django.db.models import Count, Avg
from django.template import RequestContext
from forms import *
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

        def get_context_data(self, **kwargs):
            context = super(VideoView, self).get_context_data(**kwargs)
            if self.request.user.is_authenticated() and self.request.user.has_perm('videos.add_rating'):
                try:
                    star = self.object.stars.get(rater=self.request.user)
                except ObjectDoesNotExist:
                    star = None
    
                try:
                    beaker = self.object.beakers.get(rater=self.request.user)
                except ObjectDoesNotExist:
                    beaker = None
            else:
                star = None
                beaker = None

            context['star'] = StarRatingForm(instance=star)
            context['beaker'] = BeakerRatingForm(instance=beaker)

            context['star_avg'] = self.object.stars.aggregate(Avg('rating'))['rating__avg']
            context['beaker_avg'] = self.object.beakers.aggregate(Avg('rating'))['rating__avg']

            return context

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

@permission_required('videos.add_rating')
def createRating(request, pk, t):
    obj = get_object_or_404(Video, pk=pk)

    if t == 'star':
        formType = StarRatingForm
        data = obj.stars
    elif t == 'beaker':
        formType = BeakerRatingForm
        data = obj.beakers
    else:
        raise Http404

    try:
        rating = data.get(rater=request.user)
    except ObjectDoesNotExist:
        rating = None

    if request.method == 'POST':
        form = formType(request.POST, instance=rating)
        if form.is_valid():
            f = form.save(commit=False)
            f.rater = request.user
            f.video = obj
            f.save()
            return render(request, 'rating/rating_success.html')
    else:
        form = formType(instance=rating)
    return render_to_response('rating/leave_rating.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))

@permission_required('videos.add_videoflag')
def createVideoFlag(request, pk):
    obj = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = FlagVideoForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.flagger = request.user
            f.video = obj
            f.save()
            return render(request, 'flag/flag_success.html')
    else:
        form = FlagCreationForm()
    return render_to_response('flag/leave_flag.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))

@permission_required('videos.add_commentflag')
def createCommentFlag(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = FlagCommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.flagger = request.user
            f.comment = obj
            f.save()
            return render(request, 'flag/flag_success.html')
    else:
        form = FlagCreationForm()
    return render_to_response('flag/leave_flag.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))

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
