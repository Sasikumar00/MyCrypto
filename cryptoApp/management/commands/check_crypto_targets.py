from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from cryptoApp.models import *
import requests
from django.http import JsonResponse
import os

def send_notification_email(email,coin, current_price):
    from_email = os.environ.get('EMAIL_ADDRESS')
    recipient_list = [email]
    subject = 'Cryto Target Reached!'
    message = f'The target for {coin} has reached ${current_price}'

    send_mail(subject, message, from_email, recipient_list)

#COIN_GEKO
def getCoins():
    try:
        url = "https://coingecko.p.rapidapi.com/coins/markets"
        querystring = {"vs_currency":"usd","page":"1","per_page":"100","order":"market_cap_desc"}

        headers = {
            "X-RapidAPI-Key": os.environ.get('APP_API_KEY'),
            "X-RapidAPI-Host": "coingecko.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
    except Exception as e:
        return JsonResponse({'error': 'Try after sometime'})
    return response.json()

# def fetch_crypto_prices():
#     # Mock crypto prices for testing
#     mock_crypto_prices = {
#         'bitcoin': 48000.00,
#         'ethereum': 3000.00,
#         # Add more mock prices here
#     }
#     return mock_crypto_prices

def check_crypto_symbol(coin_objs, crypto_sym):
    for coin in coin_objs:
        if coin['name'] == crypto_sym.capitalize():
            return True
        else:
            return False
        
def check_crypto_price(coinObjs, crypto_sm, crypto_price, targetType):
    for coin in coinObjs:
        if coin['name'] == crypto_sm.capitalize():
            if targetType == 'bullish':
                if coin['current_price']<=crypto_price:
                    return True
                else:
                    return False
            else:
                if coin['current_price']>=crypto_price:
                    return True
                else:
                    return False
                
def getCryptoSymbolPrice(coinObjs, cryptoSym):
    for coin in coinObjs:
        if coin['name']==cryptoSym.capitalize():
            return coin['current_price']

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Fetch crypto prices
        crypto_prices = getCoins()
        # crypto_prices = fetch_crypto_prices()

        # Loop through user watchlist targets
        if 'error' not in crypto_prices:
            watchlist_entries = watchlistModel.objects.all()
            for entry in watchlist_entries:
                crypto_symbol = entry.coinName.lower()
                target_price = entry.watchTarget
                target_type = entry.watchType
                # print(crypto_prices[crypto_symbol.lower()]>=target_price)
                if check_crypto_symbol(crypto_prices, crypto_symbol) and check_crypto_price(crypto_prices, crypto_symbol, target_price, target_type):
                    send_notification_email(entry.user, crypto_symbol, getCryptoSymbolPrice(crypto_prices, crypto_symbol))
                    watch = watchlistModel.objects.get(pk=entry.id)
                    if watch:
                        watch.delete()
                    print(f'Sending notification email to {entry.user} for {crypto_symbol}. Price: {getCryptoSymbolPrice(crypto_prices, crypto_symbol)}')
        