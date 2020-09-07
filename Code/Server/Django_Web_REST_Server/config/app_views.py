from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone

from rest.models import Device
from rest.models import IPRule
from .forms import ConfigForm, DeleteConfigForm
from .tables import IPRuleTable


@login_required(login_url='/login/')
def app_view(request, id):
    if id == 1:  # IPTABLES
        device = Device.objects.get(owner=request.user)

        table = IPRuleTable(IPRule.objects.filter(device=device))
        form = DeleteConfigForm()
        context = {
            'device': device,
            'table': table,
            'form': form,
            'id': id
        }
        template = loader.get_template('iptables_index.html')
        return HttpResponse(template.render(context, request))
    else:
        return


# iptables--------------------------------------------------
@login_required(login_url='/login/')
def iptables_view(request):
    device = Device.objects.get(owner=request.user)

    table = IPRuleTable(IPRule.objects.filter(device=device))
    form = DeleteConfigForm()
    context = {
        'device': device,
        'table': table,
        'form': form
    }
    template = loader.get_template('iptables_index.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def new_iptables_config(request):
    if request.method == "POST":
        form = ConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)

            config.device = Device.objects.get(owner=request.user)
            config.save()
            device = Device.objects.get(owner=request.user)
            device.last_changed = timezone.now()
            device.save()

            return redirect('config:app_view', id="1")

    else:
        form = ConfigForm()
        return render(request, 'new_config_from.html', {'form':
                                                            form})


@login_required(login_url='/login/')
def delete_iptables_config(request):
    if request.method == "POST":
        config_id = request.POST['id']

        device = Device.objects.get(owner=request.user)
        to_delete = IPRule.objects.get(id=config_id)
        if to_delete.device == device:
            to_delete.delete()
        return redirect('config:app_view', id="1")

    else:
        return redirect('config:app_view', id="1")



