'''
File: data.py

This file contains the constants that are used in the API call to the Urban Routes web service.

TARIFFS: Tariff classifications
ADDRESS_FROM: The source address from which route navigatioon is to start
ADDRESS_TO: The destination address at which route navigation is to end
PHONE_NUMBER: The phone number of the person making the navigation request
CARD_NUMNER: The number of the credit card of the person making the navigation request
CARD_CODE: The verification code of the credit card of the person making the navigation request
MESSAGE_FOR_DRIVER: Any special instructions to be relayed to the driver to be dispatched
URBAN_ROUTES_URL: The URL of the most recent instance of the Urban Routes web service
'''

TARIFFS                 = ('Business','Sleepy','Holiday','Talking','Supportive','Glossy')
ADDRESS_FROM	        = 'East 2nd Street, 601'
ADDRESS_TO	            = '1300 1st St'
PHONE_NUMBER	        = '+1 123 123 12 12'
CARD_NUMBER, CARD_CODE	= '1234 5678 9100','1111'
MESSAGE_FOR_DRIVER      = 'Stop at the juice bar, please'

# URL is replaced with server URL generated by platform
URBAN_ROUTES_URL    = 'https://cnt-bdb01505-15b5-4da8-8d75-dd38026c3688.containerhub.tripleten-services.com'
