"""
https://github.com/Flightradar24/fr24api-sdk-python/blob/main/examples/basic_usage.py
with Client(os.environ["FR24_API_TOKEN"]) as client:
    #light_positions = client.live.flight_positions.get_full(bounds="6.000,8.000,46.000,48.000")
    #light_positions = client.live.flight_positions.get_full(flights='all')
    #light_positions = client.live.flight_positions.get_full(flights=" [type=list_type, input_value='SAA280,UAL2222', input_ty
    #ata = client.live.flight_positions.get_full(bounds="50.682,46.218,14.422,22.243")
    #ata = client.live.flight_positions.get_full(airports=['ORD'],limit=3)
    #ata = client.live.flight_positions.get_full(altitude_ranges=['30000.00-33999.00'],limit=3)
    data = client.live.flight_positions.get_full(operating_as=['SAS'],limit=3)
    #ata = client.live.flight_positions.get_full(flights=['UA33'],limit=3)
    data = client.live.flight_positions.get_full(categories=[FlightCategory.CARGO],limit=3,timestamp=datetime(2026, 9,29, 0, 0, 0, tzinfo=timezone.utc))
"""
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import ( get_object_or_404, redirect, render)
from django.views.generic import View

from .models import Flight,  Bounds, Airport, Category, Altitude, FNo, OperatingAs, \
        Airspace, Route, Aircraft, Ebola, EbolaTest
from django.conf import settings
import requests
import time
from datetime import datetime, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from zoneinfo import ZoneInfo
from typing import Union
import pytz
#rom dateutil import parser
from typing import Tuple
import random
import subprocess
from django.shortcuts import redirect, render
from .forms import BoundsForm, AirportForm, CategoryForm, AltitudeForm, FNoForm, \
        OperatingAsForm, AirspaceForm, RouteForm, AircraftForm
from django.shortcuts import render, get_object_or_404, redirect
import math, os

#rom .tasks import send_invoice_email
from django.contrib.auth import login
#rom .tasks import send_welcome_email
#mport django-rq
from multipledispatch import dispatch
from fr24sdk.client import Client
from fr24sdk.models.geographic import AltitudeRange, Boundary
#rom fr24sdk import FR24Error, FR24RateLimitError, FR24NotFoundError, FR24AuthenticationError
#rom pyfr24 import FR24API, configure_logging, FR24Error, FR24NotFoundError
#rom pyfr24 import FR24API, configure_logging, FR24Error, FR24NotFoundError
from django.urls import reverse
#rom FlightRadar24 import FlightRadar24API
#rom django_never_cache.mixins import NoCacheMixin
#rom django_never_cache.decorators import allow_cache
# Source - https://stackoverflow.com/a/62213724
# Posted by Chris
# Retrieved 2026-01-23, License - CC BY-SA 4.0

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Count

from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.db.models.functions import TruncDate
from django.db.models import Q

from django.db import connection
from django.http import HttpResponse
import asyncio
import websockets

from django.core.handlers.wsgi import WSGIRequest
from functools import wraps
from django.core.cache import cache

try:
  TEMPLATE_RECALC=os.environ["TEMPLATE_RECALC"] # how often template should calc plane location
except KeyError:
  TEMPLATE_RECALC=2000
  print('90b',TEMPLATE_RECALC)

def serve_meteorite_csv(request):
    print('09c serve_meteorite_csv')
    # Path to where the CSV actually lives on your PA storage

def ol2(request):
    print('09d ol2 view fired')
    return render(request, "app2/index.html", {})

def ebola_time_map(request):
    print('91l ebola_time_map')
    result = (
        Ebola.objects
        .annotate(datee=TruncDate('created_at')) .values('datee') .annotate(count=Count('id')) .order_by('datee')
    )
    formatted_result = [ f"{row['datee'].strftime('%Y-%m-%d')}: {row['count']:>6} cases" for row in result ]
    #we're not doing anything with the context (this is a vestige of a simple Django prototype):
    #the template just draws a map, then calls the ebola_time_series view for geojson-format data to draw
    #ontext = { 'formatted_result': formatted_result, }
    context = {}
    return render(request, "app2/ebola_animated.html",context)


from django.http import HttpResponse
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import F, Value
from django.db.models.functions import TruncDate, JSONObject
import json

#1) json dumps (limit 30)
from django.contrib.postgres.aggregates import JSONBAgg
from django.db.models import F, Value, Func
from django.db.models.functions import TruncDate, JSONObject
from django.http import HttpResponse

# Helper class to build [lon, lat] JSON arrays in PostgreSQL
class JSONArray(Func):
    function = 'jsonb_build_array'
    output_field = None

#6) simplified (created ebola_daily_geojson)
def ebola_time_series(request):
    print('85i ebola_time_series() ')
    raw_query = """
        SELECT json_build_object(
            'days', json_agg(
                json_build_object('date', day_str, 'features', day_features)
                ORDER BY day_str
            )
        )::text
        FROM ebola_daily_geojson;
    """
    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        json_data = cursor.fetchone()[0] or '{"days": []}'
        """
        print('85m',json_data[:100])
        y = json.loads(json_data)
        print('85q',type(y))
        l2=y["days"]
        print('85r',type(l2))
        ctr=0
        for x in l2:
            ctr+=1
            if ctr>70:
                print('85u',x)
        print('85v count:',ctr)
        """

    return HttpResponse(json_data, content_type="application/json")

#1) orm
def ebola_time_series_orm(request):
    day_summaries = (
        Ebola.objects
        .filter(cas_sus__gt=0)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(
            features=JSONBAgg(
                JSONObject(
                    type=Value("Feature"),
                    geometry=JSONObject(
                        type=Value("Point"),
                        coordinates=JSONArray(F("lon"), F("lat"))
                    ),
                    properties=JSONObject(
                        id=F("id"),
                        created_at=F("created_at"),
                        cas_sus=F("cas_sus")
                    )
                )
            )
        )
        .order_by("day")
    )

    days = [
        {"date": row["day"].isoformat(), "features": row["features"]}
        for row in day_summaries
    ]

    return HttpResponse(json.dumps({"days": days}, default=str), content_type="application/json")

from datetime import datetime
from django.db import connection
from django.http import HttpResponse

#2) raw SQL w/ index 
def ebola_time_series_index(request):
    print('04f starting raw SQL', datetime.now())

    raw_query = """
        SELECT json_build_object(
            'days', json_agg(
                json_build_object(
                    'date', day_str,
                    'features', day_features
                ) ORDER BY day_str
            )
        )::text AS json_payload
        FROM (
            SELECT
                ((created_at AT TIME ZONE 'UTC')::date)::text AS day_str,
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', json_build_object(
                            'type', 'Point',
                            'coordinates', json_build_array(lon, lat)
                        ),
                        'properties', json_build_object(
                            'id', id,
                            'created_at', to_char(created_at, 'YYYY-MM-DD"T"HH24:MI:SS'),
                            'cas_sus', cas_sus
                        )
                    )
                ) AS day_features
            FROM app2_ebola
            WHERE cas_sus > 0
            GROUP BY (created_at AT TIME ZONE 'UTC')::date
            ORDER BY (created_at AT TIME ZONE 'UTC')::date
        ) sub;
    """
    print('04h          raw SQL', datetime.now())

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        row = cursor.fetchone()
        json_data = row[0] if row and row[0] else '{"days": []}'

    print('04u done     raw SQL', datetime.now())

    return HttpResponse(json_data, content_type="application/json")

