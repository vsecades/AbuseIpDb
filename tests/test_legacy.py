from unittest import TestCase

import abuseipdb
from abuseipdb.parameters import Parameters
from mock import patch


class LegacyTestCase(TestCase):

    def reset_configuration(self):
        # This is required to test the configuration isolated
        Parameters.configuration = {}

    def test_configure_api_key__key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        assert Parameters.get_config() == {'API_KEY': 'some_API_key'}

    def test_configure_api_key__no_key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key(None)
        assert Parameters.get_config() == {}

    def test_check_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_ip(ip='192.0.2.123')

    @patch('unirest.get')
    def test_check_ip(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_ip(ip='192.0.2.123')
        mock.assert_called_once_with('https://www.abuseipdb.com/check/192.0.2.123/json?key=some_API_key&days=30')

    def test_check_cidr__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_cidr(cidr='192.0.2.123')

    @patch('unirest.get')
    def test_check_cidr(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_cidr(cidr='192.0.2.0/24')
        # This URL looks wrong, but the APIv1 documentation doesn't indicate,
        # that the / needs to be encoded.
        mock.assert_called_once_with('https://www.abuseipdb.com/check-block/json?key=some_API_key&network=192.0.2.0/24&days=30')

    def test_report_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.report_ip(ip='192.0.2.123', categories="22")

    @patch('unirest.get')
    def test_report_ip(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.report_ip(ip='192.0.2.123', categories="22")
        mock.assert_called_once_with('https://www.abuseipdb.com/report/json?key=some_API_key&category=22&comment=&ip=192.0.2.123')
