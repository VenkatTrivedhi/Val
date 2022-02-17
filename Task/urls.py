
from django.urls import path,include
from Task.views import UsersView
from rest_framework import routers

route = routers.SimpleRouter()
route.register("user",UsersView,basename="user")

urlpatterns = [  
    path('api/',include(route.urls),name="api"),
]