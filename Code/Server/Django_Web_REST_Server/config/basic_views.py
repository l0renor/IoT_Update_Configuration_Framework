from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from rest.models import Device, IoTApplication
from .forms import DeleteConfigForm
from .tables import ApplicationTable


@login_required(login_url='/login/')
def home_store_view(request):
    device = Device.objects.get(owner=request.user)
    ids = []
    apps = device.applications.all()
    for app in apps.all():
        ids += [app.id]
    table = ApplicationTable(IoTApplication.objects.exclude(id__in=ids))
    form = DeleteConfigForm()
    context = {
        'device': device,
        'table': table,
        'form': form,
        'apps': apps
    }
    template = loader.get_template('appstore_index.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def install_app(request):
    if request.method == "POST":
        config_id = request.POST['id']

        device = Device.objects.get(owner=request.user)
        to_install = IoTApplication.objects.get(id=config_id)
        device.applications.add(to_install)
        return redirect('config:home_store_view')

    else:
        return redirect('config:home_store_view')


@login_required(login_url='/login/')
def uninstall_app(request, id):
    device = Device.objects.get(owner=request.user)
    to_uninstall = IoTApplication.objects.get(id=id)
    device.applications.remove(to_uninstall)
    return redirect('config:home_store_view')


