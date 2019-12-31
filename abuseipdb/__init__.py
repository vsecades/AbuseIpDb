# -*- coding: utf-8 -*-

__version__ = '3.0.0'  #: the working version
__release__ = '3.0.0'  #: the release version

import ipaddress

from abuseipdb.api_v2 import AbuseIpDbV2


class AbuseIpDb(object):
    """Wrapper for AbuseIpDb blacklist service

    Can handle version 2 of the API.

    For links to the documentation see the modules.
    """

    def __init__(self, api_key, api_version=AbuseIpDbV2.VERSION, subscriber=False):
        if api_version == AbuseIpDbV2.VERSION:
            self.api = AbuseIpDbV2(api_key=api_key, subscriber=subscriber)
        else:
            msg = 'API version {} is not supported'
            raise ValueError(msg.format(api_version))

    def _normalize_categories(self, categories):
        cleaned_categories = set([])
        unknown_categories = set([])
        if isinstance(categories, int):
            categories = [str(categories)]
        elif isinstance(categories, str):
            categories = categories.split(',')
        for cat in categories:
            category = str(cat).strip().upper()
            # Store any known category number
            if category.isdigit() and category in self.api.CATEGORIES.values():
                cleaned_categories |= {category}
                continue
            # Translate any known category name to its corresponding number
            if category.replace(' ', '_') in self.api.CATEGORIES.keys():
                category = category.replace(' ', '_')
                cleaned_categories |= {self.api.CATEGORIES[category]}
                continue
            unknown_categories |= {str(cat).strip()}
        if unknown_categories:
            msg = 'Unknown categories "{}"'
            raise ValueError(msg.format(','.join(unknown_categories)))
        return ','.join(sorted(cleaned_categories))

    def blacklist(self, confidence_minimum=None, limit=None):
        """Retrieve a list of blacklisted IP addresses"""
        return self.api.blacklist(confidence_minimum, limit)

    def bulk_report(self, file_name):
        """Report a list of IP addresses by uploading a CSV file"""
        return self.api.bulk_report(file_name)

    def check(self, ip_address, max_age_in_days=None):
        """Check a single IPv4 or IPv6 address"""
        ipaddress.ip_address(ip_address)
        return self.api.check(ip_address, max_age_in_days)

    def check_block(self, cidr_network, max_age_in_days=None):
        """Check a CIDR network block"""
        ipaddress.ip_network(cidr_network)
        return self.api.check_block(cidr_network, max_age_in_days)

    def report(self, ip_address, categories, comment=""):
        """Report a single IPv4 or IPv6 address"""
        ipaddress.ip_address(ip_address)
        categories = self._normalize_categories(categories)
        return self.api.report(ip_address, categories, comment)
