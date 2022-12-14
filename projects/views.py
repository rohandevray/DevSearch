from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project , Review ,Tag
from .forms import ProjectForm ,ReviewForm
from django.contrib import messages
from .utlis import searchProjects ,paginateProject
from django.core.paginator import Paginator ,PageNotAnInteger ,EmptyPage
# Create your views here.
# here we write the functions that we need to get triggers
#after we join the templates to the baseDIR we can use templates and render it


def projects(request):
    projects, search = searchProjects(request)
    custom_range ,projects = paginateProject(request ,projects,6)
    context={'projects':projects,'search':search , 'custom_range':custom_range} #passing data into templates via object (as when too many datas to pass)
    return render(request,'projects/projects.html', context)

def project(request,pk):
    singleproject = Project.objects.get(id=pk)
    reviews = Review.objects.filter(project=singleproject)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False) #instance of the review 
        review.project = singleproject  #setting the project of the review
        review.owner = request.user.profile #setting the owner of the review
        review.save()

            #update vote count
        singleproject.getVoteCount
        messages.success(request,'Your review was submitted!')
        return redirect("project" , pk = singleproject.id)
            

    context={'project':singleproject,'reviews':reviews ,'form':form}
    return render(request,'projects/single-project.html',context) # we have to find in projects app to find these templates

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST,request.FILES) #request.FIles for files to upload(e.g images here)
        if form.is_valid():
            project =form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request,"Project was added successfully!")
            return redirect('account')
    context={'form':form}
    return render(request,"projects/project-form.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) #we can get the project set of logged in user only
    form = ProjectForm(instance=project)  #fill its form by given data already
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()

        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.info(request,"Project was updated!")
            return redirect('account')
    context={'form':form , 'project':project}
    return render(request,"projects/project-form.html",context)

@login_required(login_url="login")
def deleteProject(request,pk):
   profile = request.user.profile
   project = profile.project_set.get(id=pk)
   if request.method=='POST':
    project.delete() #deleted the project selected
    messages.info(request,"Project was deleted")
    return redirect('account')
   context={'object':project}
   return render(request,"delete_template.html",context)
