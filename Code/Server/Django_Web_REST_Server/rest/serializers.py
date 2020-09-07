from rest_framework import serializers

from rest.models import Device, IPRule, IoTApplication


class IPRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPRule
        fields = ['chain', 'destination_port', 'packet_type', 'action']


class IPTablesDeviceConfigSerializer(serializers.ModelSerializer):
    ip_rule_set = IPRuleSerializer(many=True, source='ip_rule')

    class Meta:
        model = Device
        fields = ['uuid', 'ip_rule_set']


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IoTApplication
        fields = ['id', 'name', 'version']


class Stage1DeviceSerializer(serializers.HyperlinkedModelSerializer):
    applications = ApplicationSerializer(many=True)
    host = serializers.ReadOnlyField(default='https://dns-rpz.cs.hm.edu:8001')

    class Meta:
        model = Device
        fields = ['uuid', 'host', 'applications']
