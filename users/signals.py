#signals
from django.db.models.signals import post_save, post_delete
#post_save triggers after a model is saved
from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver #decorator
#sending mails
from django.core.mail import send_mail
from django.conf import settings

#revciver for signals
def createProfile(sender,instance,created,**kwargs):
    # IMPORTANT : when user is created a profile for it will be generated 
    if created: #created is flag (true or false for new user)
        user = instance
        profile = Profile.objects.create(
            #auto fill info in profile when a user is created
            user = user, #auto connecting the user that triggers to its profile (user after equal is instance)
            username = user.username,
            email = user.email,
            name = user.first_name
        )
 #sending mails after registering to website
        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
             subject,
             message,
             settings.EMAIL_HOST_USER,
             [profile.email],
             fail_silently=False,
        )


def updateUser(sender , instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

       

def deleteUser(sender,instance,**kwargs): 
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile,sender=User) 
#whenever User(sender) model / User is created in db then  createprofile function is triggers

post_delete.connect(deleteUser,sender=Profile) #instance is Sender i.e Profile