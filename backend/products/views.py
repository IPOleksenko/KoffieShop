from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializer import ProductSerializer

class ProductListView(APIView):
    """Class for getting the list of products"""
    permission_classes = [AllowAny]
    allowed_methods = ["GET"]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    """Class for working with a specific product"""
    permission_classes = [AllowAny]
    allowed_methods = ["GET"]

    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
