from django.contrib.auth.models import User
from django.db import models


class IoTApplication(models.Model):
    id = models.fields.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50)
    version = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Device(models.Model):
    uuid = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    applications = models.ManyToManyField(IoTApplication, blank=True, related_name='App')

    def __str__(self):
        return 'device: ' + str(self.uuid)

#App models-----------------------------------------------------------------------------------------------


class IPRule(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='ip_rule')
    chain = models.CharField(max_length=6)  # INPUT/OUTPUT
    destination_port = models.IntegerField()
    packet_type = models.CharField(max_length=10) #TCP,UDP,..
    action = models.CharField(max_length=15)  # Drop,..

    def __str__(self):
        return self.chain + ' | ' + str(self.device)

    class Meta:
        verbose_name_plural = "IP_Rules"
        ordering = ("id",)


