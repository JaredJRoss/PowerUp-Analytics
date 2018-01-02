from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from analytics.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .filters import *

#Takes a get request and parses the time in and out of each port kiosk combo
def upload(request):
    #url/upload/?id=
    kioskT = request.GET['id']
    #url/upload/?port=
    test = request.GET['ports']
    #split by the word port will make array of each port with extra blank for before the first port
    test = test.split('port')
    #get the kiosk that is sending data
    kiosk = Kiosk.objects.get(ID=request.GET['id'])
    #go through each port
    for s in test:
    #if its the blank port ignore
        if s !='':
            #get the port number and find the port that goes with the kiosk
            port = Port.objects.get(Port=int(s[0]), Kiosk=kiosk)
            #get rid of the surounding the list and split by the unique character to get each time in and out
            temp = s[2:len(s)-1].split('@')
            # go through list of times
            for t in temp:
                #split by comma and get rid of []
                times = t[1:len(t)-1].split(',')
                #parse the dates in the standard datetime format
                date = datetime.datetime.strptime(times[0],'%Y-%m-%d %H:%M:%S.%f')
                date1 = datetime.datetime.strptime(times[1],'%Y-%m-%d %H:%M:%S.%f')
                #make a new Time object connecting to the port
                time = Time(Port = port, TimeIn = date,TimeOut=date1)
                print(time)
                #save the object
                time.save()
    #should not render but this is for testing
    return render(request,'upload.html',{'id':request.GET['id']})

#creating everything that is needed like client location and kiosk
def make_user(request):
    print(request.POST)
    client_form = ClientForm(request.POST)
    if client_form.is_valid():
        print("Client")
        User.objects.create_user(request.POST['ClientName'],'','password',is_staff=True)
        client_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))

    location_form = LocationForm(request.POST)
    if location_form.is_valid():
        print('location')
        print(location_form)
        location_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))
    kiosk_form = KioskForm(request.POST)
    if kiosk_form.is_valid():
        print('kiosk')
        kiosk_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))
    port_form = PortForm(request.POST)
    if port_form.is_valid():
        port_form.save()
        return HttpResponseRedirect(reverse('analytics:add_user'))

    context = {
    'clientform':client_form,
    'locationform':location_form,
    'kioskform':kiosk_form,
    'portform':port_form,
    }
    return render(request, 'new_user.html',context)



#autocomplete for clients
class ClientAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Client.objects.all().order_by("ClientName")
        if self.q:
            qs = qs.filter(ClientName__icontains=self.q)
        return qs
#autocomplete for clients
class LocationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Location.objects.all().order_by("LocationName")
        if self.q:
            qs = qs.filter(LocationName__icontains=self.q)
        return qs
#autocomplete for clients
class KioskAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
    #add authentication django-autocomplete light .readdocs.io
        qs = Kiosk.objects.all().order_by("ID")
        if self.q:
            qs = qs.filter(ID__icontains=self.q)
        return qs

def search(request):
    print(request.GET)
    query_set = Kiosk.objects.all()
    kioskFilter  = KioskFilter(request.GET,query_set)
    #print(Kiosk.objects.filter(''))
    print(kioskFilter.qs)
    return render(request,'search.html',{'kioskFilter':kioskFilter})
