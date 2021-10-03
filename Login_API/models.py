from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OneTimePass(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,)
    otp = models.IntegerField(blank=True, null=True)
    dat_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'one_time_pass'
