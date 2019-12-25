import json

import requests


class AbuseIpDbV2(object):
    """Wrapper for the AbuseIpDb API version 2

    See https://docs.abuseipdb.com/ for documentation.
    """

    VERSION = 'APIv2'

    CATEGORIES = {
        'DDOS_ATTACK': '4',
        'FTP_BRUTE_FORCE': '5',
        'PING_OF_DEATH': '6',
        'PHISHING': '7',
        'FRAUD_VOIP': '8',
        'OPEN_PROXY': '9',
        'WEB_SPAM': '10',
        'EMAIL_SPAM': '11',
        'BLOG_SPAM': '12',
        'VPN_IP':'13',
        'PORT_SCAN': '14',
        'HACKING': '15',
        'SQL_INJECTION': '16',
        'SPOOFING': '17',
        'BRUTE_FORCE': '18',
        'BAD_WEB_BOT': '19',
        'EXPLOITED_HOST': '20',
        'WEB_APP_ATTACK': '21',
        'SSH': '22',
        'IOT_TARGETED': '23',
    }

    class DEFAULT(object):
        CONFIDENCE_MINIMUM = 100
        LIMIT = 10000
        MAX_AGE_IN_DAYS = 30

    def __init__(self, api_key):
        if not api_key:
            raise ValueError('An API key is required')
        self._api_key = api_key

    def __getattr__(self, name):
        raise NotImplementedError('{} not available in APIv2'.format(name))

    def _get_response(self, endpoint, query):
        BASE_URL = 'https://api.abuseipdb.com/api/v2/{endpoint}'
        KNOWN_ENDPOINTS = {
            'check': 'GET',
            'check-block': 'GET',
            'report': 'POST',
        }
        if endpoint not in KNOWN_ENDPOINTS.keys():
            msg = 'Unknown endpoint "{}"'
            raise NotImplementedError(msg.format(endpoint))
        headers = {'Key': self._api_key, 'Accept': 'application/json'}
        return requests.request(
            method=KNOWN_ENDPOINTS[endpoint],
            url=BASE_URL.format(endpoint=endpoint),
            headers=headers, params=query)

    def check(self, ip_address, max_age_in_days=None):
        query = {
            'ipAddress': ip_address,
            'maxAgeInDays': str(max_age_in_days or self.DEFAULT.MAX_AGE_IN_DAYS),
        }
        return self._get_response('check', query)

    def check_block(self, cidr_network, max_age_in_days=None):
        """Check a single IPv4 or IPv6 address

        See https://docs.abuseipdb.com/#check-endpoint for documentation.
        """
        query = {
            'network': cidr_network,
            'maxAgeInDays': str(max_age_in_days or self.DEFAULT.MAX_AGE_IN_DAYS),
        }
        return self._get_response('check-block', query)

    def report(self, ip_address, categories, comment=''):
        query = {
            'ipAddress': ip_address,
            'categories': categories,
            'comment': comment,
        }
        return self._get_response('report', query)
