from unittest import TestCase

from abuseipdb.api_v1 import AbuseIpDbV1
from abuseipdb.parameters import Parameters

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch




class ApiV1TestCase(TestCase):
    # Only testing the new interface.  The rest is tested in `test_legacy.py`

    def get_api(self):
        self.reset_configuration()
        return AbuseIpDbV1('some_APIv1_key')

    def reset_configuration(self):
        # This is required to test the configuration isolated
        Parameters.configuration = {}

    @patch('abuseipdb.api_v1.configure_api_key')
    def test_creating_api_with_none_api_key_raises_exception(self, mock):
        AbuseIpDbV1('some_APIv1_key')
        mock.assert_called_once_with('some_APIv1_key')

    def test_calling_undefined_method_raises_exception(self):
        abuse = self.get_api()
        with self.assertRaises(NotImplementedError):
            abuse.no_such_method('some parameter')

    @patch('abuseipdb.api_v1.check_ip')
    def test_check(self, mock):
        abuse = self.get_api()
        abuse.check('192.0.2.123')
        mock.assert_called_once_with(ip='192.0.2.123', days='30')

    @patch('abuseipdb.api_v1.check_cidr')
    def test_check_block(self, mock):
        abuse = self.get_api()
        abuse.check_block('192.0.2.0/24')
        mock.assert_called_once_with(cidr='192.0.2.0/24', days='30')

    @patch('abuseipdb.api_v1.report_ip')
    def test_report(self, mock):
        abuse = self.get_api()
        abuse.report('192.0.2.123', '22')
        mock.assert_called_once_with(ip='192.0.2.123', categories='22',
                                     comment='')
