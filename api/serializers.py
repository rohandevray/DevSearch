#converting the models into the json format for our apis using Model Serializers

from rest_framework import serializers
from projects.models import Project,Tag ,Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
   #to add an attribute(reviews) and convert into json format using below method field
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer =ReviewSerializer(reviews,many=True)
        return serializer.data