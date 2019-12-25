from unittest import TestCase

from abuseipdb.api_v2 import AbuseIpDbV2
from mock import patch


@patch('requests.request')
class ApiV2TestCase(TestCase):

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self):
        return AbuseIpDbV2('some_API_key')

    def test_check(self, mock):
        abuse = self.get_api()
        abuse.check(ip_address=self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'ipAddress': self.TEST_IP_ADDRESS, 'maxAgeInDays': '30'},
            url='https://api.abuseipdb.com/api/v2/check')

    def test_check__with_different_days(self, mock):
        abuse = self.get_api()
        abuse.check(ip_address=self.TEST_IP_ADDRESS, max_age_in_days='90')
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'ipAddress': self.TEST_IP_ADDRESS, 'maxAgeInDays': '90'},
            url='https://api.abuseipdb.com/api/v2/check')

    def test_check_block(self, mock):
        abuse = self.get_api()
        abuse.check_block(cidr_network=self.TEST_CIDR_NETWORK)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'network': self.TEST_CIDR_NETWORK, 'maxAgeInDays': '30'},
            url='https://api.abuseipdb.com/api/v2/check-block')

    def test_check_block__with_different_days(self, mock):
        abuse = self.get_api()
        abuse.check_block(cidr_network=self.TEST_CIDR_NETWORK, max_age_in_days='90')
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'network': self.TEST_CIDR_NETWORK, 'maxAgeInDays': '90'},
            url='https://api.abuseipdb.com/api/v2/check-block')

    def test_report(self, mock):
        abuse = self.get_api()
        abuse.report(ip_address=self.TEST_IP_ADDRESS, categories="22")
        mock.assert_called_once_with(
            method='POST',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'ipAddress': self.TEST_IP_ADDRESS, 'categories': '22', 'comment': ''},
            url='https://api.abuseipdb.com/api/v2/report')

    def test_report__with_some_comment(self, mock):
        abuse = self.get_api()
        abuse.report(ip_address=self.TEST_IP_ADDRESS, categories="22", comment="Some comment")
        mock.assert_called_once_with(
            method='POST',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'ipAddress': self.TEST_IP_ADDRESS, 'categories': '22', 'comment': 'Some comment'},
            url='https://api.abuseipdb.com/api/v2/report')
