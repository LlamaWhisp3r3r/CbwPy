"""This test case has to have a control by web at the default address (192.168.1.2). The control by we will also have to
have to be factory default in order for these tests to work
"""
import unittest
import sys
import os

sys.path.insert(1, '../CbwPy')
from cbw import ControlByWeb


class TestLiveCbwApi(unittest.TestCase):

    def setUp(self):
        self.cbw = ControlByWeb("192.168.1.2", "admin", 'webrelay',
                                proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})

    # TODO: Test all the functions with real life control by web feedback

    def test_device_information(self):
        # List to check request list with
        compare_list = {
            "t gen1_ctrlPageHeader": ["X-410", "30"], "x spc1_wlPartNum": ["X-410-"],
            "x spc1_wlCompany": ["Xytronix Research & Design, Inc."], "x spc1_wlEnabled": ["0"],
            "x spc1_hasCell": ["0"], "x spc1_hasWifi": ["0"], "x spc1_iface": [""],
            "t gen1_remoteServicesEnabled": ["0", "0", "1"], "t gen1_rmtSrvVersion": ["2", "1", "2"],
            "t gen1_powerLossEmails": [""], "x spc1_partNum": ["X-410-I"], "x spc1_firmRev": ["3.06"],
            "x spc1_serNum": ["00:0c:c8:06:4f:d4"], "x spc1_vin": ["12.7 V"], "x spc1_iface": [""],
            "t gen1_latitude": ["41.6796", "-90.0", "90.0"], "t gen1_longitude": ["-111.8737", "-180.0", "180.0"],
            "r gen1_temperatureUnits 1": ["checked"], "r gen1_temperatureUnits 0": [""],
            "r gen1_temperatureUnits 2": [""], "s gen1_displayTimer 0": [""], "s gen1_displayTimer 1": [""],
            "s gen1_displayTimer 2": [""], "s gen1_displayTimer 3": [""], "r gen1_displayOnAlerts 1": [""],
            "r gen1_displayOnAlerts 0": [""], "s gen1_displayLayout 1": [""], "s gen1_displayLayout 2": [""],
            "s gen1_displayLayout 4": [""], "r gen1_powerLossAlertEnabled 1": [""],
            "r gen1_powerLossAlertEnabled 0": [""], "r gen1_powerLossLogEnabled 1": [""],
            "r gen1_powerLossLogEnabled 0": [""], "t gen1_logRateLowPower": [""], "x spc1_wlFooter": [
                "For support, go to&nbsp;<a href='https://www.ControlByWeb.com' target='_blank'>www.ControlByWeb.com</a>"]
        }

        # The Json is the only thing we care about in this situation
        result_keys = self.cbw.get_device_information().json()
        self.assertDictEqual(compare_list, result_keys)

    def test_set_email_alerts(self):

        result_keys = self.cbw.set_email_alerts("example.com", "Example.com", "Example", "Example", ["Example"])
        self.assertTrue(result_keys)

    def test_set_email_alerts_bad_parameters(self):
        result_keys = self.cbw.set_email_alerts(1, 2, None, None, [None])
        self.assertTrue(result_keys)

    def test_set_header_logo(self):
        file_location = os.getcwd() + '\\test_cbw_api.py'
        result_keys = self.cbw.set_header_logo(file_location)
        self.assertTrue(result_keys)

    def test_manual_update_date_time(self):
        result = self.cbw.update_date_time(0)
        self.assertTrue(result)

    def test_sync_update_date_time(self):
        result = self.cbw.update_date_time(1)
        self.assertTrue(result)

    def test_update_relay_info(self):
        result = self.cbw.update_relay_info(1, "example")
        self.assertTrue(result)

    def test_bad_update_relay_info(self):
        result = self.cbw.update_relay_info(0, "example")
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
