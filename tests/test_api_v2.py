from unittest import TestCase

from abuseipdb.api_v2 import AbuseIpDbV2
from mock import patch


@patch('requests.request')
class ApiV2TestCase(TestCase):

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self, **kwargs):
        kwargs['api_key'] = 'some_API_key'
        return AbuseIpDbV2(**kwargs)

    def test_blacklist(self, mock):
        abuse = self.get_api()
        abuse.blacklist()
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={},
            url='https://api.abuseipdb.com/api/v2/blacklist')

    def test_blacklist__with_configence_minimum_but_not_subscriber(self, mock):
        abuse = self.get_api()
        abuse.blacklist(confidence_minimum=90)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={},
            url='https://api.abuseipdb.com/api/v2/blacklist')

    def test_blacklist__with_configence_minimum_and_subscriber(self, mock):
        abuse = self.get_api(subscriber=True)
        abuse.blacklist(confidence_minimum=90)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'confidenceMinimum': '90'},
            url='https://api.abuseipdb.com/api/v2/blacklist')

    def test_blacklist__with_too_high_confidence_minimum(self, mock):
        abuse = self.get_api(subscriber=True)
        with self.assertRaises(ValueError):
            abuse.blacklist(confidence_minimum=123)

    def test_blacklist__with_too_low_confidence_minimum(self, mock):
        abuse = self.get_api(subscriber=True)
        with self.assertRaises(ValueError):
            abuse.blacklist(confidence_minimum=10)

    def test_blacklist__with_limit(self, mock):
        abuse = self.get_api()
        abuse.blacklist(limit=123)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'limit': '123'},
            url='https://api.abuseipdb.com/api/v2/blacklist')

    def test_blacklist__with_too_low_limit(self, mock):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.blacklist(limit=0)

    def test_blacklist__with_too_high_limit_and_not_subscriber(self, mock):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.blacklist(limit=1234567890)

    def test_blacklist__with_high_limit_and_subscriber(self, mock):
        abuse = self.get_api(subscriber=True)
        abuse.blacklist(limit=1234567890)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'limit': '1234567890'},
            url='https://api.abuseipdb.com/api/v2/blacklist')

    def test_bulk_report_is_not_implemented_yet(self, mock):
        abuse = self.get_api()
        with self.assertRaises(NotImplementedError):
            abuse.bulk_report('some_file.csv')

    def test_check(self, mock):
        abuse = self.get_api()
        abuse.check(ip_address=self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(
            method='GET',
            headers={'Key': 'some_API_key', 'Accept': 'application/json'},
            params={'ipAddress': self.TEST_IP_ADDRESS, 'maxAgeInDays': '30'},
            url='https://api.abuseipdb.com/api/v2/check')

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
