from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.serializers import (
    UserSerializer,
    UserSerializerWithToken
    )
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password

# Create your views here.

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
        context = {'detail': message}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serailizer = UserSerializerWithToken(user, many=False).data

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    
    if data['password'] != '':
        user.password = make_password(data['password'])
    
    user.save()

    return Response(serailizer)


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
