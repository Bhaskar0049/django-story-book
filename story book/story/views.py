from django.shortcuts import render,get_object_or_404
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db.models import Q
import random
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
from .models import Story,Category

def story_list(request,category_slug=None,tag_slug=None):
    category=None
    categories=Category.objects.all()
    story=Story.objects.all()
    paginator=Paginator(story,4)
    page=request.GET.get('page')
    tag=None
    try:
        story=paginator.page(page)
    except PageNotAnInteger:
        story=paginator.page(1) 
    except EmptyPage:
        story=paginator.page(paginator.num_pages)       
    if category_slug:
        story=Story.objects.all()
        category=get_object_or_404(Category,slug=category_slug)
        story=story.filter(category=category)
        paginator=Paginator(story,3)
        page=request.GET.get('page')
        try:
            story=paginator.page(page)
        except PageNotAnInteger:
            story=paginator.page(1) 
        except EmptyPage:
            story=paginator.page(paginator.num_pages)   
    all_story=list(Story.objects.all())
    recent_story=random.sample(all_story,3)
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        story=Story.objects.filter(tags__in=[tag])
        paginator=Paginator(story,2)
        page=request.GET.get('page')
        try:
            story=paginator.page(page)
        except PageNotAnInteger:
            story=paginator.page(1) 
        except EmptyPage:
            story=paginator.page(paginator.num_pages)   
    return render(request,'story/story_list.html',{
                                                   'categories':categories,
                                                   'story':story,
                                                   'category':category,
                                                   'page':page,
                                                   'recent_story':recent_story,
                                                   'tag':tag
                                                   })  
                                                     
def story_detail(request,id):
    story=get_object_or_404(Story,id=id)
    all_story=list(Story.objects.exclude(id=id))
    like_story=random.sample(all_story,3)

    ############# TAGS

    post_tags_ids = Story.tags.values_list('id', flat=True)
    similar_posts = Story.objects.filter(tags__in=post_tags_ids).exclude(id=story.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]
    
    #############
    return render(request,'story/story_detail.html',{'story':story,'like_story':like_story,})
   ############## 


def search_story(request):
    query=None
    results=[]
    if request.method =="GET"  :
        query=request.GET.get("search")  
        results=Story.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    return render(request,'story/search.html',{'query':query,'results':results,})    



###### select random 3 object form model 
##### select recent 3 object from model
##### select 1 random onbject from the model
