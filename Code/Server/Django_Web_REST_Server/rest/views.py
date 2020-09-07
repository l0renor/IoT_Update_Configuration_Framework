from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest import permissions as ownPermissions
from rest.models import Device
from rest.serializers import IPTablesDeviceConfigSerializer, Stage1DeviceSerializer
from rest.signer import sign


class Stage1DeviceDetail(APIView):
    permission_classes = [ownPermissions.IsOwner, permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        self.check_object_permissions(self.request, device)
        serializer = Stage1DeviceSerializer(device)
        data = serializer.data
        data = sign(data)
        return Response(data)


class IPTablesDeviceDetail(APIView):
    permission_classes = [ownPermissions.IsOwner, permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        device = self.get_object(pk)
        self.check_object_permissions(self.request, device)
        serializer = IPTablesDeviceConfigSerializer(device)
        data = serializer.data
        data = sign(data)
        return Response(data)

# class Stage1DeviceViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Device.objects.all()
#     serializer_class = IPTablesDeviceConfigSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class DeviceViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Device.objects.all()
#     serializer_class = IPTablesDeviceConfigSerializer
#     permission_classes = [permissions.IsAuthenticated]