#3) raw SQL 
def ebola_time_series_raw(request):
    print('07f starting raw SQL',datetime.now())
    raw_query = """
        SELECT json_build_object(
            'days', json_agg(
                json_build_object(
                    'date', day_str,
                    'features', day_features
                ) ORDER BY day_str
            )
        )
        FROM (
            SELECT
                to_char(created_at, 'YYYY-MM-DD') AS day_str,
                json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', json_build_object(
                            'type', 'Point',
                            'coordinates', json_build_array(lon, lat)
                        ),
                        'properties', json_build_object(
                            'id', id,
                            'created_at', to_char(created_at, 'YYYY-MM-DD"T"HH24:MI:SS'),
                            'cas_sus', COALESCE(cas_sus, 0)
                        )
                    )
                ) AS day_features
            FROM app2_ebola
            WHERE cas_sus > 0
            GROUP BY to_char(created_at, 'YYYY-MM-DD')
            ORDER BY day_str
        ) sub;
    """
    print('07h          raw SQL',datetime.now())

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        json_data = cursor.fetchone()[0]
    #rint('07u donee    raw SQL',json_data)

    # Return the raw JSON string directly from Postgres without Python serialization
    return HttpResponse(json_data, content_type="application/json")



#4) single loop 4 seconds 
def ebola_time_series_one(request):
    # Fetch only the exact columns needed as raw dicts
    rows = (
        Ebola.objects
        .filter(cas_sus__gt=0)
        .annotate(day=TruncDate("created_at"))
        .values("id", "day", "lon", "lat", "cas_sus", "created_at")
        .order_by("day")
    )
    grouped = {}
    print('53u raw rows start looping',datetime.now())
    for r in rows:
        d = r["day"].isoformat()
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [r["lon"], r["lat"]]
            },
            "properties": {
                "id": r["id"],
                "created_at": r["created_at"].isoformat() if r["created_at"] else d,
                "cas_sus": float(r["cas_sus"]) if r["cas_sus"] is not None else 0.0,
            }
        }
        grouped.setdefault(d, []).append(feature)
    print('53v raw rows done  looping',datetime.now())
    timeline = [{"date": d, "features": feats} for d, feats in grouped.items()]
    """
    timeline is list of tuples containing two members: date and features
    features is list of dicts
    each dict contains type, geometry and properties
    each geometry contains 'Point' and coordinates
    properties contains three fields: id, created_at and cas_sus
    """
    return JsonResponse({"days": timeline})

#5) two loops 
def ebola_time_series_two(request):
    qs = (
        Ebola.objects
        .only("lon", "lat", "created_at", "cas_sus")
        .filter(cas_sus__gt=0)
        .annotate(day=TruncDate("created_at"))  # group by created_at date
        .order_by("day")
    )
    """
    for x in qs:
        print('09q',x.created_at,x.cas_sus,x.lat,x.lon)
    """

    grouped = {}

    for obj in qs:
        d = obj.day.isoformat()
        grouped.setdefault(d, []).append(obj)
    # grouped is dict - key is day, values is list of Ebola instances

    days = []
    for day, objs in grouped.items():
        features = []
        for o in objs:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [o.lon, o.lat]
                },
                "properties": {
                    "id": o.id,
                    "created_at": o.created_at.isoformat() if o.created_at else day,
                    "cas_sus": float(o.cas_sus) if o.cas_sus is not None else 0.0, # 🌟 ADD THIS
                }
            })
        days.append({"date": day, "features": features})

    """
    days is list of tuples containing two members: date and features
    features is list of dicts
    each dict contains type, geometry and properties
    each geometry contains 'Point' and coordinates
    properties contains three fields: id, created_at and cas_sus
    """
    return JsonResponse({"days": days})

def ebola_time_fake_work3(request):
    qs = Ebola.objects.filter(fake=True).order_by("distance")

    bucket_size = 0.05  # ~5 km if your units are degrees
    buckets = {}

    for row in qs:
        shell = round(row.distance / bucket_size)
        buckets.setdefault(shell, [])
        buckets[shell].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.lon, row.lat],
            },
            "properties": {
                "admin1": row.admin1,
                "sus": row.cas_sus,
                "conf": row.cas_conf,
                "dec": row.decas_conf,
                "distance": row.distance,
            }
        })

    timeline = [{"shell": s, "features": f} for s, f in sorted(buckets.items())]
    return JsonResponse({"days": timeline})

def ebola_time_flash(request):
    #s = Ebola.objects.filter(fake=True).annotate(day=TruncDate("reported_at"))
    qs = Ebola.objects.all().annotate(day=TruncDate("reported_at"))

    grouped = {}
    for row in qs:
        d = str(row.day)
        grouped.setdefault(d, [])
        grouped[d].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.lon, row.lat],
            },
            "properties": {
                "admin1": row.admin1,
                "sus": row.cas_sus,
                "conf": row.cas_conf,
                "dec": row.decas_conf,
            }
        })


    timeline = [{"date": d, "features": f} for d, f in sorted(grouped.items())]
    jr = JsonResponse({"days": timeline})
    print('01f jr',jr)
    return jr

def refresh():
    #esult = send_welcome_email("michael_sweeney303@gmail.com")
    #esult = django_rq()
    result = subprocess.run(['python', 'ree/fr24_background.py'], capture_output=True, text=True)
    print('93b result: ',result)

