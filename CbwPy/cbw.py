"""Summary
"""
from requests import request
import os


class ControlByWeb:
    """Summary

    Attributes
    ----------
    ip : TYPE
        Description
    password : TYPE
        Description
    port : TYPE
        Description
    username : TYPE
        Description
    """

    def __init__(self, ip, username, password, port=80, timeout=10, proxies=None):
        """Summary

        Parameters
        ----------
        ip : TYPE
            Description
        username : TYPE
            Description
        password : TYPE
            Description
        port : int, optional
            Description
        timeout : int, optional
            Description
        proxies : None, optional
            Description
        """
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.__timeout = timeout
        self.__proxies = proxies
        self.__wires_added = 0
        self.__scheduled_added = 0
        self.__conditional_added = 0
        self.__email_endpoint = "/email.srv"
        self.__file_upload_endpoint = "/fileUpload.srv"
        self.__network_endpoint = "/network.srv"
        self.__password_endpoint = "/passwords.srv"
        self.__date_time_endpoint = "/date-time.srv"
        self.__io_update_endpoint = "/ioUpdate.srv"
        self.__task_update_endpoint = "/taskUpdate.srv"
        self.__logging_endpoint = "/logging.srv"
        self.__control_page_endpoint = "/ctrl-setup.srv"
        self.__control_page_information_endpoint = "/ctrl-page.json"
        self.__edit_control_element_endpoint = "/editRelayCtrl.srv"
        self.__overview_endpoint = "/overview.json"
        self.__relay_update_endpoint = "/customState.json"

    def __check_request_response(self, response):

        if response.status_code == 200:
            return True
        else:
            return False

    def __send_cbw_update(self, method, endpoint, check=True, **kwargs):

        url = "http://" + self.username + ":" + self.password + "@" + self.ip + ":" + str(self.port) + endpoint
        r = self.__send_request(method, url, **kwargs)
        if check:
            return self.__check_request_response(r)
        else:
            return r

    def __send_request(self, method, url, **kwargs):

        headers = {"Cookie": "loginLevel=admin"}

        return request(method, url, headers=headers, timeout=self.__timeout, proxies=self.__proxies, **kwargs)

    def set_email_alerts(self, smtp_server, host_username, host_password, host_sender_addr, email_addrs, port=2525,
                         security=0, email_content_type=0):
        """Setup email alerts

        Parameters
        ----------
        smtp_server : str
            SMTP server that your host email uses (i.e. smtp.gmail.com)
        host_username : str
            Username to sign in to the email that will send the alerts
        host_password : str
            Password to sign in to the email that will send the alerts
        host_sender_addr : str
            Email that will be used to send alerts
        email_addrs : list
            List of up to 8 emails to send the alerts to
        port : int, optional (default=465)
            Port used for smtp communication
        security : int, optional (default=1)
            0=None, 1=SSL, 2=[TBA]
        email_content_type : int, optional (default=0)
            0=Full alerts, 1=Short alerts

        Returns
        -------
        bool
            Response was successful
        """

        if isinstance(email_addrs, list):
            if 0 < len(email_addrs) < 9:
                params = dict()
                for i in range(len(email_addrs)):
                    newkey = "gen1_emailAddr" + str(i)
                    params[newkey] = email_addrs[i]
                params["gen1_smtpHostName"] = smtp_server
                params["gen1_smtpSecurity"] = security
                params["gen1_smtpPort"] = port
                params["gen1_smtpUserName"] = host_username
                params["gen1_smtpPassword"] = host_password
                params["gen1_smtpSenderAddress"] = host_sender_addr
                params["gen1_emailContentType"] = email_content_type
                return self.__send_cbw_update("POST", self.__email_endpoint, data=params)

            else:
                raise SyntaxError("Please provide at least 1 but not more than 8 email address")
        else:
            raise SyntaxError("email_addrs is not a list. Please provide a list for email_addrs")

    def set_header_logo(self, file_location):
        """Set logo used on dashboard view

        Parameters
        ----------
        file_location : str
            Location of .png file on the local computer

        Returns
        -------
        bool
            Request was successful
        """

        if isinstance(file_location, str):
            params = {'fileCustomLogo': open(file_location, 'rb')}
            return self.__send_cbw_update("POST", self.__file_upload_endpoint, files=params)
        else:
            raise SyntaxError("Please provide a file path in the form of str")

    def set_network_settings(self, ip_address="192.168.1.2", subnet_mask="255.255.255.0", gateway="192.168.1.1",
                             dns_server_1="192.168.1.1", dns_server_2="192.168.1.1", http_port_enabled=1, http_port=80,
                             https_port=443, dhcp_enabled=0):
        """Set new network settings

        Parameters
        ---------
        ip_address: str
            IP address to set the cbw to
        subnet_mask: str
            Subnet mask for cbw
        gateway: str
            Default gateway for cbw
        dns_server_1: str
            The preferred DNS server
        dns_server_2: str
            The alternate DNS server
        http_port_enabled: int, optional (default=1)
            If the http port is active or not (1=on, 0=off)
        http_port: int, optional (default=80)
            Port used by http
        https_port: int, optional (default=443)
            Port used by https
        dhcp_enabled: int, optional (default=0)
            If dhcp is turned on for cbw (1=on, 0=off)

        Returns
        -------
        bool
            Request was successful
        """

        params = {'gen1_dhcpEnabled': dhcp_enabled, 'gen1_ip': ip_address, 'gen1_netmask': subnet_mask,
            'gen1_gateway': gateway, 'gen1_preferedDNS': dns_server_1, 'gen1_altDNS': dns_server_2,
            'gen1_httpEnabled': http_port_enabled, 'gen1_httpPort': http_port, 'gen1_httpsPort': https_port}

        return self.__send_cbw_update("POST", self.__network_endpoint, data=params)

    def update_passwords(self, admin_password, manager_password=None, user_password=None):
        """Update the admin password and if supplied, update the manager and user password

        Parameters
        ----------
        admin_password : str
            New admin password
        manager_password : str, optional (default=None)
            New manager password
        user_password : str, optional (default=None)
            New user password

        Returns
        --------
        bool
            Request was successful
        """
        params = {'gen1_adminPswd': admin_password}
        if manager_password:
            params['gen1_mgrPswdEnabled'] = 1
            params['gen1_mgrPswd'] = manager_password

        if user_password:
            params['gen1_userPswdEnabled'] = 1
            params['gen1_userPswd'] = user_password

        result = self.__send_cbw_update("POST", self.__password_endpoint, data=params)
        if result:
            self.password = admin_password
        return result

    def update_date_time(self, date_time_preset, utc_offset_hour=-5, utc_offset_min=0, dls_enabled=1, dls_start_week=2,
                         dls_start_day=0, dls_start_month=2, dls_end_week=1, dls_end_day=0, dls_end_month=10,
                         ntp_host_name=None, ntp_sync_interval=None, ntp_sync_on_powerup=None, date_month=None,
                         date_day=None, date_year=None, time_hour=None, time_min=None, time_sec=None):
        """Updates date and time in the General Settings > Date/Time section

        Parameters
        ----------
        date_time_preset: int
            Determines how to set date/time. 1=Sync with NTP server. 0=Manually
        utc_offset_hour: int, optional (default=-5)
            Hours for utc offset. This applies to both manual and ntp server presets
        utc_offset_min: int, optional (default=0)
            Minutes for utc offset. This applies to both manual and ntp server presets
        dls_enabled: int, optional (default=1)
            Daylight savings enabled. 1=enabled, 2=disabled
        dls_start_week: int, optional (default=2)
            Daylight savings start week. 1=1st Week, 2=2nd Week, 3=3rd Week, 4=4th Week, 5=Last Week
        dls_start_day: int, optional (default=0)
            Daylight savings start day. 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday
        dls_start_month: int, optional (default=2)
            Daylight savings start month. 0=Jan, 1=Feb, 2=Mar, 3=Apr, 4=May, 5=June, 6=July, 7=Aug, 8=Sep, 9=Oct, 10=Nov, 11=Dec
        dls_end_week: int, optional (default=1)
            Daylight savings end week. 1=1st Week, 2=2nd Week, 3=3rd Week, 4=4th Week, 5=Last Week
        dls_end_day: int, optional (default=0)
            Daylight savings end day. 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday
        dls_end_month: int, optional (default=10)
            Daylight savings end month. 0=Jan, 1=Feb, 2=Mar, 3=Apr, 4=May, 5=June, 6=July, 7=Aug, 8=Sep, 9=Oct, 10=Nov, 11=Dec
        ntp_host_name: str, optional (default=None)
            FQDM for ntp server. This is only applicable if time_preset is on 1 or ntp server
        ntp_sync_interval: int, optional (default=None)
            NTP sync internal. 0=Once, 1=Daily, 2=Weekly, 3=Monthly
        ntp_sync_on_powerup: int, optional (default=None)
            NTP sync on powerup. 0=No, 1=Yes
        date_month: int, optional (default=None)
            Date month for manual date/time. 0=Jan, 1=Feb, 2=Mar, 3=Apr, 4=May, 5=June, 6=July, 7=Aug, 8=Sep, 9=Oct, 10=Nov, 11=Dec
        date_day: int, optional (default=None)
            Date day for manual date/time. 1=1, 2=2, 3=3... 30=30, 31=31
        date_year: int, optional (default=None)
            Date year for manual date/time. 2018=2018...
        time_hour: int, optional (default=None)
            Hour set for manual date/time. Any number from 0-23 (inclusive)
        time_min: int, optional (default=None)
            Minutes set for manual date/time. Any number from 0-59 (inclusive)
        time_sec: int, optional (default=None)
            Seconds set for manual date/time. Any number from 0-59 (inclusive)

        Returns
        -------
        bool
            Request was successful
        """

        params = {'gen1_timeSource': date_time_preset, 'gen1_utcOffsetHour': utc_offset_hour,
            'gen1_utcOffsetMin': utc_offset_min, 'gen1_dlsEnabled': dls_enabled, 'gen1_dlsStartWeek': dls_start_week,
            'gen1_dlsStartDay': dls_start_day, 'gen1_dlsStartMonth': dls_start_month, 'gen1_dlsEndWeek': dls_end_week,
            'gen1_dlsEndDay': dls_end_day, 'gen1_dlsEndMonth': dls_end_month}

        if date_time_preset == 0:
            params['gen1_dateMonth'] = date_month
            params['gen1_dateDay'] = date_day
            params['gen1_dateYear'] = date_year
            params['gen1_timeHour'] = time_hour
            params['gen1_timeMin'] = time_min
            params['gen1_timeSec'] = time_sec
        elif date_time_preset == 1:
            params['gen1_ntpHostName'] = ntp_host_name
            params['gen1_ntpPeriod'] = ntp_sync_interval
            params['gen1_ntpSyncOnPowerup'] = ntp_sync_on_powerup
        else:
            raise SyntaxError("Please provide correct argument for date_time_preset")

        return self.__send_cbw_update("POST", self.__date_time_endpoint, data=params)

    def update_relay_info(self, relay_number, name, on_status_text="On", off_status_text="Off", pulse_time=1,
                          power_up_state=0, group=0, make_exclusive=0):
        """Update relay information from the I/O Setup > Relays page

        Parameters
        ----------
        relay_number : int
            The relay to update. Should be a number between 1-4 (inclusive)
        name : str
            Name the relay should be changed to
        on_status_text : str, optional (defaults='On')
            On status text
        off_status_text : str, optional (default='Off')
            Off status text
        pulse_time : int, optional (default=1)
            Pulse time for pulse command. This is in seconds
        power_up_state : int, optional (default=0)
            State off relay on power up. 0=off, 1=on
        group : int, optional (default=0)
            Group assigned to relay. 0=No Group, 1=Group 1, 2=Group 2
        make_exclusive : int, optional (default=0)
            Make the relay exclusive from any other relay group. 0=No, 1=Yes


        Returns
        -------
        bool
            Requests was successful
        """

        params = {'spc0_settingsTableNum': relay_number + 4,  # cbw starts at 5 for relay numbering
            'ios0_name': name, 'ios0_onStatusText': on_status_text, 'ios0_offStatusText': off_status_text,
            'ios0_relayGroup': group, 'ios0_powerUpState': power_up_state, 'ios0_relayPulseTime': pulse_time,
            'ios0_relayMakeExclusive': make_exclusive}

        return self.__send_cbw_update("POST", self.__io_update_endpoint, data=params)

    def update_digital_input(self, input_number, name, on_status_text="On", off_status_text="Off", mode=0, hold_time=20,
                             measure_on_time=0, measure_total_on_time=0):
        """Update digital input

        Parameters
        ----------
        input_number : int
            The input to update. Should be a number between 1-4 (inclusive)
        name : str
            Name to change the Digital Input to
        on_status_text : str, optional (default='On')
            On status text
        off_status_text : str, optional (default='Off')
            Off status text
        mode : int, optional (default=0)
            Mode to set input to. Currently, the only supported type is ON/OFF which is 0
        hold_time : int, optional (default=20)
            The De-Bounce or the amount of time the input must be 'ON' for it to be considered on
        measure_on_time : int, optional (default=0)
            Stores how long a single interval (from on to off) of an input is on for in an internal variable. 0=Disabled, 1=Enabled
        measure_total_on_time : int, optional (default=0)
            Stores the total on time of this input. 0=Disabled, 1=Enabled

        Returns
        -------
        bool
            Request was successful
        """

        params = {'spc0_settingsTableNum': input_number, 'ios0_name': name, 'ios0_onStatusText': on_status_text,
            'ios0_offStatusText': off_status_text, 'ios0_digInputMode': mode, 'ios0_debounceMS': hold_time,
            'ios0_measureOnTime': measure_on_time, 'ios0_measureTotalOnTime': measure_total_on_time}

        return self.__send_cbw_update("POST", self.__io_update_endpoint, data=params)

    def create_wire_sensor(self, name, wire_id="00-00000000000000", local_wire_number=1, decimal_place=2, offset=0):
        """Create a wire sensor

        Parameters
        ----------
        name : str
            Name to give to the 1 wire sensor
        wire_id : str, optional (default="00-00000000000000")
            The wire id of the 1 wire sensor to add
        local_wire_number : int, optional (default=1)
            The wire number used at the states.json endpoint. 1=Unassigned, 2-64 (inclusive) are all available wire numbers
        decimal_place : int, optional (default=2)
            The number of digits displayed in the control page. This has nothing to do with the accuracy of the underlying value
        offset : int, optional (default=0)
            This offset gets added to the value measured and creates the final displayed value

        Returns
        -------
        bool
            Request was successful
        """

        params = {'spc0_settingsTableNum': 11 + self.__wires_added, 'ios0_enabled': 1, 'ios0_name': name,
            'ios0_oneWireID': wire_id, 'ios0_localIONum': local_wire_number, 'ios0_decimalPlaces': decimal_place,
            'ios0_offset': offset, 'ios0_local': 1, 'ios0_ioTypeID': 6 + self.__wires_added, 'ios0_devIONum': 1}

        return self.__send_cbw_update("POST", self.__io_update_endpoint, data=params)

    def update_vin(self, name):
        """Update Vin connector

        Parameters
        ----------
        name : str
            New name of the Vin connection

        Returns
        -------
        bool
            Request was successful
        """

        params = {"spc0_settingsTableNum": 9, "spc0_settingsTableType": 4, "ios0_enabled": 1, "ios0_units": "V",
            "ios0_name": name, "ios0_localIONum": 1, "ios0_devID": 0, "ios0_local": 1, "ios0_ioTypeID": 11}

        return self.__send_cbw_update("POST", self.__io_update_endpoint, data=params)

    def create_scheduled_task(self, name, action1, action1_function, action1_function_argument, run_mode=1,
                              start_date_month=0, start_date_day=1, start_date_year=2020, start_time_type=0,
                              start_time_hour=8, start_time_min=0, start_time_sec=0, end_repeat_type=0, repeat_every=1,
                              repeat_units=4, condition=0, condition_value=0, condition_operator=0,
                              condition_deadband=0, on_each=0, day_of_month=0, day_type=0, month_of_year=0,
                              days_of_month=0, end_repeat_month=0, end_repeat_day=0, end_repeat_year=0,
                              end_repeat_hour=0, end_repeat_minute=0, end_repeat_second=0):

        """ Create a scheduled task. These tasks occur on a certain day and time

        Parameters
        ----------
        name: str
            Name to assign the task
        action1: int
            An action that occurs when the start time is set. 0=None, 5-8=Relays accordingly, 101-102=Relay Groups 1/2 accourdingly, 10=Register 1 (To Set color set actionFun1=26), 0=Logging (This depends
            on what actionFunc1 is 9=Log, 19=Reset Log, 27=Pause Log, 28=Resume Logging), 0=Send Email (This depends on what actionFunc1 is 14=Send Email), 0=Send SNMP Trap (
            This depends on what actionFunc1 is 15=Send SNMP Trap For Cond 1 I/O Value, 16=Send SNMP Trap For Cond 2 I/O Value, 17=Send SNMP Traps For Cond 1 and 2 I/O Values), 0=Send SNMP Notification
            (This depends on what actionFunc1 is 23=For Cond 1 I/O value, 24=For Cond 1 I/O Value, 25=For Conf 1 & 2 I/O Value), 0=Send Device State to Remote Services Server (18=Send Device
            State to Remote Services Server), 9=Set Power Status Color (To Set color set actionFun1=26), 11=Temperature (To Set color set actionFun1=26). Note that the Push I/O State To Remote Receiver
            Devices does not seem to work on this API or the GUI interface
        action1_function: int
            This function is directly related to the action1 argument. This argument is only applicable when the correct action1 argument is selected. Such as: Register, Logging, Send Email, Send
            SNMP Trap, Send SNMP Notifications, Send Device State to Remote Services Server, Power, and Temperature
        action1_function_argument: int
            Further information passed to some action_functions. See chart for further details
        run_mode: int, optional (default=1)
            Defines when the scheduled event is active. 0=Off, 1=Always active, 2=Active when all override schedules aren't
        start_date_month : int, optional
            The month that the schedule will begin. 0=Jan, 1=Feb, 2=Mar, 3=Apr, 4=May, 5=June, 6=July, 7=Aug, 8=Sep, 9=Oct, 10=Nov, 11=Dec
        start_date_day : int, optional
            The day that the schedule will begin. 1-31
        start_date_year : int, optional
            The year that the schedule will begin
        start_time_type : int, optional
            Set the start time to three defaults. 0=Set, 1=Sunrise, 2=Sunset
        start_time_hour : int, optional
            The hour to start the schedule at
        start_time_min : int, optional
            The minute of the hour to start the schedule at
        start_time_sec : int, optional
            The second of the minute to start the schedule at
        end_repeat_type : int, optional
            Determines if the schedule will repeat forever or until a date
        repeat_every : int, optional
            The amount to repeat the schedule at. This value is determined by what the repeat_unit is.
        repeat_units : int, optional
            Determines how the schedule will repeat. 0=No Repeat, 1=Seconds, 2=Minutes, 3=Hourly, 4=Daily, 5=Weekly, 6=Monthly, 7=Yearly
        condition: int, optional (default=0)
            Condition for task to run. 0=Off, 1-4=Digital Input 1-4 accordingly, 5-8=Relays 1-4 accordingly, 9=VIN, 10=Register 1, 11-...=1-wire sensors
        condition_value: int, optional (default=0)
            Sets additional values if the condition has additional values to set. Relays & Digital Inputs: 0=Off, 1=On | VIN & Register & Wire Sensors: #=Numerical value to set condition to
        condition_operator: int, optional (default=0)
            Sets the operand of the condition to check with the condition value when applicable. Wire Sensors & Power: 5=≥, 2=<, 13=≥I/O (Note that the condition value now has to be a
            Register or Power number) 10=<I/O (Note that the condition value now has to be a Register or Power number) | Register: 1='=', 2=<, 3=>
        condition_deadband: int, optional (default=0)
            Eliminates multiple triggers for the same condition due to chatter. This option is only applicable when the condition_operator has < or > in it
        on_each: int, optional (default=0)
            Depending on the repeat_unit it will give you a calendar view of day selection. 1=Day select, 0=Calendar Select
        day_of_month: int, optional (default=0)
            If on_each is == 1 select the week the repeat will occur. 1=First, 2=Second, 3=Third, 4=Fourth
        day_type: int, optional (default=0)
            If on_each is == 1 select the day of the week to go along with the day_of_month parameter. 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thur, 5=Fri, 6=Sat
        month_of_year: int, optional (default=0)
            Only used when on_each == 0 while repeat_units is set to 7. See chart for applicable days and how they add together
        days_of_month: int, optional (default=0)
            Only used when on_each is == 0 while repeat_units is set to 6. See chart for applicable days and how they add together
        end_repeat_month: int, optional (default=0)
            Month to end the repeat on. 0=Jan, 1=Feb, 2=Mar, 3=Apr, 4=May, 5=June, 6=July, 7=Aug, 8=Sep, 9=Oct, 10=Nov, 11=Dec
        end_repeat_day: int, optional (default=0)
            Day of the month to end the repeat on. 1-31
        end_repeat_year: int, optional (default=0)
            Year to end the repeat on
        end_repeat_hour: int, optional (default=0)
            Hour of the day to end the repeat on. 0-24
        end_repeat_minute: int, optional (default=0)
            Minutes of the hour to end the repeat on. 0-59
        end_repeat_second: int, optional (default=0)
            Seconds of the minute to end the repeat on. 0-59

        Returns
        -------
        bool
            Request was successful
        """

        params = {'spc0_settingsTableNum': 1 + self.__scheduled_added, 'stk0_enabled': 1, 'stk0_name': name,
            'stk0_runMode': run_mode, 'stk0_startDateMonth': start_date_month, 'stk0_startDateDay': start_date_day,
            'stk0_startDateYear': start_date_year, 'stk0_startTimeType': start_time_type,
            'stk0_startTimeHour': start_time_hour, 'stk0_startTimeMin': start_time_min,
            'stk0_startTimeSec': start_time_sec, 'stk0_actionIONum1': action1, 'stk0_actionFunc1': action1_function,
            'stk0_actionOperand1': action1_function_argument, 'stk0_repeatUnits': repeat_units,
            'stk0_repeatEvery': repeat_every, 'stk0_repeatEndType': end_repeat_type, 'stk0_operandIONum1': condition,
            'stk0_compareOperator1': condition_operator, 'stk0_operandCompVal1': condition_value,
            'stk0_deadband1': condition_deadband, 'stk0_onEach': on_each, 'stk0_ordinalDayOfMonth': day_of_month,
            'stk0_dayType': day_type, 'stk0_monthsOfYear': month_of_year, 'stk0_daysOfMonth': days_of_month,
            'stk0_endRepeatMonth': end_repeat_month, 'stk0_endRepeatDay': end_repeat_day,
            'stk0_endRepeatYear': end_repeat_year, 'stk0_endRepeatHour': end_repeat_hour,
            'stk0_endRepeatMin': end_repeat_minute, 'stk0_endRepeatSec': end_repeat_second}

        self.__scheduled_added += 1

        return self.__send_cbw_update("POST", self.__task_update_endpoint, data=params)

    def create_conditional_task(self, name, condition1=11, condition1_comparison=2, condition1_value=100, dead_pan=0,
                                action1=7, action1_function=2, action_email=0):
        """Summary

        Parameters
        ----------
        name : TYPE
            Description
        condition1 : int, optional
            Description
        condition1_comparison : int, optional
            Description
        condition1_value : int, optional
            Description
        dead_pan : int, optional
            Description
        action1 : int, optional
            Description
        action1_function : int, optional
            Description
        action_email : int, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {'spc0_settingsTableNum': 1 + self.__conditional_added, 'ctk0_operandIONum1': condition1,
            'ctk0_actionEmail1': action_email, 'ctk0_compareOperator1': condition1_comparison,
            'ctk0_operandCompVal1': condition1_value, 'ctk0_deadband1': dead_pan, 'ctk0_enabled': 1, 'ctk0_name': name,
            'ctk0_actionIONum1': action1, 'ctk0_actionFunc1': action1_function}

        self.__conditional_added += 1

        return self.__send_cbw_update("POST", self.__task_update_endpoint, data=params)

    def update_logging(self, enable_logging, logging_interval=(20, 0), power_up_state=1, relay1=(0, 0), relay2=(0, 0),
                       relay3=(0, 0), relay4=(0, 0), digital1=(0, 0), digital2=(0, 0), digital3=(0, 0), digital4=(0, 0),
                       vin=(0, 0), register=(0, 0), one_wire=(0, 0), xml_logging=0, modbus_logging=0, snmp_logging=0,
                       email_logging=0, email_address=0, daily_send=(10, 0)):
        """Summary

        Parameters
        ----------
        enable_logging : TYPE
            Description
        logging_interval : tuple, optional
            Description
        power_up_state : int, optional
            Description
        relay1 : tuple, optional
            Description
        relay2 : tuple, optional
            Description
        relay3 : tuple, optional
            Description
        relay4 : tuple, optional
            Description
        digital1 : tuple, optional
            Description
        digital2 : tuple, optional
            Description
        digital3 : tuple, optional
            Description
        digital4 : tuple, optional
            Description
        vin : tuple, optional
            Description
        register : tuple, optional
            Description
        one_wire : tuple, optional
            Description
        xml_logging : int, optional
            Description
        modbus_logging : int, optional
            Description
        snmp_logging : int, optional
            Description
        email_logging : int, optional
            Description
        email_address : int, optional
            Description
        daily_send : tuple, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {"gen1_loggingEnabled": enable_logging, "gen1_logRate": logging_interval[0],
            "gen1_logUnits": logging_interval[1], "gen1_logPowerUpState": power_up_state,
            "gen1_logDailySendHour": daily_send[0], "gen1_logDailySendMin": daily_send[1],
            "gen1_logEmailAddrNum": email_address, "i1_l": relay1[0], "i1_tL": relay1[1], "i2_l": relay2[0],
            "i2_tL": relay2[1], "i3_l": relay3[0], "i3_tL": relay3[1], "i4_l": relay4[0], "i4_tL": relay4[1],
            "i5_l": digital1[0], "i5_tL": digital1[1], "i6_l": digital2[0], "i6_tL": digital2[1], "i7_l": digital3[0],
            "i7_tL": digital3[1], "i8_l": digital4[0], "i8_tL": digital4[1], "i9_l": vin[0], "i9_tL": vin[1],
            "i10_l": register[0], "i10_tL": register[1], "i11_l": one_wire[0], "i11_tL": one_wire[1],
            "gen1_logXmlReq": xml_logging, "gen1_logModbusReq": modbus_logging, "gen1_logSnmpReq": snmp_logging,
            "gen1_emailLogEnabled": email_logging, }

        return self.__send_cbw_update("POST", self.__logging_endpoint, data=params)

    def add_control_page_element(self, id):
        """Summary

        Parameters
        ----------
        id : TYPE
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {'spc0_addControlIOID': id}

        return self.__send_cbw_update("POST", self.__control_page_endpoint, data=params)

    def delete_control_page_element(self, id):
        """Summary

        Parameters
        ----------
        id : TYPE
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {'spc0_delControl': id}

        return self.__send_cbw_update("POST", self.__control_page_endpoint, data=params)

    def update_control_page_element(self, table_number, io_type_id=None, enabled=None, status_enabled=None,
                                    on_status_color=None, off_status_color=None, on_button_text=None,
                                    on_button_value=None, on_button_enabled=None, off_button_text=None,
                                    off_button_value=None, off_button_enabled=None, toggle_button_text=None,
                                    toggle_button_value=None, toggle_enabled=None, pulse_button_text=None,
                                    pulse_button_value=None, pulse_button_enabled=None):
        """Summary

        Parameters
        ----------
        table_number : TYPE
            Description
        io_type_id : None, optional
            Description
        enabled : None, optional
            Description
        status_enabled : None, optional
            Description
        on_status_color : None, optional
            Description
        off_status_color : None, optional
            Description
        on_button_text : None, optional
            Description
        on_button_value : None, optional
            Description
        on_button_enabled : None, optional
            Description
        off_button_text : None, optional
            Description
        off_button_value : None, optional
            Description
        off_button_enabled : None, optional
            Description
        toggle_button_text : None, optional
            Description
        toggle_button_value : None, optional
            Description
        toggle_enabled : None, optional
            Description
        pulse_button_text : None, optional
            Description
        pulse_button_value : None, optional
            Description
        pulse_button_enabled : None, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {"spc0_settingsTableNum": table_number, "ios0_ioTypeID": io_type_id, "ctl0_enabled": enabled,
            "ctl0_statusEnabled": status_enabled, "ctl0_onStatusColor": on_status_color,
            "ctl0_offStatusColor": off_status_color, "ctl0_buttonText1": on_button_text,
            "ctl0_buttonValue1": on_button_value, "ctl0_buttonEnabled1": on_button_enabled,
            "ctl0_buttonText2": off_button_text, "ctl0_buttonValue2": off_button_value,
            "ctl0_buttonEnabled2": off_button_enabled, "ctl0_buttonEnabled3": pulse_button_enabled,
            "ctl0_buttonText3": pulse_button_text, "ct10_buttonValue3": pulse_button_value,
            "ctl0_buttonText4": toggle_button_text, "ctl0_buttonEnabled4": toggle_enabled,
            "ct10_buttonValue4": toggle_button_value}

        return self.__send_cbw_update("POST", self.__control_page_endpoint, data=params)

    def submit_control_page(self, page_header="ControlByWeb", refresh_rate=3, page_footer="Insert Something Here",
                            show_custom_logo=1, control_page_order=""):
        """Summary

        Parameters
        ----------
        page_header : str, optional
            Description
        refresh_rate : int, optional
            Description
        page_footer : str, optional
            Description
        show_custom_logo : int, optional
            Description
        control_page_order : str, optional
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {"gen1_ctrlPageHeader": page_header, "gen1_ctrlPageRefreshRate": refresh_rate,
            "gen1_ctrlPageFooter": page_footer, "gen1_showCustomLogo": show_custom_logo,
            "spc0_ctrlOrder": control_page_order}

        return self.__send_cbw_update("POST", self.__control_page_endpoint, data=params)

    def get_device_information(self):
        """Summary

        Returns
        -------
        TYPE
            Description
        """
        return self.__send_cbw_update("GET", self.__overview_endpoint, data={}, check=False)

    def get_serial_number(self):
        """Summary

        Returns
        -------

        """

        device_information = self.get_device_information()
        if device_information.status_code == 200:
            return device_information.json()['x spc1_serNum'][0]

    def get_control_page_details(self, table_number):
        """Summary

        Parameters
        ----------
        table_number : TYPE
            Description

        Returns
        -------
        TYPE
            Description
        """
        params = {'spc1_settingsTableNum': table_number}

        return self.__send_cbw_update("GET", self.__edit_control_element_endpoint, params=params, check=False)

    def get_active_result_of_control_page(self):
        """Summary

        Returns
        -------
        TYPE
            Description
        """
        params = {'showUnits': 1, 'showColors': 1}

        return self.__send_cbw_update("GET", self.__relay_update_endpoint, params=params, check=False)

    def upload_basic_script(self, file_location, script_enabled=0):
        """Summary

        Parameters
        ----------
        file_location : TYPE
            Description
        script_enabled : int, optional
            Description
        """

        if not os.path.isfile(file_location) and isinstance(file_location, bytes):
            file_location = file_location
        else:
            file_location = open(file_location)

        params = {'fileBasicScript': file_location, 'gen1_basicScriptEnabled': script_enabled}
        return self.__send_cbw_update("POST", self.__file_upload_endpoint, files=params, check=False)
