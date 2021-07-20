from rest_framework.response import Response
from base.models import Product
from base.serializers import (ProductSerializer,)
from rest_framework.decorators import api_view

#from rest_framework import status


# Create your views here.

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
