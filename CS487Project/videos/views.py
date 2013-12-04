from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from models import *
from django.db.models import Count, Avg
from django.template import RequestContext
from django.utils.http import urlencode
from forms import *
import string
import re
import datetime

def getVideo(pk):
        video = get_object_or_404(Video, pk=pk)
        if not video.block == None:
            raise Http404
        else:
            return video

# Create your views here.
class IndexView(generic.ListView):
        template_name = 'videos/index.html'
        model = Video

        def get_queryset(self, **kwargs):
		allvids = super(IndexView, self).get_queryset(**kwargs).filter(block=None)
		related = getRelatedVideos(self.request)
		unrelated = allvids.exclude(related)
		if related and unrelated:
			sort = related | unrelated
		elif related:
			sort = related
		elif unrelated:
			sort = unrelated
		else:
			sort = allvids
		return sort
                #return super(IndexView, self).get_queryset(**kwargs).filter(block=None)

class ViewVideo(generic.DetailView):
        template_name = 'videos/view.html'
        model = Video
        
        def get_queryset(self, **kwargs):
            return super(ViewVideo, self).get_queryset(**kwargs).filter(block=None)

        def get_context_data(self, **kwargs):
            context = super(ViewVideo, self).get_context_data(**kwargs)
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

class EditVideo(generic.UpdateView):
        template_name = 'videos/edit.html'
        model = Video
        form_class = VideoUploadForm

        def get_success_url(self):
            return self.object.get_absolute_url()

        def get_queryset(self, **kwargs):
            return super(EditVideo, self).get_queryset(**kwargs).filter(block=None)

        def get_object(self, **kwargs):
            video = super(EditVideo, self).get_object(**kwargs)
            if self.request.user.has_perm('videos.change_video') or self.request.user == video.uploader:
                return video
            else:
                raise PermissionDenied()

@permission_required('videos.add_video', raise_exception=True)
def uploadFile(request):
	if request.method == 'POST':
		form = VideoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			f = form.save(commit=False)
                        f.uploader = request.user
                        f.save()
                        form.save_m2m()
			return redirect(f)
	else:
		form = VideoUploadForm()
	return render_to_response('videos/upload.html', {'form': form}, context_instance=RequestContext(request))

def videoCount(request, pk):
        video = getVideo(pk)
        video.viewCount += 1
        if request.user.is_authenticated():
            vv, created = video.user_views.get_or_create(user=request.user, defaults={'count':1, 'video':video})
            if created:
                vv.count += 1
                vv.save()
        video.save()
        return HttpResponse(status=200)

def getRelatedVideos(request):
	related = None
	results = Video.objects.filter(block=None)
	if request.user.is_authenticated():
		u = request.user
		bliked = BeakerRating.objects.filter(rater = u).filter(rating__in=[4, 5]).values_list('video', flat=True)
		sliked = StarRating.objects.filter(rater = u).filter(rating__in=[4, 5])
		liked = Video.objects.filter(pk__in=set(bliked)) | Video.objects.filter(pk__in=set(sliked))
		keywords = liked.values_list('keywords', flat=True)
		for key in keywords:
			if related is None:
				related = results.filter(keywords__keyword=key)
			else:
				related = related | results.filter(keywords__keyword=key)
	return related

def searchResult(request):
        results = Video.objects.filter(block=None)
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
		relevant = getRelatedVideos(request)
		if relevant:
			related = relevant & r
			results1 = related.annotate(matches=Count('keywords')).order_by('-matches')
		else: 
			related = None
			results1 = None
		
		if relevant:
			unrelated = r.exclude(relevant)
		else:
			unrelated = r
		results2 = unrelated.annotate(matches=Count('keywords')).order_by('-matches')
		if results1 and results2:
			results = results1 | results2
		elif results1:
			results = results1
		elif results2:
			results = results2
		else:
			results = None
	if 'jquery' in request.GET and request.GET['jquery']:
                context['jquery'] = request.GET['jquery']
		results = results.filter(journal__name=request.GET['jquery'])

	if 'aquery' in request.GET and request.GET['aquery']:
                context['aquery'] = request.GET['aquery']
		results = results.filter(authors__name=request.GET['aquery'])

        if context != {}:
                context['results'] = results
        return render(request, 'videos/search.html', context)

@permission_required('videos.add_rating', raise_exception=True)
def createRating(request, pk, t):
    obj = getVideo(pk)

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

@permission_required('videos.add_videoflag', raise_exception=True)
def createVideoFlag(request, pk):
    obj = getVideo(pk)
    if request.method == 'POST':
        form = FlagVideoForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.flagger = request.user
            f.video = obj
            f.save()
            return render(request, 'flag/flag_success.html')
    else:
        form = FlagVideoForm()
    return render_to_response('flag/leave_flag.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))

@permission_required('videos.add_commentflag', raise_exception=True)
def createCommentFlag(request, pk):
    obj = getVideo(pk)
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
