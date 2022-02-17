
from typing import OrderedDict
import requests

from django.test import TestCase
from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.test import APITestCase

from Task.serializers import UserSerializer
from Task.models import User


#class for testing SerilizerClass
class UserSerializerTestCase(TestCase):

    def setUp(self):

        User.objects.create(
                id = 3,
                first_name = "Art",
                last_name = "Venere",
                company_name = "Chemel, James L Cpa",
                city = "Bridgeport",
                state = "NJ",
                zip = 80514,
                email = "art@venere.org",
                web = "http://www.chemeljameslcpa.com",
                age = 80
            )

        self.data ={
                "id" : 3,
                "first_name": "Art",
                "last_name": "Venere",
                "company_name": "Chemel, James L Cpa",
                "city": "Bridgeport",
                "state": "NJ",
                "zip": 80514,
                "email": "art@venere.org",
                "web": "http://www.chemeljameslcpa.com",
                "age": 80     
        } 
        self.required_output = [OrderedDict(self.data)]


    def test_Serializer(self):
        user = User.objects.all()
        serialized = UserSerializer(user,many=True)
        
        self.assertEqual(serialized.data,self.required_output)


        


#class for testing api endpoints
class UserAPITestCase(APITestCase):


    def setUp(self):
        
        #getting data from all instances from the APi link that was given in assignment to be used     
        try:
            data = requests.get("https://datapeace-storage.s3-us-west-2.amazonaws.com/dummy_data/users.json")
        except:
            pass

        # creating  objects from each instance with iteration 
        for d in data.json():
             User.objects.create(id= d['id'],
                                first_name= d["first_name"],
                                last_name= d["last_name"],
                                company_name= d["company_name"],
                                city= d["city"],
                                state= d["state"],
                                zip= d["zip"],
                                email= d["email"],
                                web= d["web"],
                                age= d["age"]
                                )

        #creating data manually
        self.data = {
                "id" : 3,
                "first_name": "Art",
                "last_name": "Venere",
                "company_name": "Chemel, James L Cpa",
                "city": "Bridgeport",
                "state": "NJ",
                "zip": 80514,
                "email": "art@venere.org",
                "web": "http://www.chemeljameslcpa.com",
                "age": 80
            }

        #creating invalid data for invalid cases
        self.invalid_data = {
                    
                "first_name": "Art",
                "last_name": "Venere",
                "company_name": "Chemel, James L Cpa",
                "city": "Bridgeport",
                "state": "NJ",
                "zip": 80514,
                "email": "art@venere.org",
                "web": "http://www.chemeljameslcpa.com",
                "age":  "char"    ,
            }



    # testing post api with valid data
    def test_user_create(self):
        res = self.client.post("/api/user/",self.data)
        self.assertEquals(res.status_code,status.HTTP_201_CREATED)



    # testing post api with invalid data
    def test_user_create_fail(self):
        res = self.client.post("/api/user/",self.invalid_data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    


    #testing get api to list,  without query parametets in url   
    def test_user_fetch_without_param(self):
        res = self.client.get("/api/user/")

        quer = User.objects.all().order_by('id')
        Page = Paginator(quer,5)
        serilized = UserSerializer(Page.page(1).object_list,many=True)
        
        self.assertEqual(res.json()['results'],serilized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    # testing get api to list, with name parameter in url
    def test_user_fetch_with_filter_substring_insensitive(self):

        res = self.client.get("/api/user/?name=ven")

        quer = User.objects.filter(Q(first_name__icontains='VEn')|Q(last_name__icontains='VEN')).order_by('id')
        Page = Paginator(quer,5)
        serilized = UserSerializer(Page.page(1).object_list,many=True)

        self.assertEqual(res.json()['results'],serilized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    # testing get api to list, with limit parameter in url
    def test_user_fetch_with_pagination_limit(self):

        res = self.client.get("/api/user/?limit=20")

        quer = User.objects.all().order_by("id")
        Page = Paginator(quer,20)
        serilized = UserSerializer(Page.page(1).object_list,many=True)

        self.assertEqual(res.json()['results'],serilized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    # testing get api to list, with sort parameter in url
    def test_user_fetch_with_sort(self):
        res = self.client.get("/api/user/?sort=-age")

        quer = User.objects.all().order_by("-age")
        Page = Paginator(quer,5)
        serilized = UserSerializer(Page.page(1).object_list,many=True)

        self.assertEqual(res.json()['results'],serilized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    # testing get api to list,  with all name,limit,sort parameters
    def test_user_fetch_with_all_params(self):
        res = self.client.get("/api/user/?name=ma&limit=15&sort=zip")

        quer = User.objects.filter(Q(first_name__icontains='mA')|Q(last_name__icontains='MA')).order_by("zip")
        Page = Paginator(quer,15)
        serilized = UserSerializer(Page.page(1).object_list,many=True)

        self.assertEqual(res.json()['results'],serilized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)



    # testing get api to detail particular single object with valid pk
    def test_user_get(self):
        res = self.client.get("/api/user/5/")

        query = User.objects.get(pk=5)
        serialized = UserSerializer(query)

        self.assertEqual(res.data,serialized.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    

    # testing get api to detail object with invalid pk,to be respond with 404 not found
    def test_user_get_invalid_pk(self):
        # object with id = 510 in none existing 
        res = self.client.get("/api/user/510/")

        self.assertEqual(res.status_code,status.HTTP_404_NOT_FOUND)

    

    # testing update api with valid data
    def test_user_update(self):
        
        changed = self.client.put("/api/user/3/",data=self.data)
        re_get = self.client.get("/api/user/3/")

        self.assertEqual(changed.status_code,status.HTTP_200_OK)

        #rechecking the object whether it got updated with self.data
        self.assertEqual(re_get.data,self.data)



    # testing update api with invalid data
    def test_user_update_invalid_data(self):
        
        changed = self.client.put("/api/user/3/",data=self.invalid_data)
    
        self.assertEqual(changed.status_code,status.HTTP_400_BAD_REQUEST)
        


    # testing delete api with valid pk
    def test_user_delete(self):
        
        delete = self.client.delete("/api/user/3/")
        re_get = self.client.get("/api/user/3/")

        self.assertEqual(delete.status_code,status.HTTP_200_OK)
        
        #if object with id = 3 was deleted it should not found on getting
        self.assertEqual(re_get.status_code,status.HTTP_404_NOT_FOUND)
        

    # testing delete api with invalid pk
    def test_delete_not_existing(self):
        delete = self.client.delete("/api/user/510/")
        
        self.assertEqual(delete.status_code,status.HTTP_404_NOT_FOUND)


    


    


     

    





        


    
 


    

