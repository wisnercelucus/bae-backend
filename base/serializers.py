from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_admin', 'name', '_id', 'username', 'email']

    def get_name(self, obj):
        name = obj.first_name

        if name == '':
            name = obj.email

        return name

    def get__id(self, obj):
        return obj.id

    def get_is_admin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_admin', 'name', '_id', 'username', 'email', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)

        return str(token.access_token)



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'