def update_route(request):
    if request.method == 'POST':
      print('09b POST !!!')
      rf=RouteForm(request.POST)
      if rf.is_valid():
        rf.save()
        count=update_flight_table(rf,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'route'
        request.session.save()
        print('09p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('08q GET !!!')
      rf=RouteForm()
    return render(request, "app2/route_template.html",{"form":rf})


def update_airspace(request):
    if request.method == 'POST':
      af=AirspaceForm(request.POST)
      #f.created_at=datetime.now()
      if af.is_valid():
        af.save()
        count=update_flight_table(af,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'airspace'
        request.session.save()
        print('89p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('89q GET !!!')
      af=AirspaceForm()
    return render(request, "app2/airspace_template.html",{"form":af})

def update_operating_as(request):
    if request.method == 'POST':
      of=OperatingAsForm(request.POST)
      #f.created_at=datetime.now()
      if of.is_valid():
        of.save()
        print('88n',of.cleaned_data)
        print('88o',of.errors)
        count=update_flight_table(of,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'operating_as'
        request.session.save()
        print('88p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('88q GET !!!')
      of=OperatingAsForm()
    return render(request, "app2/operating_as_template.html",{"form":of})

def update_fno(request):
    #no = FNo.objects.get(id=1)
    if request.method == 'POST':
      ff=FNoForm(request.POST)
      #f.created_at=datetime.now()
      if ff.is_valid():
        ff.save()
        count=update_flight_table(ff,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'fno'
        request.session.save()
        print('78p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('78q GET !!!')
      ff=FNoForm()
    return render(request, "app2/fno_template.html",{"form":ff})

def update_altitude(request):
    if request.method == 'POST':
      print('71b POST !!!')
      af=AltitudeForm(request.POST)
      #f.created_at=datetime.now()
      if af.is_valid():
        af.save()
        count=update_flight_table(af,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'altitude'
        request.session.save()
        print('71p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('28q GET !!!')
      af=AltitudeForm()
    return render(request, "app2/altitude_template.html",{"form":af})

def update_aircraft(request):
    if request.method == 'POST':
      print('18b POST !!!')
      af=AircraftForm(request.POST)
      if af.is_valid():
        af.save()
        count=update_flight_table(af,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'aircraft'
        request.session.save()
        print('18p update_flight_table() called but nothing updated')
        #eturn HttpResponseRedirect("/rare/")saved!!!')
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('18q GET !!!')
      af=AircraftForm()
    return render(request, "app2/aircraft_template.html",{"form":af})

def update_category(request):
    #ategory = Category.objects.get(id=1)
    if request.method == 'POST':
      cf=CategoryForm(request.POST)
      #f.created_at=datetime.now()
      if cf.is_valid():
        cf.save()
        count=update_flight_table(cf,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'category'
        request.session.save()
        print('08p saved!!!')
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('08q GET !!!')
      cf=CategoryForm()
    return render(request, "app2/category_template.html",{"form":cf})

def update_airport(request):
    #irport = Airport.objects.get(id=1)
    if request.method == 'POST':
      print('07a request.POST.keys', dir(request.POST.keys))
      print('07b request.POST.values', dir(request.POST.values))
      af=AirportForm(request.POST)
      print('07c my_form.errors:',af.errors)
      print('07m type(af)',type(af))
      print('07n dir(af)',dir(af))
      #f.created_at=datetime.now()
      if af.is_valid():
        print('07e my_form.cleaned_data',af.cleaned_data)
        print('07f my_form.data',af.data)
        instance = af.save(commit=False)
        # problem: Django was plugging default 0 into dir2 field no matter what they choose.
        # next 3 lines provide manual fix (also fields dir2 and iata must be defined in form)
        instance.dir2 = af.cleaned_data['dir2']
        print(f"07g instance.dir2 (instance is returned by my_form.save()): {instance.dir2}")
        instance.save()
        # above 3 lines maybe needed if Django writing default 0 no matter what

        count=update_flight_table(af,request)
        print('55w',request.session.session_key)
        request.session['criterion'] = 'airport'
        request.session.save()
        #egister_user(request)
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
    else:
      print('07q GET !!!')
      af=AirportForm()
    return render(request, "app2/airport_template.html",{"form":af})

def update_bounds(request):
    #ounds = Bounds.objects.get(id=1)
    if request.method == 'POST':
      bf=BoundsForm(request.POST)
      #f.created_at=datetime.now()
      if bf.is_valid():
        bf.save()
        count=update_flight_table(bf,request)
        request.session['criterion'] = 'bounds'
        request.session.save()
        #egister_user(request)
        #eturn HttpResponseRedirect("/rare/")
        return HttpResponseRedirect(reverse('flight_view') + '?count='+str(count))
      print('03p saved!!!')
      print('03s redirecting')
      return HttpResponseRedirect("/rare/")
    else:
      print('04d GET !!!')
      bf=BoundsForm()
    return render(request, "app2/bounds_template.html",{"form":bf})


def random_airport():
  index=int(49 * random.random()) #50 airports
  iata = list(airports.keys())[index]
  coords=airports[iata]
  return (iata,coords)

airports = {
    # North America
    'ATL': (33.6407, -84.4277),  # Hartsfield–Jackson Atlanta International Airport
    'DFW': (32.8998, -97.0403),  # Dallas/Fort Worth International Airport
    'DEN': (39.8561, -104.6737), # Denver International Airport
    'ORD': (41.9742, -87.9073),  # O'Hare International Airport (Chicago)
    'LAX': (33.9425, -118.4080), # Los Angeles International Airport
    'JFK': (40.6413, -73.7781),  # John F. Kennedy International Airport (New York)
    'LAS': (36.0840, -115.1537), # Harry Reid International Airport (Las Vegas)
    'CLT': (35.2144, -80.9431),  # Charlotte Douglas International Airport
    'MCO': (28.4294, -81.3089),  # Orlando International Airport
    'MIA': (25.7959, -80.2871),  # Miami International Airport
    'PHX': (33.4343, -112.0117), # Phoenix Sky Harbor International Airport
    'SFO': (37.6213, -122.3790), # San Francisco International Airport
    'SEA': (47.4502, -122.3088), # Seattle–Tacoma International Airport
    'BOS': (42.3643, -71.0052),  # Logan International Airport (Boston)
    'IAD': (38.9445, -77.4558),  # Washington Dulles International Airport
    'EWR': (40.6895, -74.1745),  # Newark Liberty International Airport
    'FLL': (26.0717, -80.1384),  # Fort Lauderdale–Hollywood International Airport
    'DTW': (42.2162, -83.3554),  # Detroit Metropolitan Airport
    'MSP': (44.8820, -93.2217),  # Minneapolis–Saint Paul International Airport
    'PHL': (39.8720, -75.2411),  # Philadelphia International Airport
    'CUN': (21.0366, -86.8770),  # Cancún International Airport (Mexico)
    'YYZ': (43.6777, -79.6248),  # Toronto Pearson International Airport (Canada)

    # Europe & Middle East
    'DXB': (25.2532, 55.3656),   # Dubai International Airport (UAE)
    'LHR': (51.4700, -0.4543),   # London Heathrow Airport (UK)
    'IST': (41.2753, 28.7408),   # Istanbul Airport (Turkey)
    'CDG': (49.0097, 2.5479),    # Charles de Gaulle Airport (Paris, France)
    'AMS': (52.3086, 4.7639),    # Amsterdam Airport Schiphol (Netherlands)
    'MAD': (40.4839, -3.5679),   # Adolfo Suárez Madrid–Barajas Airport (Spain)
    'FRA': (50.0379, 8.5622),    # Frankfurt Airport (Germany)
    'DOH': (25.2730, 51.6038),   # Hamad International Airport (Doha, Qatar)
    'FCO': (41.8003, 12.2389),   # Leonardo da Vinci–Fiumicino Airport (Rome, Italy)
    'MUC': (48.3537, 11.7861),   # Munich Airport (Germany)
    'BCN': (41.3005, 2.0762),    # Barcelona–El Prat Airport (Spain)

    # Asia & Oceania
    'HND': (35.5494, 139.7798),  # Tokyo Haneda Airport (Japan)
    'PVG': (31.1434, 121.8053),  # Shanghai Pudong International Airport (China)
    'DEL': (28.5666, 77.1003),   # Indira Gandhi International Airport (Delhi, India)
    'CAN': (23.3980, 113.3130),  # Guangzhou Baiyun International Airport (China)
    'ICN': (37.4691, 126.4510),  # Seoul Incheon International Airport (South Korea)
    'SIN': (1.3592, 103.9897),   # Singapore Changi Airport (Singapore)
    'PEK': (40.0799, 116.6031),  # Beijing Capital International Airport (China)
    'BKK': (13.6811, 100.7473),  # Suvarnabhumi Airport (Bangkok, Thailand)
    'KUL': (2.7456, 101.7088),   # Kuala Lumpur International Airport (Malaysia)
    'SZX': (22.6393, 113.8118),  # Shenzhen Bao'an International Airport (China)
    'TFU': (30.3340, 104.4280),  # Chengdu Tianfu International Airport (China)
    'CGK': (-6.1256, 106.6559),  # Soekarno–Hatta International Airport (Jakarta, Indonesia)
    'BOM': (19.0888, 72.8681),   # Chhatrapati Shivaji Maharaj International Airport (Mumbai, India)
    'HKG': (22.3080, 113.9189),  # Hong Kong International Airport (Hong Kong)
    'SYD': (-33.9461, 151.1772), # Sydney Airport (Australia)
    'MEL': (-37.6733, 144.8433),  # Melbourne Airport (Australia)
    'NNG': (22.8167, 108.3275)   # Chhatrapati Shivaji International (Sahar International) (added 11/5/25)
}
params = {
  'access_key': '4d27ba3cd6c277e07fa024419858e843', #aviationstack.com
  'limit': 1
}
def maps_view(request):
    return render(request, 'googleMap.html', {'google_maps_api_key': settings.GOOGLE_API_KEY})

#######
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from app2.models import Ebola

def red_geojson(request):
    qs = EbolaCase.objects.filter(case_status='confirmed')
    return HttpResponse(serializers.serialize('geojson', qs), content_type='application/json')

def blue_geojson(request):
    qs = EbolaCase.objects.filter(case_status='suspected')
    return HttpResponse(serializers.serialize('geojson', qs), content_type='application/json')

def ebola_test_geojson(request):
    print('34m ebola_test_geojson');
    features = []
    ctr=0

    for row in Ebola.objects.order_by("created_at"):
        bad=False
        for field in row._meta.fields:
            val = getattr(row, field.name)
            if isinstance(val, float) and math.isnan(val):
                print(f"13s dropping row {row.id} field '{field.name}' is NaN")
                bad=True
        if bad:
          continue
        ctr+=1
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row.lon, row.lat],
            },
            "properties": {
                "admin1": row.admin1,
                "admin2": row.admin2,
                "admin3": row.admin3,
                "cas_sus": row.cas_sus,
                "cas_conf": row.cas_conf,
                "decas_conf": row.decas_conf,
                #created_at": row.created_at.isoformat(), not in Ebola
            }
        })

    print('35r ctr',ctr)
    return JsonResponse({
        "type": "FeatureCollection",
        "features": features
    })


#######
class OLView(View):
    template_name = "app2/ol_map.html"

    def get(self, request):
        print('48b OLView')
        print('32j rendering unto Caesar')
        return render(request, self.template_name)

#######

#######
class EbolaView(View):
    template_name = "app2/ebola_map.html"

    def get(self, request):
        print('47b EbolaView')
        # If the request asks for JSON, return JSON
        #f request.headers.get("x-requested-with") == "XMLHttpRequest":
        """
        if False:
            features = []
            for obj in EbolaTest.objects.all():
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [obj.lon, obj.lat],
                    },
                    "properties": {
                        "admin1": obj.admin1,
                        "admin2": obj.admin2,
                        "admin3": obj.admin3,
                        "cas_sus": obj.cas_sus,
                        "cas_conf": obj.cas_conf,
                    }
                })
            return JsonResponse({
                "type": "FeatureCollection",
                "features": features
            })

        """
        # Otherwise return the HTML map page
        print('32j rendering unto Caesar')
        return render(request, self.template_name)

class AISView(View):
    async def stream(self):
        api_key = settings.AISSTREAM_API_KEY
        if not api_key:
            raise ValueError("02c AISSTREAM_API_KEY is not set.")
        messages = []
        async with websockets.connect(
            "wss://stream.aisstream.io/v0/stream",
            compression="deflate",
        ) as ws:
            await ws.send(json.dumps({
                "APIKey": api_key,
                "BoundingBoxes": [[[25.835, -80.208], [25.603, -79.879]]],
                "FilterMessageTypes": ["PositionReport"]
            }))
            async for payload in ws:
                data = json.loads(payload)
                print("09a received:", data)
                if data.get("MessageType") == "SubscriptionConfirmation":
                    print('08g')
                    continue
                messages.append(data)
                print('09o',messages)
                if len(messages) >= 3:
                    print('08h')
                    break
        return messages

    def get(self, request):
        messages = asyncio.run(self.stream())
        return JsonResponse({"status": "ok", "ships": messages})

class AISView5(View):
    async def stream(self):
        api_key = settings.AISSTREAM_API_KEY
        if not api_key:
            raise ValueError("02c AISSTREAM_API_KEY is not set.")

        #eturn '07a'
        messages = []
        async with websockets.connect(
            "wss://stream.aisstream.io/v0/stream",
            compression="deflate",
        ) as ws:
            await ws.send(json.dumps({
                "APIKey": api_key,
                "BoundingBoxes": [[[35.160, 129.055], [35.200, 129.095]]],
                "FilterMessageTypes": ["PositionReport"]
            }))

            # Read up to 5 messages, then exit the loop
            async for payload in ws:
                data = json.loads(payload)
                messages.append(data)
                print("08b received AIS packet:", data)
                #f len(messages) >= 5:
                if True:
                    print("08e bailing")
                    break

        return messages

    def get(self, request):
        print('06a')
        messages = asyncio.run(self.stream())
        AISSTREAM_API_KEY = '366b1dbea14c9bee11b88820825e46a098711950'
        return HttpResponse(messages)

class AISView1(View):
    def get(self, request):
        return HttpResponse("Streaming complete")


class AISView2(View):
    async def stream(self):
        #pi_key = os.environ.get("AISSTREAM_API_KEY")
        api_key = settings.AISSTREAM_API_KEY
        if not api_key:
            raise ValueError("02c AISSTREAM_API_KEY is not set.")

        async with websockets.connect(
            "wss://stream.aisstream.io/v0/stream",
            compression="deflate",
        ) as ws:
            await ws.send(json.dumps({
                "APIKey": api_key,
                "BoundingBoxes": [[[35.160, 129.055], [35.200, 129.095]]],
                "FilterMessageTypes": ["PositionReport"]
            }))
            async for payload in ws:
                print(json.loads(payload))

    def get(self, request):
        print('04a AISView')
        #syncio.run(self.stream())
        print('04m AISView')
        return HttpResponse("Streaming complete")

#ef flight_view(request):
#method_decorator(allow_cache, name="dispatch")
decorators = [never_cache,]
#method_decorator(decorators, name='dispatch')
class FlightView(View):
  def get(self, request):
    print('11g FlightView get()')
    flight_list = []
    # update Flight model before correcting airplane locations in template:
    try:
      #rint('55x',request.session.session_key)
      criterion=request.session.get('criterion')
      #rint('55t',criterion)
      update_flight_table(criterion,request) #criterion is a string so we need to overload update_flight_table
    except KeyError:
      criterion = None
      print('91p request.session.get(criterion) returned ',type(criterion))

    flights=Flight.objects.all()
    for flight in flights:
        flight_dict={'callsign':flight.callsign,'latitude':flight.latitude, \
                'longitude':flight.longitude, \
                #timee':flight.timee, \
                'velocity':flight.velocity, \
                'geo_altitude':flight.geo_altitude, \
                'true_track':flight.true_track, \
                'dest_iata':flight.dest_iata, \
                'orig_iata':flight.orig_iata, \
                'squawk':flight.squawk, \
                'eta':flight.eta, \
                'noww':flight.noww, \
                'flightno':flight.flightno}
        #rint('12b flight_dict:',flight_dict)
        flight_list.append(flight_dict)
    #xtent=find_average_location_circular(flight_list) #center map to show all planeS
    extent=find_random_location(flight_list)
    #rint('09c calling calculate_zoom_factor() with: ',flight_list)
    #oom=calculate_zoom_factor(flight_list)
    #oom = calculate_max_zoom_for_locations(flight_list)
    zoom = 3 #show one plane close for effect
    print('18m',settings.GOOGLE_API_KEY)
    return render( request, 'app2/33_solid.html', {'settings.BASE_DIR':settings.BASE_DIR,'count':request.GET.get('count'),\
          'zoom':zoom,'extent':extent,'django_flights':flight_list, \
          'recalc': TEMPLATE_RECALC, 'active_criterion': criterion,'google_api_key':settings.GOOGLE_API_KEY})


def one_random():
    point_list = []
    start = random_airport()
    #rint('19e ',start[1])
    end   = random_airport()
    #rint('19f ',end[1])
    lat_range = end[1][0] - start[1][0]
    lng_range = end[1][1] - start[1][1]
    #rint('19s lat_range: ',lat_range)
    #rint('19t lng_range: ',lng_range)
    glimses=20
    ctr=0
    while ctr<glimses:
      ctr+=1
      lat_changing=start[1][0] + ctr*lat_range/glimses
      lng_changing=start[1][1] + ctr*lng_range/glimses
      #ng_changing=ctr*lng_range/glimses
      #rint('19x ',lat_changing)
      #rint('19y ',lng_changing)
      point = {"latitude":lat_changing,"longitude":lng_changing}
      point_list.append(point)
      #ime.sleep(1)
    return point_list





def calculate_current_location(
    dep_loc: Tuple[float, float],
    arr_loc: Tuple[float, float],
    dep_time: datetime,
    curr_time: datetime,
    arr_time: datetime
) -> Tuple[float, float]:
    # 1. Calculate the total time elapsed for the journey and the time elapsed so far



    total_duration = arr_time - dep_time
    print('08c ',total_duration)
    time_elapsed = curr_time - dep_time
    print('08d ',time_elapsed)

    # 2. Check for edge cases and division by zero
    if total_duration <= 0:
        # If departure and arrival are the same time, or invalid times,
        # return the departure location (or raise an error)
        return dep_loc

    # 3. Calculate the interpolation factor (alpha)
    # This is the fraction of the total journey completed (time-wise).
    alpha = time_elapsed / total_duration

    # Cap alpha between 0 and 1, in case current_time is outside the range
    alpha = max(0.0, min(1.0, alpha))

    # 4. Perform Linear Interpolation for latitude and longitude
    # dep_loc and arr_loc should be tuples of coordinates
    dep_lat = 100.000
    dep_lon = 50.00
    arr_lat = 75.00
    arr_lon = 25.00

    current_latitude = dep_lat + alpha * (arr_lat - dep_lat)
    current_longitude = dep_lon + alpha * (arr_lon - dep_lon)

    return (current_latitude, current_longitude)

def curl_request(url):
    command = ['curl', '-w -v -s', url]
    result = subprocess.run(command, capture_output=True, text=True)
    #md = ["curl", "https://example.com"]
    #esult = subprocess.run(cmd, capture_output=True, text=True)
    #eturn result.stdout
    return result

from django.http import HttpResponseRedirect
from django.shortcuts import render



def find_random_location(coordinates):
    #instead of zooming as close as possible to show all, let's zoom in on one to dramatize motion
    if not coordinates: #list of dicts {'latitude':1.000,'longitude':2.000,'whatever':5.5}
        return None
    sorted_lat = sorted(coordinates, key=lambda x: x['latitude'])
    count = len(coordinates)
    pick = sorted_lat[round(count/2)]
    return {"latitude":pick["latitude"],"longitude":pick["longitude"]}



def find_average_location(coordinates): #doesn't work for average -170 and 170 lat = Greenwich
    if not coordinates:
        return None

    # Initialize sums
    total_latitude = 0
    total_longitude = 0

    # hot-wire to instead show one plane up close instead of zoom in as close as can to show all
    typical_longitude = 0
    typical_longitude = 0

    # Get the number of coordinates
    count = len(coordinates)

    # Sum all latitudes and longitudes
    for coord in coordinates:
        total_latitude += coord['latitude']
        total_longitude += coord['longitude']

    # Calculate the average
    average_latitude = total_latitude / count
    average_longitude = total_longitude / count

    # Return the result as a new coordinate dictionary
    return {
        "latitude": average_latitude,
        "longitude": average_longitude
    }

    import math

def find_average_location_circular(coordinates):
    if not coordinates:
        return None

    # 1. Latitude (Simple Arithmetic Mean)
    total_latitude = sum(coord['latitude'] for coord in coordinates)

    # 2. Longitude (Vector Averaging for Circular Data)
    # Convert longitudes to radians and calculate the mean sine and cosine components
    sum_cos = 0
    sum_sin = 0

    for coord in coordinates:
        # Convert degrees to radians for math functions
        lon_rad = math.radians(coord['longitude'])

        sum_cos += math.cos(lon_rad)
        sum_sin += math.sin(lon_rad)

    count = len(coordinates)

    # Calculate the mean sine and cosine
    avg_cos = sum_cos / count
    avg_sin = sum_sin / count

    # Convert the mean vector back to an angle (longitude) using atan2
    # atan2(y, x) gives the angle in radians in the range (-pi, pi]
    average_longitude_rad = math.atan2(avg_sin, avg_cos)

    # Convert the result back to degrees
    average_longitude = math.degrees(average_longitude_rad)

    # 3. Final Average Location
    average_latitude = total_latitude / count

    return {
        "latitude": average_latitude,
        "longitude": average_longitude
    }


# Constants based on the Google/OpenStreetMap/Mercator tiling scheme
# World map is 256x256 pixels at zoom 0. Each zoom level doubles the map width.
WORLD_DIM = 256
MAX_ZOOM = 20

# A reasonable screen width/height for a map window (e.g., on a webpage)
# Used to determine how many tiles/pixels the map *should* cover.
MAP_PIXEL_WIDTH = 800  # Example screen width in pixels
MAP_PIXEL_HEIGHT = 600 # Example screen height in pixels
# Use a padding factor (e.g., 0.9) to ensure the bounding box fits with a margin
PADDING_FACTOR = 0.9

def calculate_zoom_factor(coordinates):
    if not coordinates:
        return None
    for d5 in coordinates:
        print('90c original latitude: ',d5["latitude"])
        print('90d original longitude:',d5["longitude"])

    # --- 1. Find the Bounding Box (Min/Max Lat/Lon) ---
    lats = [coord['latitude'] for coord in coordinates]
    lons = [coord['longitude'] for coord in coordinates]
    print('90f lats: ',lats)
    print('90g lons: ',lons)

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    print('90h min_lat: ',min_lat)
    print('90i max_lat: ',max_lat)
    print('90j min_lon: ',min_lon)
    print('90k max_lon: ',max_lon)

    # Calculate the center latitude for Mercator distortion correction
    center_lat = (min_lat + max_lat) / 2
    print('90l center_lat: ',center_lat)

    # Calculate the angular difference (span)
    # Longitude wrap-around correction is omitted for simplicity here,
    # as large spans often default to low zoom anyway (e.g., zoom 3 or 4)
    # For global spans > 180 deg, min_lon and max_lon will correctly capture the full 360 span.
    delta_lat = max_lat - min_lat
    delta_lon = max_lon - min_lon
    print('90m delta_lat: ',delta_lat)
    print('90n delta_lon: ',delta_lon)

    # If all points are the same, use a default high zoom (e.g., street level)
    if delta_lat < 1e-6 and delta_lon < 1e-6:
        return 15

    # --- 2. Calculate Zoom based on Latitude Span (Y-axis) ---
    # The Mercator projection distorts latitude linearly, but the degree-to-pixel
    # relationship is non-linear. We use the Mercator formula to convert lat/lon to
    # 'world pixel' coordinates and find the size of the bounding box.

    def lat_to_mercator_y(lat_deg):
        # Clip latitude to avoid atan(inf) near poles (~85.05 degrees)
        lat_rad = math.radians(max(-85.0511, min(85.0511, lat_deg)))
        # Standard Mercator formula (in radians/pi)
        return math.log(math.tan(math.pi / 4 + lat_rad / 2))

    # Calculate the vertical span in Mercator units at zoom 0 (full world size)
    print('90o lat_to_mercator_y(max_lat): ',lat_to_mercator_y(max_lat))
    print('90p lat_to_mercator_y(min_lat): ',lat_to_mercator_y(min_lat))
    delta_merc_y = abs(lat_to_mercator_y(max_lat) - lat_to_mercator_y(min_lat))
    print('90q difference between the mercators: ',delta_merc_y)

    # The world's Mercator Y-span is 2 * pi. At zoom Z, the map height is 2^Z * WORLD_DIM.
    # The world's vertical span in "world pixels" at zoom Z is (2^Z) * 256.
    # We want a zoom Z such that: (delta_merc_y / (2 * math.pi)) * (WORLD_DIM * 2^Z) 
    # <= MAP_PIXEL_HEIGHT
    # Rearranging for Z:
    print('91f WORLD_DIM ',WORLD_DIM) #256
    print('91g MAX_ZOOM ',MAX_ZOOM)
    print('91h PADDING_FACTOR: ',PADDING_FACTOR) #.9
    print('91i MAP_PIXEL_HEIGHT: ',MAP_PIXEL_HEIGHT) #600

    zoom_lat = math.log2((MAP_PIXEL_HEIGHT / WORLD_DIM / PADDING_FACTOR) 
            * (2 * math.pi / delta_merc_y))

    # --- 3. Calculate Zoom based on Longitude Span (X-axis) ---
    # Longitude is linear. 360 degrees map to WORLD_DIM * 2^Z pixels.
    # We want a zoom Z such that: (delta_lon / 360) * (WORLD_DIM * 2^Z) <= MAP_PIXEL_WIDTH
    # Rearranging for Z:
    zoom_lon = math.log2((MAP_PIXEL_WIDTH / WORLD_DIM / PADDING_FACTOR) * (360 / delta_lon))

    # --- 4. Determine Final Zoom ---
    # We must use the minimum zoom of the two (lat and lon) to ensure *both* fit.
    final_zoom = min(zoom_lat, zoom_lon)

    # Round down to the nearest integer and enforce min/max limits
    final_zoom_int = max(0, min(MAX_ZOOM, math.floor(final_zoom)))

    return final_zoom_int

# myapp/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
#rom .tasks import process_data_in_background
import uuid

@require_http_methods(["POST"])
def trigger_background_process(request):
    # 1. Get data/parameters needed by the background process
    user_id = request.user.id if request.user.is_authenticated else 999
    file_path = f"/data/uploads/{uuid.uuid4()}.csv"

    # 2. **SEND THE MESSAGE TO THE BROKER (Redis/RabbitMQ)**
    # .delay() is a shortcut for .apply_async() and is non-blocking.
    # It immediately returns an AsyncResult object.
    task_result = process_data_in_background.delay(user_id, file_path)

    # 3. Respond to the user immediately
    return JsonResponse({
        "status": "Task Queued",
        "message": "Processing started in the background.",
        "task_id": task_result.id  # You can use this ID to check status later
    }, status=202) # HTTP 202 Accepted status



def get_date(string_in):
    format = '%Y-%m-%dT%H:%M:%S'
    return datetime.datetime.strptime(string_in.rstrip('Z'), format)

def get_time(string_in):
    format_code = "%Y-%m-%dT%H:%M:%S"
    iso_format_string = string_in.replace('Z', '+00:00')
    datetime_object = datetime.fromisoformat(iso_format_string)
    return datetime_object.time()

def write_summary(response):
    print('62b write_summary (not write_positions)',type(response))
    fr_api = FlightRadarAPI()
    flights = response.data
    ctr=0
    for flight in flights:
      ctr+=1
      # Each 'flight' here is a FlightSummaryFull object
      print(f"62f flight ID: {flight.fr24_id}")
      print(f"62i flight Number: {flight.flight}")
      print(f"62m latitude: {flight.latitude}")
      print(f"62n latitude: {flight.longitude}")
      #et_flight_info(flight.fr24_id)
      id=flight.fr24_id
      flight = Flight(id)
      flight_details = fr_api.get_flight_details(flight)
      print('62m',flight_details)
    return ctr

def get_flight_info(flight_id):
    print('62h',flight_id)
    """
    async with FR24() as client:
        response = await client.flight_summary.fetch(flight_id)
        flight_info = response.to_dict()  # Convert response to dictionary
        print('62e',flight_info)
    """
    #ith Client(os.environ["FR24_API_TOKEN"]) as client:
    with FR24() as client:
      flight_info = client.flight_summary.fetch(flight_id)
      print('62j',flight_info)

# overloaded to expect noww for historic data
def write_positions(data,noww):
    print('60x',data)
    list2=json.loads(data.json())
    fr24s=list2["data"] 
    Flight.objects.all().delete() #empty out Flight table
    if len(fr24s)<1:
      print('48h bailing out - no planes')
      return 0
    ctr=0
    for x in fr24s:
      ctr+=1;
      fligh2=Flight(flightno=x["flight"],latitude=x["lat"],longitude=x["lon"], eta=x["eta"], callsign=x["callsign"], \
              timee=get_time(x["timestamp"]),geo_altitude=x["alt"],velocity=x["gspeed"], \
              true_track=x["track"], squawk=x["squawk"],orig_iata=x["orig_iata"],dest_iata=x["dest_iata"],noww=noww)
      fligh2.save()
      #rint('08x write_positions - ctr:',ctr)
    return ctr

def write_positions(data):
    print('60y',data)
    list2=json.loads(data.json())
    fr24s=list2["data"] 
    Flight.objects.all().delete() #empty out Flight table
    if len(fr24s)<1:
      print('48h bailing out - no planes')
      return 0
    ctr=0
    for x in fr24s:
      ctr+=1;
      fligh2=Flight(flightno=x["flight"],latitude=x["lat"],longitude=x["lon"], eta=x["eta"], callsign=x["callsign"], \
              timee=get_time(x["timestamp"]),geo_altitude=x["alt"],velocity=x["gspeed"], \
              true_track=x["track"], squawk=x["squawk"],orig_iata=x["orig_iata"],dest_iata=x["dest_iata"],noww=None)
      fligh2.save()
      #rint('08x write_positions - ctr:',ctr)
    return ctr

@dispatch(Route)
def hit_API(route:Route):
    s2=route.from2+"-"+route.to2
    print('19c hit_API() on Route: ',s2)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.live.flight_positions.get_full(routes=[s2],limit=10)
    return write_positions(data)


@dispatch(Altitude)
def hit_API(altitude:Altitude):
    s2=str(altitude.low)+"-"+str(altitude.high)
    min = s2.split('-', 1)[0]  
    max = s2.split('-', 1)[1]  
    print('59c hit_API() on Altitude: ',s2)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.live.flight_positions.get_full(altitude_ranges=[s2],limit=10)
    return write_positions(data)

@dispatch(Aircraft)
def hit_API(aircraft: Aircraft):
    print('09s aircraft:', aircraft.code)
    five_days_ago = datetime.now() - timedelta(days=5)
    three_days_ago = datetime.now() - timedelta(days=3)
    print('60c', aircraft.code)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      # Pass as a string, e.g. aircraft='A310' (or comma-separated string if multiple)
      data = client.live.flight_positions.get_full(aircraft=aircraft.code, limit=10)
      #ata = client.live.flight_positions.get_full(aircraft="A310,B77W,A359", limit=10)
    print('61x', type(data))
    return write_positions(data)  # Plural write_positions

@dispatch(Category)
def hit_API(category:Category):
    print('55b',category.code)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.live.flight_positions.get_full(categories=[category.code],limit=10)
    return write_positions(data)

@dispatch(OperatingAs)
def hit_API(operating_as:OperatingAs):
    print('75b hit_API() on OperatingAs',operating_as.oa)
    try:
      with Client(os.environ["FR24_API_TOKEN"]) as client:
        data = client.live.flight_positions.get_full(operating_as=[operating_as.oa],limit=10)
      print('75c get_full on FR24 returned',data)
      return write_positions(data)
    except:
      print("75e error hitting API with operating_as criterion",operating_as.oa)
      return 0

@dispatch(Airspace)
def hit_API(airspace:Airspace):
    print('77b hit_API() on Airspace')
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.live.flight_positions.get_full(airspaces=[airspace.airsp],limit=10)
    return write_positions(data)


@dispatch(FNo,WSGIRequest)
def hit_API(fno:FNo,request:WSGIRequest):
    print('65b hit_API() on FNo')
    try:
      with Client(os.environ["FR24_API_TOKEN"]) as client:
        data = client.live.flight_positions.get_full(flights=[fno.flightno],limit=10)
      return write_positions(data)
    except:
      print("95e error hitting API with fno criterion",fno.flightno)
      return 0

# not called:
@dispatch(FNo,WSGIRequest)
def zit_API(fno:FNo,request:WSGIRequest):
    dt1 = datetime(2026, 9, 30, 5, 22, 27, tzinfo=timezone.utc)

    #
    now = time.time()
    last_hit = request.session.get('last_hit_ts')
    if last_hit and (now - last_hit > 30):
        request.session.pop('dt38', None)

    request.session['last_hit_ts'] = now
    #
    dt38_str = request.session.get('dt38')
    if dt38_str:
        print('25g retrieved dt38_str:', dt38_str)
        dt38 = datetime.fromisoformat(dt38_str)
    else:
        print('25h no session found, starting over with dt1')
        dt38 = dt1

    # 2. Increment and save for the next run
    dt38 = dt38 + timedelta(seconds=1)
    request.session['dt38'] = dt38.isoformat()
    request.session.set_expiry(0)

    try:
      with Client(os.environ["FR24_API_TOKEN"]) as client:
        #ata = client.historic.flight_positions.get_full(flights=[fno.flightno], timestamp=datetime(2026, 9,30,5,22,30, tzinfo=timezone.utc))
        data = client.historic.flight_positions.get_full(flights=[fno.flightno], timestamp=dt38)
      return write_positions(data,dt38)
    except:
      print("65e error hitting API with fno criterion",fno.flightno)
      return 0

@dispatch(Airport)
def hit_API(airport:Airport):
    print('65c',airport.iata)
    if airport.dir2==1: #match case will kick in version 10
      s4='inbound:'+airport.iata
    elif airport.dir2==2:
      s4='both:'+airport.iata
    elif airport.dir2==3:
      s4='outbound:'+airport.iata
    else:
        s4='both:'+airport.iata
    print('95b hitting API with airports=',s4)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
        data = client.live.flight_positions.get_full(airports=[s4],limit=10)
    return write_positions(data)

@dispatch(Bounds)
def hit_API(bounds: Bounds):
    print('85b hit_API() on Bounds')
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.live.flight_positions.get_full(bounds=str(bounds.north)+','+str(bounds.south)+','
              +str(bounds.west)+','+str(bounds.east),limit=10)
    return write_positions(data)

def update_flight_table(what,request):
    #rint('56a update_flight_table',what)
    if isinstance(what,BoundsForm) or (isinstance(what, str) and what == 'bounds'):
      print('56j hitting bounds')
      bounds=Bounds.objects.order_by('-created_at').first()
      return hit_API(bounds)
    elif isinstance(what,RouteForm) or (isinstance(what, str) and what == 'route'):
      print('56z hitting route')
      route=Route.objects.order_by('-id').first()
      return hit_API(route)
    elif isinstance(what,AirportForm) or (isinstance(what, str) and what == 'airport'):
      print('56k hitting airport')
      airport=Airport.objects.order_by('-created_at').first()
      return hit_API(airport)
    elif isinstance(what,AirspaceForm) or (isinstance(what, str) and what == 'airspace'):
      airspace=Airspace.objects.order_by('-id').first()
      print('56f hitting airspace',type(airspace))
      return hit_API(airspace)
    elif isinstance(what,FNoForm) or (isinstance(what, str) and what == 'fno'):
      fno=FNo.objects.order_by('-id').first()
      print('56s hitting fno',type(fno))
      return hit_API(fno,request)
    elif isinstance(what,OperatingAsForm) or (isinstance(what, str) and what == 'operating_as'):
      operating_as=OperatingAs.objects.order_by('-id').first()
      print('56r hitting operating_as',type(operating_as))
      return hit_API(operating_as)
    elif isinstance(what,AltitudeForm) or (isinstance(what, str) and what == 'altitude'):
      altitude=Altitude.objects.order_by('-id').first()
      print('56p hitting altitude',type(altitude))
      return hit_API(altitude)
    elif isinstance(what,AircraftForm) or (isinstance(what, str) and what == 'aircraft'):
      aircraft=Aircraft.objects.order_by('-id').first()
      print('56t hitting aircraft',aircraft)
      return hit_API(aircraft)
    elif isinstance(what,CategoryForm) or (isinstance(what, str) and what == 'category'):
      print('56l hitting category')
      category=Category.objects.order_by('-created_at').first()
      return hit_API(category)
    else:
      print('56m update_flight_table() did nothing')
      return 0

def calculate_max_zoom_for_locations(locations, map_width_pixels=600, map_height_pixels=400):
    """
    Calculates the maximum Google Maps zoom factor (level) to show all
    provided locations within a map area of a given pixel size.

    Note: This is an approximation, as the exact calculation depends on
    the specific map implementation (API version, device DPI, padding, etc.).
    It uses a standard formula for the Mercator projection.

    Args:
        locations (list of tuples): A list of (latitude, longitude) tuples.
                                    E.g., [(40.7128, -74.0060), ...].
        map_width_pixels (int): The width of the map area in pixels (e.g., 600).
        map_height_pixels (int): The height of the map area in pixels (e.g., 400).

    Returns:
        int: The maximum integer zoom level (0-20, inclusive).
    """
    if not locations:
        return 0  # Zoom out fully for an empty list

    # 1. Find the geographic boundaries (bounding box)
    #in_lat = min(loc[0] for loc in locations)
    #ax_lat = max(loc[0] for loc in locations)
    #in_lon = min(loc[1] for loc in locations)
    #ax_lon = max(loc[1] for loc in locations)
    len2=len(locations)
    print('17y len(location): ',len(locations))
    sorted_lat = sorted(locations, key=lambda x: x['latitude'])
    sorted_lng = sorted(locations, key=lambda x: x['longitude'])
    #rint('18f sorted_lat: ',sorted_lat)
    #rint('18g sorted_lng: ',sorted_lng)
    min_lat=sorted_lat[0]["latitude"]
    max_lat=sorted_lat[len2-1]["latitude"]
    min_lon=sorted_lng[0]["longitude"]
    max_lon=sorted_lng[len2-1]["longitude"]
    #rint('10a min_lat: ',min_lat)
    #rint('10b max_lat: ',max_lat)
    #rint('10c min_lon: ',min_lon)

    # 2. Calculate the difference in degrees
    delta_lat = max_lat - min_lat
    #rint('103 delta_lat: ',delta_lat)
    # Handle longitude wrap-around (e.g., crossing the Antimeridian at 180/-180)
    delta_lon = max_lon - min_lon
    if delta_lon > 180:
        delta_lon = 360 - delta_lon

    # Global map size in pixels at zoom level 0 is 256x256
    TILE_SIZE = 256
    MAX_ZOOM = 20

    # Earth's circumference in meters at the Equator is about 40075016.686m
    # This is equivalent to TILE_SIZE * 2^0 pixels at zoom 0.

    # 3. Calculate required zoom for the Latitude Span (Vertical)
    # The vertical distance (latitude) is distorted by Mercator projection.
    # The formula relates latitude to the y-coordinate on the map.
    # y = TILE_SIZE * 2^zoom / (2*pi) * log(tan(pi/4 + lat/2)) in radians

    # Function to convert latitude (degrees) to a Mercator y-coordinate (0 to 1)
    def lat_to_mercator_y(lat):
        lat_rad = math.radians(lat)
        return math.log(math.tan(math.pi/4 + lat_rad/2))

    y_min = lat_to_mercator_y(min_lat)
    y_max = lat_to_mercator_y(max_lat)
    #rint('10f now, using log(tan(pi/4 + radians(y)/2))...')
    #rint('10g min_lat',min_lat,'becomes y_min',y_min)
    #rint('10h max_lat',min_lat,'becomes y_max',y_max)

    # Delta in Mercator y-coordinate space, scaled from 0 to 1 for the whole world
    mercator_y_span = abs(y_max - y_min) / (2 * math.pi)
    #rint('10i now, using abs(y_max - y_min) / (2 * pi)...')
    #rint('10j we calculate mercator_y_span ',mercator_y_span)

    # Required zoom based on vertical span
    if mercator_y_span > 0:
        # 2^(zoom) = (map_height_pixels / TILE_SIZE) / mercator_y_span
        zoom_y = math.log2(map_height_pixels / TILE_SIZE / mercator_y_span) #hard-coded screen height and pixels (?)
    else:
        zoom_y = MAX_ZOOM  # Very small span, allow maximum zoom
    #rint('10m now, since 2^(zoom) = (map_height_pixels / TILE_SIZE) / mercator_y_span')
    #rint('10n mercator_y_span',mercator_y_span,' becomes zoom_y ',zoom_y)

    # 4. Calculate required zoom for the Longitude Span (Horizontal)
    # The horizontal distance is uniform in degrees (not distorted).
    # The entire 360 degrees of longitude fit in TILE_SIZE * 2^zoom pixels.
    # The fraction of the map spanned horizontally is delta_lon / 360

    # Required zoom based on horizontal span
    if delta_lon > 0:
        # 2^(zoom) = (map_width_pixels / TILE_SIZE) / (delta_lon / 360)
        zoom_x = math.log2((map_width_pixels / TILE_SIZE) / (delta_lon / 360.0))
    else:
        zoom_x = MAX_ZOOM # Very small span, allow maximum zoom

    # 5. Determine the final zoom level
    # The map must fit *both* the horizontal and vertical spans, so we take the smaller zoom
    # (which corresponds to the larger required geographic area).
    #ax_required_zoom = min(zoom_x, zoom_y)
    max_required_zoom = zoom_y #force y
    #ax_required_zoom = 16 hard-code 11

    # Clamp the result to the valid Google Maps zoom range and return an integer
    return max(0, min(MAX_ZOOM, math.floor(max_required_zoom)))

"""
locations_data = [
    (40.7128, -74.0060),  # New York, USA
    (51.5074, 0.1278),    # London, UK
    (35.6895, 139.6917),  # Tokyo, Japan
    (-33.8688, 151.2093), # Sydney, Australia
    (-22.9068, -43.1729), # Rio de Janeiro, Brazil
    (48.8566, 2.3522),    # Paris, France
    (19.0760, 72.8777),   # Mumbai, India
    (55.7558, 37.6173),   # Moscow, Russia
    (-26.2041, 28.0473),  # Johannesburg, South Africa
    (34.0522, -118.2437)  # Los Angeles, USA
zoom_level = calculate_max_zoom_for_locations(locations_data)
print(f"The calculated maximum zoom factor is: {zoom_level}")
local_locations = [
    (34.0522, -118.2437),
    (34.0600, -118.2500),
    (34.0400, -118.2300)
]
local_zoom = calculate_max_zoom_for_locations(local_locations)
print(f"The calculated maximum zoom factor for local locations is: {local_zoom}")
    except FR24AuthenticationError:
      print("75d Authentication failed")
      return 0
    except FR24NotFoundError:
      print("85e Flight not found")
      return 0
    except FR24RateLimitError:
      print("75f Rate limit exceeded")
      return 0
"""



"""
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.flight_summary.get_full(
        aircraft=[aircraft.code],
        flight_datetime_from=five_days_ago.strftime("%Y-%m-%dT%H:%M:%S"),
        flight_datetime_to=three_days_ago.strftime("%Y-%m-%dT%H:%M:%S"),
        limit=10)
    with Client(os.environ["FR24_API_TOKEN"]) as client:
      data = client.flight_summary.get_full(
        aircraft=[aircraft.code],
        flight_datetime_from=five_days_ago.strftime("%Y-%m-%dT%H:%M:%S"),
        flight_datetime_to=three_days_ago.strftime("%Y-%m-%dT%H:%M:%S"),
        limit=10
    )
"""
