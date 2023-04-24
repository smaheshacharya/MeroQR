from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import User 
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    # otp_code = serializers.CharField(write_only=True, required=True, max_length=4)
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True )
    class Meta:
        model = User
        fields=['phone' ,'password']
        
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
       
       
class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['phone','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone']
    
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    class Meta:
        fields = ['id','phone','otp_password_forget','activation_key_forget_password']
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        print("forget password phone",phone)
        if User.objects.filter(phone=phone).exists():
            return attrs
        else:
            return Response({"Error" : "You are not registered user"}, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):  # sourcery skip: avoid-builtin-shadow
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is Invalid or Expired')

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is Valid or Expired') from identifier

        
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone']
        
        