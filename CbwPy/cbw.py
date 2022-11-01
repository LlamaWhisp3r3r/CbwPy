import requests


class ControlByWeb:

	def __init__(self, ip, username, password, timeout=10):
		self.ip = ip
		self.username = username
		self.password = password
		self.__timeout = timeout
		self.__wires_added = 0
		self.__scheduled_added = 0
		self.__conditional_added = 0
		self.__default_password = "webrelay"
		self.__email_endpoint = "/email.srv"
		self.__file_upload_endpoint = "/fileUpload.srv"
		self.__network_endpoint = "/network.srv"
		self.__password_endpoint = "/passwords.srv"
		self.__date_time_endpoint = "/date-time.srv"
		self.___io_update_endpoint = "/ioUpdate.srv"
		self.__task_update_endpoint = "/taskUpdate.srv"
		self.__logging_endpoint = "/logging.srv"
		self.__control_page_endpoint = "/ctrl-setup.srv"
		self.__overview_endpoint = "/overview.json"

	def __send_cbw_update(self, params, endpoint, file=False, **kwargs):
		try:
			url = "http://" + self.username + ":" + self.password + "@" + self.ip + endpoint
			r = self.__send_request(url, params, file=file, **kwargs)
			if r.status_code == 401:
				url = "http://" + self.username + ":" + self.__default_password + "@" + self.ip + endpoint
				r = self.__send_request(url, params, file=file, **kwargs)
			return r
		except Exception as e:
			print(e)
			return None
		

	def __send_request(self, url, params, file=False, get=False):

		headers = {
			"Cookie": "loginLevel=admin"
		}

		if file:
			return requests.post(url, files=params, headers=headers, timeout=self.__timeout)
		else:
			headers["Content-Type"] = "application/x-www-form-urlencoded"
			if get:
				return requests.get(url, data=params, headers=headers, timeout=self.__timeout)
			else:
				return requests.post(url, data=params, headers=headers, timeout=self.__timeout)

	def set_email_alerts(self, smtp_server, host_username, host_password, host_sender_addr, email_addrs, port=2525, security=0, email_content_type=0):
		"""Setup email alerts

		Parameters
		----------
		smtp_server: str
			SMTP server that your host email uses (i.e. smtp.gmail.com)
		host_username: str
			Username to sign into the email that will send the alerts
		host_password: str
			Password to sign into the email that will send the alerts
		host_sender_addr: str
			Email that will be used to send alerts
		email_addrs: list
			List of up to 8 emails to send the alerts to
		port: int, optional (default=465)
			Port used for smtp communication
		security: int, optional (default=1)
			0=None, 1=SSL, 2=[TBA]
		email_content_type: int, optional (default=0)
			0=Full alerts, 1=Short alerts

		Returns
		-------
		requests.Response
			response from the http request made
		"""

		if isinstance(email_addrs, list):
			if len(email_addrs) > 0 and len(email_addrs) < 9:
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
				return self.__send_cbw_update(params, self.__email_endpoint)

			else:
				print("Please provide at least 1 but not more than 8 eail address")
				return None
		else:
			print("Please provide the proper argument")
			return None

	def set_header_logo(self, file_location):
		"""Set logo used on dashboard view

		Parameters
		----------
		file_location: str
			Location of .png file on the local computer

		Returns
		-------
		requests.Response
			response from the http request made
		"""

		if isinstance(file_location, str):
			params = {'fileCustomLogo': open(file_location, 'rb')}
			return self.__send_cbw_update(params, self.__file_upload_endpoint, file=True)
		else:
			print("Please provide a proper argument")
			return None
	
	def set_network_settings(self, ip_address="192.168.1.2", subnet_mask="255.255.255.0", gateway="192.168.1.1", dns_server_1="192.168.1.1", dns_server_2="192.168.1.1", http_port_enabled=1, http_port=80, https_port=443, dhcp_enabled=0):
		"""Set new network settings

		Paramters
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
		requests.Response
			response from the http request made
		"""

		params = {
			'gen1_dhcpEnabled': dhcp_enabled,
			'gen1_ip': ip_address,
			'gen1_netmask': subnet_mask,
			'gen1_gateway': gateway,
			'gen1_preferedDNS': dns_server_1,
			'gen1_altDNS': dns_server_2,
			'gen1_httpEnabled': http_port_enabled,
			'gen1_httpPort': http_port,
			'gen1_httpsPort': https_port
		}

		return self.__send_cbw_update(params, self.__network_endpoint)

	def update_passwords(self, admin_password, manager_password=None, user_password=None):
		params = {'gen1_adminPswd': admin_password}
		if manager_password:
			params['gen1_mgrPswdEnabled'] = 1
			params['gen1_mgrPswd'] = manager_password
			
		if user_password:
			params['gen1_userPswdEnabled'] = 1
			params['gen1_userPswd'] = user_password
		
		return self.__send_cbw_update(params, self.__password_endpoint)

	def update_date_time(self, date_time_preset, utc_offset_hour=-5, utc_offset_min=0, dls_enabled=1,
		dls_start_week=2, dls_start_day=0, dls_start_month=2, dls_end_week=1, dls_end_day=0,
		dls_end_month=10, ntp_host_name=None, ntp_sync_interval=None, ntp_sync_on_powerup=None,
		date_month=None, date_day=None, date_year=None, time_hour=None, time_min=None, time_sec=None):
		""" Updates the date and time"""

		params = {
			'gen1_timeSource': date_time_preset,
			'gen1_utcOffsetHour': utc_offset_hour,
			'gen1_utcOffsetMin': utc_offset_min,
			'gen1_dlsEnabled': dls_enabled,
			'gen1_dlsStartWeek': dls_start_week,
			'gen1_dlsStartDay': dls_start_day,
			'gen1_dlsStartMonth': dls_start_month,
			'gen1_dlsEndWeek': dls_end_week,
			'gen1_dlsEndDay': dls_end_day,
			'gen1_dlsEndMonth': dls_end_month
		}
		if date_time_preset == 0:
			# manually setup
			params['gen1_dateMonth'] = date_month
			params['gen1_dateDay'] = date_day
			params['gen1_dateYear'] = date_year
			params['gen1_timeHour'] = time_hour
			params['gen1_timeMin'] = time_min
			params['gen1_timeSec'] = time_sec

		elif date_time_preset == 1:
			# ntp setup
			params['gen1_ntpHostName'] = ntp_host_name
			params['gen1_ntpPeriod'] = ntp_sync_interval
			params['gen1_ntpSyncOnPowerup'] = ntp_sync_on_powerup
		else:
			print("Please provide correct arguments")
			return None

		return self.__send_cbw_update(params, self.__date_time_endpoint)
	
	def update_relay_info(self, relay_number, name, on_status_text="On", off_status_text="Off", pulse_time=1, power_up_state=0, group=0, make_exclusive=0):

		params = {
			'spc0_settingsTableNum': relay_number+4, # For some reason cbw starts at 5 for relay numbering
			'ios0_name': name,
			'ios0_onStatusText': on_status_text,
			'ios0_offStatusText': off_status_text,
			'ios0_relayGroup': group,
			'ios0_powerUpState': power_up_state,
			'ios0_relayPulseTime': pulse_time,
			'ios0_relayMakeExclusive': make_exclusive
		}

		return self.__send_cbw_update(params, self.___io_update_endpoint)

	def update_digital_inputs(self, input_number, name, on_status_text="On", off_status_text="Off", mode=0, hold_time=20, measure_on_time=0, measure_total_on_time=0):

		params = {
			'spc0_settingsTableNum': input_number,
			'ios0_name': name,
			'ios0_onStatusText': on_status_text,
			'ios0_offStatusText': off_status_text,
			'ios0_digInputMode': mode,
			'ios0_debounceMS': hold_time,
			'ios0_measureOnTime': measure_on_time,
			'ios0_measureTotalOnTime': measure_total_on_time
		}

		return self.__send_cbw_update(params, self.___io_update_endpoint)
	
	def create_wire_sensor(self, name, wire_id="00-00000000000000", local_wire_number=1, decimal_place=2, offset=0):
		""" Create a one wire sensor
		"""

		params = {
			'spc0_settingsTableNum': 11+self.__wires_added,
			'ios0_enabled': 1,
			'ios0_name': name,
			'ios0_oneWireID': wire_id,
			'ios0_localIONum': local_wire_number,
			'ios0_decimalPlaces': decimal_place,
			'ios0_offset': offset,
			'ios0_local': 1,
			'ios0_ioTypeID': 6+self.__wires_added,
			'ios0_devIONum': 1
		}

		return self.__send_cbw_update(params, self.___io_update_endpoint)
	
	def update_vin(self, name):

		params = {
			"spc0_settingsTableNum": 9,
			"spc0_settingsTableType": 4,
			"ios0_enabled": 1,
			"ios0_units": "V",
			"ios0_name": name,
			"ios0_localIONum": 1,
			"ios0_devID": 0,
			"ios0_local": 1,
			"ios0_ioTypeID": 11
		}

		return self.__send_cbw_update(params, self.___io_update_endpoint)
	
	def create_scheduled_task(self, name, action1, action1_function, action1_function_argument, run_mode=1,
		start_date_month=0, start_date_day=1, start_date_year=2020, start_time_type=0, start_time_hour=8,
		start_time_min=0, start_time_sec=0, end_repeat_type=0, repeat_every=1, repeat_units=4):
		
		# TODO: what to do about all the other options? How do I describe them?
		params = {
			'spc0_settingsTableNum': 1+self.__scheduled_added,
			'stk0_enabled': 1,
			'stk0_name': name,
			'stk0_runMode': run_mode,
			'stk0_startDateMonth': start_date_month,
			'stk0_startDateDay': start_date_day,
			'stk0_startDateYear': start_date_year,
			'stk0_startTimeType': start_time_type,
			'stk0_startTimeHour': start_time_hour,
			'stk0_startTimeMin': start_time_min,
			'stk0_startTimeSec': start_time_sec,
			'stk0_actionIONum1': action1,
			'stk0_actionFunc1': action1_function,
			'stk0_actionOperand1': action1_function_argument,
			'stk0_repeatUnits': repeat_units,
			'stk0_repeatEvery': repeat_every,
			'stk0_repeatEndType': end_repeat_type
		}

		self.__scheduled_added += 1

		return self.__send_cbw_update(params, self.__task_update_endpoint)
	
	def create_conditional_task(self, name, condition1=11, condition1_comparison=2, condition1_value=100, dead_pan=0, action1=7, action1_function=2, action_email=0):
		
		params = {
			'spc0_settingsTableNum': 1+self.__conditional_added,
			'ctk0_operandIONum1': condition1,
			'ctk0_actionEmail1': action_email,
			'ctk0_compareOperator1': condition1_comparison,
			'ctk0_operandCompVal1': condition1_value,
			'ctk0_deadband1': dead_pan,
			'ctk0_enabled': 1,
			'ctk0_name': name,
			'ctk0_actionIONum1': action1,
			'ctk0_actionFunc1': action1_function
		}

		self.__conditional_added += 1

		return self.__send_cbw_update(params, self.__task_update_endpoint)

	def update_logging(self, enable_logging, logging_interval=(20, 0), power_up_state=1, relay1=(0, 0),
		relay2=(0, 0), relay3=(0, 0), relay4=(0, 0), digital1=(0, 0), digital2=(0, 0),digital3=(0, 0), digital4=(0, 0),
		vin=(0, 0), register=(0, 0), one_wire=(0, 0), xml_logging=0, modbus_logging=0, snmp_logging=0, email_logging=0, email_address=0, daily_send=(10, 0)):

		params = {
			"gen1_loggingEnabled":  enable_logging,
			"gen1_logRate":  logging_interval[0],
			"gen1_logUnits":  logging_interval[1],
			"gen1_logPowerUpState":  power_up_state,
			"gen1_logDailySendHour":  daily_send[0],
			"gen1_logDailySendMin":  daily_send[1],
			"gen1_logEmailAddrNum":  email_address,
			"i1_l":  relay1[0],
			"i1_tL":  relay1[1],
			"i2_l":  relay2[0],
			"i2_tL":  relay2[1],
			"i3_l":  relay3[0],
			"i3_tL":  relay3[1],
			"i4_l":  relay4[0],
			"i4_tL":  relay4[1],
			"i5_l":  digital1[0],
			"i5_tL":  digital1[1],
			"i6_l":  digital2[0],
			"i6_tL":  digital2[1],
			"i7_l":  digital3[0],
			"i7_tL":  digital3[1],
			"i8_l":  digital4[0],
			"i8_tL":  digital4[1],
			"i9_l":  vin[0],
			"i9_tL":  vin[1],
			"i10_l":  register[0],
			"i10_tL":  register[1],
			"i11_l": one_wire[0],
			"i11_tL":  one_wire[1],
			"gen1_logXmlReq":  xml_logging,
			"gen1_logModbusReq":  modbus_logging,
			"gen1_logSnmpReq":  snmp_logging,
			"gen1_emailLogEnabled":  email_logging,
		}

		return self.__send_cbw_update(params, self.__logging_endpoint)

	def add_control_page_element(self, id):

		params = {
			'spc0_addControlIOID': id
		}

		return self.__send_cbw_update(params, self.__control_page_endpoint)
	
	def delete_control_page_element(self, id):

		params = {
			'spc0_delControl': id
		}

		return self.__send_cbw_update(params, self.__control_page_endpoint)
	
	def submit_control_page(self, page_header="ControlByWeb", refresh_rate=3, page_footer="Insert Something Here", show_custom_logo=1, control_page_order=""):

		params = {
			"gen1_ctrlPageHeader":  page_header,
			"gen1_ctrlPageRefreshRate":  refresh_rate,
			"gen1_ctrlPageFooter":  page_footer,
			"gen1_showCustomLogo":  show_custom_logo,
			"spc0_ctrlOrder": control_page_order 
		}

		return self.__send_cbw_update(params, self.__control_page_endpoint)

	def get_device_information(self):
     
		return self.__send_cbw_update({}, self.__overview_endpoint, get=True)

