#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. codeauthor:: Valentin Secades <vsecades@qxdev.com>
"""
import warnings

import requests

from .parameters import Parameters


def configure_api_key(api_key):
    # Check that api_key is not None OR that it has been set previously
    warnings.warn('Sunset date for Abuse IP DB APIv1 is 2020-02-01',
                  DeprecationWarning)
    if not api_key:
        raise ValueError("Api key cannot be blank")
    Parameters.set_config({"API_KEY": api_key})


def check_ip(ip=None, days=Parameters.defaults["days"]):
    # used to check an IP for reports
    warnings.warn('Sunset date for Abuse IP DB APIv1 is 2020-02-01',
                  DeprecationWarning)
    if not ip:
        raise ValueError("IP is not defined")
    request_url = Parameters.url_templates["check_ip"]
    request_url = request_url.replace("[IP]", ip)
    request_url = request_url.replace("[API_KEY]", Parameters.get_config()["API_KEY"])
    request_url = request_url.replace("[DAYS]", days)
    response = requests.request('GET', request_url)
    # return raw for now, we will add decorators later on
    return response.text


def check_cidr(cidr=None, days=Parameters.defaults["days"]):
    # used to check an IP for reports
    warnings.warn('Sunset date for Abuse IP DB APIv1 is 2020-02-01',
                  DeprecationWarning)
    if not cidr:
        raise ValueError("CIDR is not defined")
    request_url = Parameters.url_templates["check_cidr"]
    request_url = request_url.replace("[CIDR]", cidr)
    request_url = request_url.replace("[API_KEY]", Parameters.get_config()["API_KEY"])
    request_url = request_url.replace("[DAYS]", days)
    response = requests.request('GET', request_url)
    # return raw for now, we will add decorators later on
    return response.text


def report_ip(categories=None, comment="", ip=None):
    # used to check an IP for reports
    warnings.warn('Sunset date for Abuse IP DB APIv1 is 2020-02-01',
                  DeprecationWarning)
    if not ip or not categories:
        raise ValueError("Categories or ip not defined")
    request_url = Parameters.url_templates["report_ip"]
    request_url = request_url.replace("[IP]", ip)
    request_url = request_url.replace("[API_KEY]", Parameters.get_config()["API_KEY"])
    request_url = request_url.replace("[COMMENT]", comment)
    request_url = request_url.replace("[CATEGORIES]", categories)
    response = requests.request('GET', request_url)
    # return raw for now, we will add decorators later on
    return response.text


class AbuseIpDbV1(object):

    def __init__(self, api_key):
        configure_api_key(api_key)

    def __getattr__(self, name):
        raise NotImplementedError('{} not available in APIv1'.format(name))

    def check(self, ip_address, max_age_in_days=None):
        max_age_in_days = max_age_in_days or Parameters.defaults["days"]
        return check_ip(ip=ip_address, days=max_age_in_days)

    def check_block(self, cidr_network, max_age_in_days=None):
        max_age_in_days = max_age_in_days or Parameters.defaults["days"]
        return check_cidr(cidr=cidr_network, days=max_age_in_days)

    def report(self, ip_address, categories, comment=""):
        return report_ip(
            ip=ip_address, categories=categories, comment=comment)
