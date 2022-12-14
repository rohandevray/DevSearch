from django.db import models
from users.models import Profile
import uuid

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
    demo_link= models.CharField(max_length=2000,null=True,blank=True)
    source_link =models.CharField(max_length=2000,null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True) #if Tag model is above this model then we dont need to put it in (' ')
    vote_total=models.IntegerField(default=0, null= True, blank=True)
    vote_ratio=models.IntegerField(default=0, null= True, blank=True)
    created =models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True,unique=True)
    def __str__(self):
        return self.title #python things to reprsent this class by its title not by defult its id
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']  #recent created project at top (order)
    
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset


    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_ratio = ratio
        self.vote_total = totalVotes
        self.save()

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up vote'),
        ('down','Down vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE ,null=True)
    #one to many relationships between models using foreign key
    project=models.ForeignKey(Project,on_delete=models.CASCADE) #on deletion of project(parent) its reviews(children) also get deleted (as we used CASACADE)
    body =models.TextField(null=True, blank=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE) #values gives choices as vote type in dropdown options
    created =models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True,unique=True)

    #to make sure owner of review can give 1 review per project 

    class Meta:
        unique_together = [['owner','project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created =models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True,unique=True)
    def __str__(self):
        return self.name


    
