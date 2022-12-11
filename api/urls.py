from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #when the above token expires then this create a new one and stores in the browser


    path('',views.getRoutes),
    path('projects/',views.getProjects),
    path('projects/<str:pk>/',views.getProject), 
    path('projects/<str:pk>/vote/',views.ProjectVote), 

]