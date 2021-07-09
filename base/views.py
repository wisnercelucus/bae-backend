from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from .products import products
# Create your views here.

def insertProducts(user):
    for p in products:
        if p['_id'] == '1':
            continue
        prod = Product()
        prod.name = p['name']
        prod.description = p['description']
        prod.price = p['price']
        prod.countInStock = p['countInStock']
        prod.rating = p['rating']
        prod.brand = p['brand']
        prod.category = p['category']
        prod.numReviews = p['numReviews']
        prod.user = user
        prod.save()


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
