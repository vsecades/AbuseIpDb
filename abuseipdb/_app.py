#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. codeauthor:: Valentin Secades <vsecades@qxdev.com>
"""
import unirest
from parameters import Parameters

def configure_api_key(api_key):
    #Check that api_key is not None OR that it has been set previously
    if api_key is not None:
        Parameters.set_config({"API_KEY": api_key})
    else:
        print("Api key cannot be blank")

def check_ip(ip=None,days="30"):
    #used to check an IP for reports
    if ip is not None:
        request_url = Parameters.url_templates["check_ip"]
        request_url = request_url.replace("[IP]",ip)
        request_url = request_url.replace("[API_KEY]",Parameters.get_config()["API_KEY"])
        request_url = request_url.replace("[DAYS]",days)
        print(request_url)
        response = unirest.get(request_url)
        # return raw for now, we will add decorators later on
        return response.raw_body
    else:
        print("ip is not defined")
        return None

def check_cidr():

    print("Checking CIDR")

def report_ip():
    print("Reporting IP")