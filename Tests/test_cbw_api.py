import unittest
import httpretty
import os
import sys
sys.path.insert(1, '../CbwPy')
from cbw import ControlByWeb


class TestCbwApi(unittest.TestCase):

    def setUp(self):
        self.cbw = ControlByWeb("192.168.1.2", "admin", 'Example')

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_device_information(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/overview.json",
            body={},
            status=200
        )
        self.assertTrue(self.cbw.get_device_information().status_code)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_device_information(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/overview.json",
            status=401
        )
        self.assertTrue(401, self.cbw.get_device_information().status_code)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_set_email_alerts(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/email.srv",
            status=200
        )
        self.assertTrue(self.cbw.set_email_alerts('example.server.com', 'username', 'password', 'example.email.com', ['number1', 'number2']))

    def test_email_alerts_too_many_email_arguments(self):
        with self.assertRaises(SyntaxError):
            self.cbw.set_email_alerts('example.server.com', 'username', 'password', 'example.email.com',
                                      ['number1', 'number2', 'number3', 'number4', 'number5', 'number6', 'number7', 'number8', 'number9'])

    def test_email_alerts_too_few_email_arguments(self):
        with self.assertRaises(SyntaxError):
            self.cbw.set_email_alerts('example.server.com', 'username', 'password', 'example.email.com',
                                      [])

    def test_email_alerts_wrong_email_arguments(self):
        with self.assertRaises(SyntaxError):
            self.cbw.set_email_alerts('example.server.com', 'username', 'password', 'example.email.com', ('number1'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_set_header_logo(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/fileUpload.srv",
            status=200
        )
        file_location = os.getcwd() + '\\test_cbw_api.py'
        self.assertTrue(self.cbw.set_header_logo(file_location))

    def test_bad_file_location_set_header_logo(self):
        file_location = 'Random\\Location'
        with self.assertRaises(FileNotFoundError):
            self.cbw.set_header_logo(file_location)

    def test_wrong_argument_set_header_logo(self):
        file_location = ['FileLocation']
        with self.assertRaises(SyntaxError):
            self.cbw.set_header_logo(file_location)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_set_network_settings(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/network.srv",
            status=200
        )
        self.assertTrue(self.cbw.set_network_settings())

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_set_network_settings(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/network.srv",
            status=401
        )
        self.assertFalse(self.cbw.set_network_settings())

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_date_time(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/date-time.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_date_time(0))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_date_time(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/date-time.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_date_time(0))

    def test_bad_parameter_update_date_time(self):
        with self.assertRaises(SyntaxError):
            self.cbw.update_date_time(3)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_relay_info(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_relay_info(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_relay_info(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_relay_info(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_digital_input(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_digital_input(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_digital_input(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_digital_input(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_create_wire_sensor(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.create_wire_sensor(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_create_wire_sensor(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.create_wire_sensor(1, 'Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_vin(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_vin('Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_vin(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ioUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_vin('Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_create_scheduled_task(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/taskUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.create_scheduled_task("Example", 0, 1, 1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_create_scheduled_task(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/taskUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.create_scheduled_task("Example", 0, 1, 1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_create_conditional_task(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/taskUpdate.srv",
            status=200
        )
        self.assertTrue(self.cbw.create_conditional_task('Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_create_conditional_task(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/taskUpdate.srv",
            status=401
        )
        self.assertFalse(self.cbw.create_conditional_task('Example'))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_logging(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/logging.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_logging(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_logging(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/logging.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_logging(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_add_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=200
        )
        self.assertTrue(self.cbw.add_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_add_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=401
        )
        self.assertFalse(self.cbw.add_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_delete_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=200
        )
        self.assertTrue(self.cbw.delete_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_delete_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=401
        )
        self.assertFalse(self.cbw.delete_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_update_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=200
        )
        self.assertTrue(self.cbw.update_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_update_control_page_element(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=401
        )
        self.assertFalse(self.cbw.update_control_page_element(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_submit_control_page(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=200
        )
        self.assertTrue(self.cbw.submit_control_page(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_submit_control_page(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/ctrl-setup.srv",
            status=401
        )
        self.assertFalse(self.cbw.submit_control_page(1))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_get_control_page_details(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/editRelayCtrl.srv",
            status=200
        )
        self.assertTrue(self.cbw.get_control_page_details(1).status_code == 200)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_get_control_page_details(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/editRelayCtrl.srv",
            status=401
        )
        self.assertFalse(self.cbw.get_control_page_details(1).status_code == 200)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_get_active_result_of_control_page(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/customState.json",
            status=200
        )
        self.assertTrue(self.cbw.get_active_result_of_control_page().status_code == 200)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_get_active_result_of_control_page(self):
        httpretty.register_uri(
            httpretty.GET,
            "http://192.168.1.2:80/customState.json",
            status=401
        )
        self.assertFalse(self.cbw.get_active_result_of_control_page().status_code == 200)

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_upload_basic_script(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/fileUpload.srv",
            status=200
        )
        file_location = os.getcwd() + '\\test_cbw_api.py'
        self.assertTrue(self.cbw.upload_basic_script(file_location))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_upload_basic_script(self):
        httpretty.register_uri(
            httpretty.POST,
            "http://192.168.1.2:80/fileUpload.srv",
            status=401
        )
        file_location = os.getcwd() + '\\test_cbw_api.py'
        self.assertFalse(self.cbw.upload_basic_script(file_location))

    @httpretty.activate(verbose=False, allow_net_connect=False)
    def test_bad_upload_basic_script(self):
        with self.assertRaises(FileNotFoundError):
            self.cbw.upload_basic_script('Example\\Location')


if __name__ == '__main__':
    unittest.main()
