from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import pyotp
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
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
        totp = pyotp.TOTP(secret, interval=300)
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
def signupVerify(request,otp):
    try:
        user = User.objects.get(otp = otp)
        _otp = int(user.otp)
        print("otp from db",type(_otp))
        print("otp from frontend", type(otp))
        if otp != _otp:
            return Response({"Msg" : "Invalid otp"},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            activation_key = user.activation_key
            totp = pyotp.TOTP(activation_key, interval=300)
            verify = totp.verify(otp)
            
            if verify:
                user.user_active     = True
                user.save()
                
                return Response({"Msg" : "Your account has been successfully activated!!"})
            else:
                return Response({"Msg" : "Given otp is expired!!"})
    
    except:
        return Response({"Msg" : "Invalid otp OR No any active user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = UserRegistrationSerializer(data=request.data)
    # print(serializer)

    if serializer.is_valid():
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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       


# class UserRegistrationView(APIView):
#     renderer_classes = [UserRenderers]
#     def post(self, request, phone, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
#         print("print data from user registration", serializer)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
        
#         token = get_tokens_for_user(user)
        
#         return Response(
#                 {'token':token, 'msg':'Registration Success'},
#                 status= status.HTTP_201_CREATED
#             )
       

class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        password = serializer.data.get('password')
        user = authenticate(phone=phone,password=password)
        if not user.user_active:
            return Response({'errors':{'non_field_errors':['Verify you phone number first then try again.']}}, status= status.HTTP_404_NOT_FOUND)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success','user_id':user.id}, status= status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Phone or Password is not Valid']}}, status= status.HTTP_404_NOT_FOUND)


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
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


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
