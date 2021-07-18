from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import (ProductSerializer,
    UserSerializer,
    UserSerializerWithToken
    )
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/products/',
        'api/products/create/',
        'api/products/upload/',
        'api/products/<id>/reviews/',
        'api/products/top/',
        'api/products/<id>/',
        'api/products/delete/<id>/',
        'api/products/update/<id>/',
    ]
    return Response(routes)

@api_view(['GET'])    
def getProducts(request):
    products = Product.objects.all()
    serailizer = ProductSerializer(products, many=True).data

    return Response(serailizer)


@api_view(['GET'])    
def getProduct(request, pk):
    product = Product.objects.filter(pk=int(pk)).first()
    serailizer = ProductSerializer(product).data

    return Response(serailizer)

@api_view(['POST'])
def register(request):
    data = request.data

    try:

        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )


        serializer = UserSerializerWithToken(user).data

        return Response(serializer)
    except:
        message = "Email already exist. Unable to create the account."
        context = {'message': message}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serailizer = UserSerializer(user, many=False).data
    return Response(serailizer)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])    
def getUsers(request):
    users = User.objects.all()
    serailizer = UserSerializer(users, many=True).data

    return Response(serailizer)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
