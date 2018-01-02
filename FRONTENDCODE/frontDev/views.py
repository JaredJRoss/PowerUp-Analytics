from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def admin_side(request):
    return render(request, 'admin_view.html')
def kiosk(request):
	template = loader.get_template('kiosk.html')
	context = {'status' : "offline"}
	return HttpResponse(template.render(context, request))
def port(request):
	template = loader.get_template('port.html')
	context = {'status' : "offline"}
	return HttpResponse(template.render(context, request))