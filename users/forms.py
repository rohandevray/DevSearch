from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile , Skill , Message

class CustomUserCreationForm(UserCreationForm): #inherit the usercreationform and make changes /better
    class Meta:
        model = User #model name whose fields have to be edited
        fields =['first_name','email','username','password1','password2']
        labels ={
            'first_name' : 'Name', #change the first name to name
        }
    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)
        
        #using for loop
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','location','bio','short_intro','profile_image',
          'social_github', 'social_twitter', 'social_linkedin', 'social_website'
        ]

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        
        #using for loop
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields =['name','description']

    def __init__(self,*args,**kwargs):
        super(SkillForm,self).__init__(*args,**kwargs)
        
        #using for loop
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']
    
    def __init__(self,*args,**kwargs):
        super(MessageForm,self).__init__(*args,**kwargs)
        
        #using for loop
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})