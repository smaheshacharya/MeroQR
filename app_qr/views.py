from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . custom_permission import IsOwnerOrReadOnly
from .models import Category as CategoryModel
from .models import Product as ProductModel
from .models import Resturant as ResturantModel
from .models import Qr as QrModel
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import ProductCategorySerializer
from .serializers import ResturantSirializer
from .serializers import QrSirializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


class CategoryList(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        category = CategoryModel.object.filter(user_id=self.request.user).order_by ('-id')
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

class ResturantList(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        resturant = ResturantModel.object.filter(user_id=self.request.user)
        serializer = ResturantSirializer(resturant, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            serializer = ResturantSirializer(data=request.data, many=True)
        else:
            serializer = ResturantSirializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user)
            return Response({"Message":"Resturant Data Created Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QrList(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        qrdata = QrModel.object.filter(user_id=self.request.user)
        serializer = QrSirializer(qrdata, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            serializer = QrSirializer(data=request.data, many=True)
        else:
            serializer = QrSirializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=self.request.user)
            return Response({"Message":"Qr Data Created Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductList(APIView):
    permission_classes = [IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        product = ProductModel.object.filter(user_id=self.request.user).order_by ('-id')
        serializer = ProductSerializer(product, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list):
            print(data)
            serializer = ProductSerializer(data=data, many=True)

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
        except CategoryModel.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category,context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
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

class ResturantDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
        ]
    def get_object(self, pk):
        try:
            return ResturantModel.object.get(pk=pk)
        except ResturantModel.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        resturant = self.get_object(pk)
        serializer = ResturantSirializer(resturant,context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk, format=None):
        resturant = self.get_object(pk)
        serializer = ResturantSirializer(resturant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Resturant Update Successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        resturant = self.get_object(pk)
        resturant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get_object(self, pk):
        try:
            return ProductModel.object.get(pk=pk)
        except ProductModel.DoesNotExist as e:
            raise Http404 from e
            
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product,context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Product Update Successfully"})    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllProducCategorytListPublic(APIView):
    def get(self, request, pk, format=None):
        category_product = CategoryModel.object.filter(user_id=pk).order_by ('id')
        serializer = ProductCategorySerializer(category_product, many=True,context={'request': request})
        return Response(serializer.data)

class AllProducCategorytList(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]    
    def get(self, request, format=None):
        category = CategoryModel.object.filter(user_id=self.request.user)
        serializer = ProductCategorySerializer(category, many=True,context={'request': request})
        return Response(serializer.data)

class ResturantData(APIView):
    def get(self, request, pk, format=None):
        resturant_data = ResturantModel.object.filter(user_id=pk)
        serializer = ResturantSirializer(resturant_data, many=True,context={'request': request})
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

