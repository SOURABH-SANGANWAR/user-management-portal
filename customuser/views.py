from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, OtpObject
from rest_framework.response import Response
from .email_manager import EmailManager
from random import randint

class UserCreate(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request,*args,**kwargs):
        try:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                user.is_activated = False
                user.save()
                EmailManager.welcome_email(user)
                return Response({
                    'message':'User created successfully. PLease verify your email address to activate your account and login.',
                })
            else:
                return Response({"error":user_serializer.errors})
        except Exception as e:
            return Response({"error":str(e)})


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request,*args,**kwargs):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            OtpObject.objects.filter(user=user).delete()
            otp_obj = OtpObject.objects.create(user=user,otp=randint(1000,9999))
            otp_obj.save()
            EmailManager.password_reset_email(user,otp_obj.otp)
            return Response({
                'message':'An OTP has been sent to your email address. Please use it to reset your password.',
            })
        except CustomUser.DoesNotExist:
            return Response({'error':'User does not exist'})
    
    def put(self,request,*args,**kwargs):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            otp_obj = OtpObject.objects.get(user=user,otp=request.data['otp'])
            if otp_obj.is_valid_otp():
                otp_obj.delete()
                user.set_password(request.data['password'])
                user.save()
                return Response({
                    'message':'Password reset successful. Please login to continue.',
                })
            else:
                return Response({'error':'Invalid OTP'})
        except CustomUser.DoesNotExist:
            return Response({'error':'User does not exist'})
        except OtpObject.DoesNotExist:
            return Response({'error':'Invalid OTP'})
        except Exception as e:
            return Response({'error':str(e)})
        

class UserRetrive(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        try:
            user = CustomUser.objects.get(email = request.data['email'])
            if user.check_password(request.data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error':'Invalid password'})
        except CustomUser.DoesNotExist:
            return Response({'error':'User does not exist'})

