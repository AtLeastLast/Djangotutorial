from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator



#Python docs for datetime/How to format datetime

def venue_pdf(request):
    #Create a Bytestream buffer
    buf = io.BytesIO()
    #Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("===================")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    writer = csv.writer(response)
    venues = Venue.objects.all().order_by('name')
    writer.writerow(['Venue Name','Address','Zip Code','Phone','Web Address','Email'])

    for venue in venues:
        writer.writerow([venue,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])

    return response

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f'{venue}\n{venue.address}\n{venue.web}\n{venue.email_address}\n{venue.phone}\n\n\n')
    response.writelines(lines)
    # lines = ["This is line 1\n",
    #          "This is line 2\n",
    #          "This is line 3\n"]
    # response.writelines(lines)
    return response

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venues')

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {
        'event': event,
        'form': form,
    })

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',{
        'form': form,
        'submitted': submitted
    })


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venues')
    return render(request, 'events/update_venue.html', {
        'venue': venue,
        'form': form,
    })

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {
            'searched': searched,
            'venues': venues,
        })
    else:
        return render(request, 'events/search_venues.html', )


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {
        'venue': venue
    })

def all_events(request):
    event_list = Event.objects.all().order_by('event_date',)

    return render(request, 'events/event_list.html', {
        'event_list' : event_list
    })

def venues(request):
    venue_list = Venue.objects.all().order_by('name')
    # Set up pagination
    p = Paginator(venue_list, 3)
    page = request.GET.get('page')
    venues = p.get_page(page)
    #nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venue.html', {
        'venue_list' : venue_list,
        'venues': venues,
    })



def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',{
        'form': form,
        'submitted': submitted
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Mattias"
    #Convert month from name to number
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #Create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    #Get current
    now = datetime.now()
    current_year = now.year
    current_time = now.strftime('%H:%M:%S %p')

    return render(request, 'events/home.html', {
        "name" : name,
        "year" : year,
        "month" : month,
        "month_number" : month_number,
        "cal" : cal,
        "current_year" : current_year,
        "current_time" : current_time,
    })
