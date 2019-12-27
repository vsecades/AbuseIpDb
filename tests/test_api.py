from unittest import TestCase

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from abuseipdb import AbuseIpDb
from abuseipdb.api_v1 import AbuseIpDbV1
from abuseipdb.api_v2 import AbuseIpDbV2
from abuseipdb.parameters import Parameters


@patch('requests.request')
class ApiParameterValidationTestCase(TestCase):
    # Testing the parameter validation independent from the used API version

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self):
        return AbuseIpDb('some_API_key')

    def test_instantiate__no_key_provided(self, request):
        with self.assertRaises(ValueError):
            AbuseIpDb(None)
        request.assert_not_called()

    def test_instantiate__empty_key_provided(self, request):
        with self.assertRaises(ValueError):
            AbuseIpDb('')
        request.assert_not_called()

    def test_check__no_valid_ip_address_provided(self, request):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.check(ip_address='malformed.ip.address')
        request.assert_not_called()

    def test_check_block__no_valid_cidr_network_provided(self, request):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.check_block(cidr_network='malformed.cidr.network')
        request.assert_not_called()

    def test_report__no_valid_ip_address_provided(self, request):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.report(ip_address='malforemd.ip.address', categories="22")
        request.assert_not_called()

    def test_report__no_valid_categories_provided(self, request):
        abuse = self.get_api()
        with self.assertRaises(ValueError):
            abuse.report(ip_address=self.TEST_IP_ADDRESS, categories='invalid')
        request.assert_not_called()

    def test_report_with_multiple_categories__single_number(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, 22)
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__single_number_as_string(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, '22')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__single_known_keyword(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, 'SSH')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__single_known_keyword_lower_case(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, 'ssh')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__string_of_numbers_without_spaces(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, '15,22')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__string_of_numbers_with_spaces(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, '15, 22')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__keywords_with_spaces(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, 'HACKING, SSH')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__mixed_string(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, '15 , SSH')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__tuple_with_numbers(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, (15, 22))
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__tuple_with_strings_of_numbers(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, ('15', '22'))
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__tuple_with_keywords(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, ('HACKING', 'SSH'))
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '15,22', '')
        request.assert_not_called()

    def test_report_with_multiple_categories__mixed_tuple(self, request):
        abuse = self.get_api()
        with patch.object(abuse.api, 'report') as mock:
            abuse.report(self.TEST_IP_ADDRESS, (13, '15 ', 'SSH'))
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '13,15,22', '')
        request.assert_not_called()


class ApiReturnValueTestCase(TestCase):
    # The tests assume, that the request returns valid JSON, that is already
    # decoded.  This only works with APIv2, but that is now the default anyway.

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self):
        return AbuseIpDb('some_API_key')

    def assert_response_contains(self, response, key, value):
        assert key in response.keys()
        assert response[key] == value

    def test_check_returns_dictionary(self):
        expected_response = {
            "ipAddress": "{}".format(self.TEST_IP_ADDRESS)
        }
        abuse = self.get_api()
        with patch.object(abuse.api, '_get_response', return_value={"data": expected_response}):
            result = abuse.check(self.TEST_IP_ADDRESS)
        assert type(result) == dict
        self.assert_response_contains(result, 'ipAddress', self.TEST_IP_ADDRESS)

    def test_check_block_returns_dictionary(self):
        expected_response = {
            "networkAddress": "{}".format(self.TEST_CIDR_NETWORK[:-3])
        }
        abuse = self.get_api()
        with patch.object(abuse.api, '_get_response', return_value={"data": expected_response}):
            result = abuse.check_block(self.TEST_CIDR_NETWORK)
        assert type(result) == dict
        self.assert_response_contains(result, 'networkAddress', self.TEST_CIDR_NETWORK[:-3])

    def test_blacklist_returns_list_of_dictionaries(self):
        expected_response = [{
            "ipAddress": "{}".format(self.TEST_IP_ADDRESS),
            "abuseConfidenceScore": 100,
        }]
        abuse = self.get_api()
        with patch.object(abuse.api, '_get_response', return_value={"data": expected_response}):
            result = abuse.check(self.TEST_IP_ADDRESS)
        assert type(result) == list
        assert len(result) == 1
        result = result[0]
        self.assert_response_contains(result, 'ipAddress', self.TEST_IP_ADDRESS)
        self.assert_response_contains(result, 'abuseConfidenceScore', 100)

    def test_report_returns_dictionary(self):
        expected_response = {
            "ipAddress": "{}".format(self.TEST_IP_ADDRESS),
            "abuseConfidenceScore": 52,
        }
        abuse = self.get_api()
        with patch.object(abuse.api, '_get_response', return_value={"data": expected_response}):
            result = abuse.report(self.TEST_IP_ADDRESS, (13, '15 ', 'SSH'))
        assert type(result) == dict
        self.assert_response_contains(result, 'ipAddress', self.TEST_IP_ADDRESS)


