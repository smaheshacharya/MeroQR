from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import pyotp
from users.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,UpdateSerializer
from django.contrib.auth import authenticate
from users.renderers import UserRenderers
from users.models import User 
from django.http import Http404
from .utils import MessageHandler


class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=60)
        OTP = totp.now()
        return {"totp":secret,"otp":OTP}

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        # access_token.set_exp(lifetime=timedelta(days=10))
    }

@api_view(['POST'])
@permission_classes([AllowAny,])
def changePasswordVerify(request,otp_password_forget):
    try:
        user = User.objects.get(otp_password_forget = otp_password_forget)
        _otp = int(user.otp)
        print("otp from db",type(_otp))
        print("otp from frontend", type(otp_password_forget))
        if otp_password_forget != _otp:
            return Response({"Msg" : "Invalid otp"},status=status.HTTP_406_NOT_ACCEPTABLE)
        activation_key_forget_password = user.activation_key_forget_password
        totp = pyotp.TOTP(activation_key_forget_password, interval=60)
        if verify := totp.verify(otp_password_forget):
            user.user_active = True
            user.save()

            return Response({"Msg" : "Your account has been successfully activated!!"})
        else:
            return Response({"Error" : "Given otp is expired!!"})

    except Exception:
        return Response({"Error" : "Invalid otp OR No any active user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny,])
def signupVerify(request,otp):
    try:
        user = User.objects.get(otp = otp)
        _otp = int(user.otp)
        print("otp from db",type(_otp))
        print("otp from frontend", type(otp))
        if otp != _otp:
            return Response({"Msg" : "Invalid otp"},status=status.HTTP_406_NOT_ACCEPTABLE)
        activation_key = user.activation_key
        totp = pyotp.TOTP(activation_key, interval=60)
        if verify := totp.verify(otp):
            user.user_active = True
            user.save()
            return Response({"Msg" : "Your account has been successfully activated!!"})
        else:
            return Response({"Error" : "Given otp is expired!!"})
    except Exception:
        return Response({"Error" : "Invalid otp OR No any active user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    key = generateKey.returnValue()
    user = User(
        phone = serializer.data['phone'],
        otp = key['otp'],
        activation_key = key['totp'],
    )
    user.set_password(serializer.data['password'])
    user.save()
    message_handeller = MessageHandler(serializer.data['phone'], key['otp']).send_otp_on_phone()
    print("message_handeller",message_handeller)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        password = serializer.data.get('password')
        user = authenticate(phone=phone,password=password)
        if user and not user.user_active:
            return Response({'errors':{'non_field_errors':['Verify your phone number first then try again.']}}, status= status.HTTP_404_NOT_FOUND)
        if user is None:
            return Response({'errors':{'non_field_errors':['Phone or Password is not Valid']}}, status= status.HTTP_404_NOT_FOUND)
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Login Success','user_id':user.id}, status= status.HTTP_200_OK)


class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user,context={'request': request})
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
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            raise Http404 from e

    def put(self, request, pk, format=None):
        serializer = SendPasswordResetEmailSerializer(user, data=request.data, partial=True)
        print ("serializer data", serializer)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        key = generateKey.returnValue()
        user = User(
            otp_password_forget = key['otp'],
            activation_key_forget_password = key['totp'],
        )
        user.save()
        message_handeller = MessageHandler(serializer.data['phone'], key['otp']).send_otp_on_phone()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request,uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data,
        context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception =True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            raise Http404 from e
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
