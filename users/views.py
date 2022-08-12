from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,UpdateSerializer,UserEmailandSlugSerializer
from django.contrib.auth import authenticate
from users.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from users.models import User 
from django.shortcuts import render, get_object_or_404
from django.http import Http404




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        # access_token.set_exp(lifetime=timedelta(days=10))

    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
                {'token':token, 'msg':'Registration Success'},
                status= status.HTTP_201_CREATED
            )
        


class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status= status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status= status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserEmailandSlug(APIView):
    renderer_classes = [UserRenderers]
    def get(self, request, format=None):
        user_email_slug = User.objects.values('email','unique_business_slug')
        serializer = UserEmailandSlugSerializer(user_email_slug, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data= request.data,
        context = {'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Change Success'}, status= status.HTTP_200_OK)


class SendPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, fromat=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Rest Link send. Please check your email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request,uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data,
        context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception =True)
        return Response({'msg':'Password Rest Successfully'}, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
