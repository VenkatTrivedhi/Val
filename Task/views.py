from rest_framework.views import Response
from rest_framework import viewsets,status
from rest_framework.pagination import LimitOffsetPagination
from Task.models import User
from Task.serializers import UserSerializer
from django.db.models import Q


#this single class can fullfill the all the api endpoint requirements asked in assignment 
class UsersView(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    pagination_class  = LimitOffsetPagination


    # overriding to get queryset as per sort, limit,name parameters 
    def get_queryset(self):
        try:
            ordering = self.request.GET["sort"]
        except:
            ordering = 'id'
        try:
            name  = self.request.GET["name"]
            return User.objects.filter(Q(first_name__icontains=name)|Q(last_name__icontains=name)).order_by(ordering)
        except:
            return User.objects.all().order_by(ordering)


    # overriding the delete api because on success response with status "200 ok" is asked in assignment,
    # but the Modelviewset's destroy method returning 204 instead
    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            query = {"detail": "Successfully deleted"}
            return Response(query,status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            query = {"detail": "Not found."}
            return Response(query,status=status.HTTP_404_NOT_FOUND)

    
        


    




    
    
    
   
    


        


            



    
