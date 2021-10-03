from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
import random
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
                OneTimePass.objects.create(fk_user=ins_user, otp=otp)
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
