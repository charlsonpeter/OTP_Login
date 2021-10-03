from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import DateTimeField, ExpressionWrapper, F
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import *
import requests
import random
import json
# Create your views here.


class GetOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            mob_num = request.data.get('mob_no')
            otp = random.randint(100000, 999999)
            ins_user = None
            if not User.objects.filter(username=str(mob_num)).exists():
                ins_user = User()
                ins_user.username = str(mob_num)
                ins_user.set_password(str(otp))
                ins_user.is_active=False
                ins_user.save()
                OneTimePass.objects.create(user=ins_user, otp=otp)
            elif User.objects.filter(username=str(mob_num), is_active=False).exists():
                ins_user = User.objects.get(username=str(mob_num))
                ins_user.set_password(str(otp))
                ins_user.save()
                OneTimePass.objects.filter(user=ins_user).delete()
                OneTimePass.objects.create(user=ins_user, otp=otp)
            else:
                return Response({'status':'success', 'messages':'Mobile Number Already Used'}, status=status.HTTP_200_OK)
            return Response({'status':'success', 'otp':otp}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            mob_num = request.data.get('mob_no')
            otp = request.data.get('otp')
            ins_otp = OneTimePass.objects.annotate(end_time=ExpressionWrapper(F('dat_created') + timedelta(minutes=5),
                            output_field=DateTimeField())).filter(user__username=str(mob_num), user__is_active=False,
                            otp=otp)
            if ins_otp.filter(end_time__gte=datetime.now()).exists():
                User.objects.filter(username=str(mob_num)).update(is_active=True)
                ins_otp.delete()
            elif ins_otp.exists():
                return Response({'status':'failed', 'message':'OTP Expired'}, status=status.HTTP_200_OK)

            user = authenticate(request, username=str(mob_num), password=str(otp))
            if user:
                login(request, user)
                token_json = requests.post(request.scheme+'://'+request.get_host()+'/api-token-auth/',{'username':str(mob_num),'password':str(otp)})
                token = json.loads(token_json._content.decode("utf-8"))['token']
                return Response({'status':'success', 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'failed', 'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
