from django.urls import path, include

from config import basic_views, app_views

app_name = 'config'
urlpatterns = [
    path('', basic_views.home_store_view, name='home_store_view'),
    path('', include('django.contrib.auth.urls')),
    path('uninstall/<int:id>/', basic_views.uninstall_app, name='uninstall'),
    path('install_app', basic_views.install_app, name='install_app'),

    path('app/<int:id>/', app_views.app_view, name='app_view'),

    # IPTABLES
    path('Firewall-iptables', app_views.iptables_view, name='Firewall-iptables'),
    path('new_iptables_config', app_views.new_iptables_config, name='new_iptables_config'),
    path('delete_iptables_config', app_views.delete_iptables_config, name='delete_iptables_config'),

    # DNS-Firewall
    # path('block_domain', app_views.block_domain, name='block_domain'),
    # path('unblock_domain', app_views.unblock_domain, name='unblock_domain'),

]
