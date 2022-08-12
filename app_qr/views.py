from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . custom_permission import IsOwnerOrReadOnly
from .models import Category as CategoryModel, Product
from .models import Product as ProductModel
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import ProductCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.shortcuts import render, get_object_or_404





class CategoryList(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        category = CategoryModel.object.filter(user_id=self.request.user)
        serializer = CategorySerializer(category, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            serializer = CategorySerializer(data=request.data, many=True)
        else:
            serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user)
            return Response({"Message":"Category Created Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductList(APIView):
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        product = ProductModel.object.filter(user_id=self.request.user)
        serializer = ProductSerializer(product, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            serializer = ProductSerializer(data=request.data, many=True)
        else:
            serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user)
            return Response({"Message":"Product Created Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
class CategoryDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
        ]
    def get_object(self, pk):
        try:
            return CategoryModel.object.get(pk=pk)
        except CategoryModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category,context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Category Update Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get_object(self, pk):
        try:
            return ProductModel.object.get(pk=pk)
        except ProductModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = ProductSerializer(category)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = ProductSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Product Update Successfully"})    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllProducCategorytList(APIView):
    def get(self, request, pk, format=None):
        category_product = CategoryModel.object.filter(user_id=pk)
        serializer = ProductCategorySerializer(category_product, many=True,context={'request': request})
        return Response(serializer.data)



class AllProduct(APIView):
    def get(self, request, pk, format=None):
        product = ProductModel.object.filter(user_id=pk)
        serializer = ProductSerializer(product, many=True,context={'request': request})
        return Response(serializer.data)


class AllCategory(APIView):
    def get(self, request, pk, format=None):
        category = CategoryModel.object.filter(user_id=pk)
        serializer = CategorySerializer(category, many=True,context={'request': request})
        return Response(serializer.data)