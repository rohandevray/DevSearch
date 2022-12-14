from django.shortcuts import render,redirect
from django.contrib.auth import login ,authenticate ,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Profile ,Skill ,Message
from .utlis import searchProfiles ,paginateProfile
from .forms import CustomUserCreationForm ,ProfileForm , SkillForm ,MessageForm
# Create your views here.

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST" :
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exit")
        
        user =authenticate(request,username=username,password=password) #check notes

        if user is not None:
            login(request,user) #this will create session id for the user and log in
            return redirect(request.GET['next'] if 'next' in request.GET else 'account') 
        else:
            messages.error(request,"Username or Password is incorrect")


    return render(request,'users/login_register.html')


def logoutUser(request):
    logout(request) #deleting the session from browser of login
    messages.info(request,"User was successfully logged out!")
    return redirect('login')


def registerUser(request):
    page ="register"
    form =CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST) #sending data of the form to variable form (it stores the info)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"Whoo! Account is successfully created")
            login(request,user)
            return redirect("edit-account")
        else:
             messages.error(request,"Oops! Something went wrong!")
           

    context={'page':page,'form':form}
    return render(request,"users/login_register.html",context)


def profiles(request):
    profiles, search = searchProfiles(request)
    custom_range , profiles = paginateProfile(request,profiles,6)
    context={'profiles':profiles,'search':search ,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)
    

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk) #we have taken all the info of a single profile using id (get by id) which we have clicked upon
    context ={'profile':profile}
    return render(request,'users/user-profile.html',context)

#we can get profile of logged in user by request.user.profile (1 to 1 relationship b/w user and profile)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    context={'profile':profile}
    return render(request,"users/account.html",context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile #that one while is under process to edit
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")
    context={'form': form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url="login")
def createSkill(request):
    page ="create"
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill was added successfully!")
            return redirect("account")
            
            

    context={'form':form,'page':page}
    return render(request,"users/skill_form.html",context)

@login_required(login_url="login")
def updateSkill(request,pk):
    page="update"
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill) #prefill the info by using instance = skill
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill was updated!")
            return redirect("account")
    context={'form':form,'page':page }
    return render(request,"users/skill_form.html",context)


@login_required(login_url="login")
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.info(request,"Skill eliminated!")
        return redirect("account")
        
    context={"object":skill}
    return render(request, "delete_template.html",context)
 
@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all() #realated _name of recipient is messages thats why we dont use _set.all as it will conflict with sender
    unreadCount = messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,"users/inbox.html",context)


@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    mainMessage = profile.messages.get(id=pk)
    if mainMessage.is_read == False:
        mainMessage.is_read = True
        mainMessage.save()
    context={'mainMessage':mainMessage}
    return render(request,"users/message.html",context)

def sendMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
        messages.success(request,"Message sent successfully!")
        return redirect("user-profile",pk=recipient.id)

    context={'form':form,'recipient':recipient}
    return render(request,"users/message_form.html",context)