class GenericApiV1TestCase(TestCase):
    # Only testing the interface.  The rest is tested in `test_api_v1.py`

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self):
        self.reset_configuration()
        return AbuseIpDb('some_API_key', 'APIv1')

    def reset_configuration(self):
        # This is required to test the configuration isolated
        Parameters.configuration = {}

    def test_creating_api(self):
        abuse = self.get_api()
        assert type(abuse.api) == AbuseIpDbV1

    def test_blacklist(self):
        abuse = self.get_api()
        with self.assertRaises(NotImplementedError):
            abuse.blacklist()

    def test_bulk_report(self):
        abuse = self.get_api()
        with self.assertRaises(NotImplementedError):
            abuse.bulk_report('some_file.vsv')

    @patch('abuseipdb.api_v1.AbuseIpDbV1.check')
    def test_check(self, mock):
        abuse = self.get_api()
        abuse.check(self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, None)

    @patch('abuseipdb.api_v1.AbuseIpDbV1.check_block')
    def test_check_block(self, mock):
        abuse = self.get_api()
        abuse.check_block(self.TEST_CIDR_NETWORK)
        mock.assert_called_once_with(self.TEST_CIDR_NETWORK, None)

    @patch('abuseipdb.api_v1.AbuseIpDbV1.report')
    def test_report(self, mock):
        abuse = self.get_api()
        abuse.report(self.TEST_IP_ADDRESS, '22')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')


class GenericApiV2TestCase(TestCase):
    # Only testing the interface.  The rest is tested in `test_api_v2.py`

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def get_api(self):
        return AbuseIpDb('some_API_key', 'APIv2')

    def test_creating_api(self):
        abuse = self.get_api()
        assert type(abuse.api) == AbuseIpDbV2

    @patch('abuseipdb.api_v2.AbuseIpDbV2.blacklist')
    def test_blacklist(self, mock):
        abuse = self.get_api()
        abuse.blacklist()
        mock.assert_called_once_with(None, None)

    @patch('abuseipdb.api_v2.AbuseIpDbV2.bulk_report')
    def test_bulk_report(self, mock):
        abuse = self.get_api()
        abuse.bulk_report('some_file.vsv')
        mock.assert_called_once_with('some_file.vsv')

    @patch('abuseipdb.api_v2.AbuseIpDbV2.check')
    def test_check(self, mock):
        abuse = self.get_api()
        abuse.check(self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, None)

    @patch('abuseipdb.api_v2.AbuseIpDbV2.check_block')
    def test_check_block(self, mock):
        abuse = self.get_api()
        abuse.check_block(self.TEST_CIDR_NETWORK)
        mock.assert_called_once_with(self.TEST_CIDR_NETWORK, None)

    @patch('abuseipdb.api_v2.AbuseIpDbV2.report')
    def test_report(self, mock):
        abuse = self.get_api()
        abuse.report(self.TEST_IP_ADDRESS, '22')
        mock.assert_called_once_with(self.TEST_IP_ADDRESS, '22', '')
