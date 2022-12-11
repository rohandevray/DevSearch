from django.db.models import Q
from . models import Skill , Profile
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage


def paginateProfile(request,profiles,results):
    page = request.GET.get('page')
    paginator = Paginator(profiles,results) #p = Paginator(objects,2)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page =1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles= paginator.page(page)

    leftIndex = (int(page)-4)
    if leftIndex < 1:
        leftIndex =1
    
    rightIndex =(int(page)+5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
    
    custom_range = range(leftIndex,rightIndex) #range(1,100) its range function
    return custom_range , profiles






def searchProfiles(request):
    search =""
    if request.GET.get('text'):
        search = request.GET.get('text')
    
    skills = Skill.objects.filter(name__icontains=search) #searching via skills by name and then filter it among profiles by checking skill of which profile is in skills set we search
    profiles =Profile.objects.distinct().filter(Q(name__icontains=search)  |
        Q(short_intro__icontains=search) | Q(skill__in=skills))
     #all  info from profile model dtabase into profiles
    return profiles , search