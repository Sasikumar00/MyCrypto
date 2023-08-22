from django.http import JsonResponse
from django.shortcuts import redirect, render
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import os
import json
from .models import *
from django.contrib import messages


def aboutPage(request):

    return render(request, 'about.html')

@login_required(login_url='/user/signin')
def wishlistPage(request):

    return render(request, 'watchlist.html')

def pricingPage(request):

    return render(request, 'pricing.html')

#COIN_GEKO
def getCoins():
    try:
        url = "https://coingecko.p.rapidapi.com/coins/markets"
        querystring = {"vs_currency":"usd","page":"1","per_page":"100","order":"market_cap_desc"}

        headers = {
            "X-RapidAPI-Key": os.environ.get('GEKO_API_KEY'),
            "X-RapidAPI-Host": "coingecko.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
    except Exception as e:
        return JsonResponse({'error': 'Try after sometime'})
    return response.json()

#COIN_GEKO
def home(request):
    data = getCoins()
    if not len(data)<=1:
        for i in data:
            input_date = datetime.strptime(i['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
            # You can convert to the desired timezone if needed
            aware_input_date = timezone.make_aware(input_date, timezone.get_default_timezone())
            # Convert to the desired timezone if needed
            localized_date = timezone.localtime(aware_input_date)
            # Format the date as a single string
            formatted_date_string = localized_date.strftime("%d %B %Y")
            formatted_time_string = localized_date.strftime("%I:%M:%S %p")
            i['last_updated']=[formatted_date_string,formatted_time_string]
        return render(request, 'home.html', {'data': data})
    else:
        return JsonResponse({'error': 'API limit exceeded! Try again after few minutes'})

#GET ALL COINS - COIN_GEKO
# def coins(request):
#     url = "https://coingecko.p.rapidapi.com/coins/markets"
#     querystring = {"vs_currency":"usd","page":"1","per_page":"100","order":"market_cap_desc"}

#     headers = {
#         "X-RapidAPI-Key": os.environ.get('GEKO_API_KEY'),
#         "X-RapidAPI-Host": "coingecko.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)
#     return JsonResponse({'data': response.json()})

# GET TIMESERIES DATA - COIN_API
# def coinTimeSeries(request):
#     today = datetime.now()
#     start_date = today - timedelta(days=365)
#     start_date_iso = start_date.strftime("%Y-%m-%dT%H:%M:%S")
#     url = f'https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1DAY&time_start={start_date_iso}&limit=365'
#     headers = {'X-CoinAPI-Key' : 'B258C2D5-FCB2-4569-81DC-CC648509EFDE'}
#     response = requests.get(url, headers=headers)

#     return JsonResponse({'data': response.json()})

# Display Chart - COIN_GEKO & COIN_API
def chart(request, coin):
    today = datetime.now()
    start_date = today - timedelta(days=365)
    start_date_iso = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    end_date_iso = today.strftime("%Y-%m-%dT%H:%M:%S")
    url = f'https://rest.coinapi.io/v1/exchangerate/{coin}/USD/history?period_id=1DAY&time_start={start_date_iso}&time_end={end_date_iso}&limit=365'
    headers = {'X-CoinAPI-Key' : os.environ.get('API_KEY1')}
    response = requests.get(url, headers=headers)
    updated_array = []
    if('error' not in response.json()[0]):
        for original_object in response.json():
            updated_object = {}
            for key, value in original_object.items():
                new_key = key.replace('rate_', '')  # Remove 'rate_' prefix
                if key == 'time_period_end':
                    new_key = 'date'  # Change 'time_period_end' to 'date'
                    updated_object[new_key] = value.split('T')[0]  # Remove time part
                else:
                    updated_object[new_key] = value
            updated_array.append(updated_object)
    else:
        url = f'https://rest.coinapi.io/v1/exchangerate/{coin}/USD/history?period_id=1DAY&time_start={start_date_iso}&limit=365'
        headers = {'X-CoinAPI-Key' : os.environ.get('API_KEY2')}
        response = requests.get(url, headers=headers)
        if(not response.json['error']):
            for original_object in response.json():
                updated_object = {}
                for key, value in original_object.items():
                    new_key = key.replace('rate_', '')  # Remove 'rate_' prefix
                    if key == 'time_period_end':
                        new_key = 'date'  # Change 'time_period_end' to 'date'
                        updated_object[new_key] = value.split('T')[0]  # Remove time part
                    else:
                        updated_object[new_key] = value
                updated_array.append(updated_object)
    data = updated_array
    # json_file_path = os.path.join(settings.BASE_DIR, f'{coin.lower()}.json')
    # f = open(json_file_path)
    # data = json.load(f)
    d = getCoins()
    if not len(data)<=1 and not len(d)<=1:
        info=[]
        for i in d:
            if i['symbol']==coin.lower():
                info = i
        input_date = datetime.strptime(info['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # You can convert to the desired timezone if needed
        aware_input_date = timezone.make_aware(input_date, timezone.get_default_timezone())
        # Convert to the desired timezone if needed
        localized_date = timezone.localtime(aware_input_date)
        # Format the date as a single string
        formatted_date_string = localized_date.strftime("%d %B %Y")
        formatted_time_string = localized_date.strftime("%I:%M:%S %p")
        info['last_updated'] = [formatted_date_string, formatted_time_string]
        context={
            'Coindata': data,
            'CoinInfo': info,
            'Pairs': f'{coin.upper()}/USD'
        }
        return render(request, 'chart.html', context)
    else:
        return JsonResponse({"error": "API limit exceeded! Try again after few minutes"})

@login_required(login_url='/user/signin')
def addToWatchlist(request):
    username=request.user
    coinName =request.POST.get('coinname')
    coinImg =request.POST.get('coinimg')
    watchTarget = float(request.POST.get('target'))
    watchType = request.POST.get('type')
    watchLists = watchlistModel.objects.filter(user=request.user).order_by('-id')
    if not len(watchLists)>=3:
        watchlistModel.objects.create(user=username,coinName=coinName,coinImg=coinImg,watchType=watchType,watchTarget=watchTarget)
        return redirect('/get-watchlist')
    else:
        messages.error(request,'Watchlist limit reached. Upgrade plans to increase limit.', extra_tags='alert')
        return redirect('/')

@login_required(login_url='/user/signin')
def getWatchlist(request):
    user = request.user
    watchList = watchlistModel.objects.filter(user=user).order_by('-id')
    context={
        'data': watchList
    }
    return render(request,'watchlist.html', context)

@login_required(login_url='/user/signin')
def deleteWatch(request):
    watchId = request.POST.get('watchId')
    watch = watchlistModel.objects.get(pk=watchId)
    if watch:
        watch.delete()
    messages.success(request,'Deleted watch item successfully', extra_tags='alert')
    watchList = watchlistModel.objects.filter(user=request.user).order_by('-id')
    context={
        'data': watchList
    }
    return render(request,'watchlist.html', context)
