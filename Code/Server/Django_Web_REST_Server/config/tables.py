import django_tables2 as tables

from rest.models import IPRule, IoTApplication


class IPRuleTable(tables.Table):
    class Meta:
        model = IPRule
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "chain", "destination_port", "packet_type", "action")


class ApplicationTable(tables.Table):
    class Meta:
        model = IoTApplication
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "version")


