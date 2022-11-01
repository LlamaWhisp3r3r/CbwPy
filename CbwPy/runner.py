from cbw import ControlByWeb
import requests
import time

if __name__ == '__main__':
	ncbw = ControlByWeb("192.168.1.2", "admin", "Avscle2010")
	try:
		# TODO: Create VIN connector
		start_time = time.time()
		ncbw.create_wire_sensor("TEMPERATURE")
		ncbw.set_network_settings(dns_server_2="8.8.8.8")
		ncbw.set_email_alerts("send.smtp.com", "alarms@covertlawenforcement.com", "Covert1234!", "alarms@covertlawenforcement.com", ["alarms@covertlawenforcement.com"], port=2525, security=0)
		ncbw.update_passwords("Avscle2010", "Covert1234", "Covert1234")
		ncbw.update_date_time(1, ntp_host_name="ntp.axis.com", ntp_sync_interval=1, ntp_sync_on_powerup=1, utc_offset_hour=-7)
		relay_list = ["ROUTER", "CAMERA", "FAN", "STROBE LIGHT"]
		count = 1
		for i in relay_list:
			if count < 3:
				ncbw.update_relay_info(count, i, group=1, power_up_state=1)
			else:
				if i == "FAN":
					ncbw.update_relay_info(count, i, on_status_text="RUNNING")
				ncbw.update_relay_info(count, i)
			count += 1
		ncbw.update_digital_inputs(1, "PCB Input 1")
		ncbw.update_vin("POWER")
		ncbw.create_scheduled_task("Daily Restart", 101, 4, 30, start_date_day=31, start_date_month=11, start_date_year=1969, start_time_hour=4)
		ncbw.create_conditional_task("TEMP _ 100 FAN OFF")
		ncbw.create_conditional_task("TEMP _ 101 FAN ON", condition1_comparison=5, action1_function=1)
		ncbw.create_conditional_task("OVERTEMP OFF SYS ON", condition1_comparison=5, condition1_value=140, dead_pan=5, action1=101, action1_function=0)
		ncbw.create_conditional_task("OVERTEMP ON SYS OFF", condition1_value=138, action1=101, action1_function=1)
		ncbw.create_conditional_task("POWER113V", condition1=9, condition1_value=11.3, dead_pan=0.5, action1=0, action1_function=14, action_email=1)
		ncbw.create_conditional_task("POWER CHARGING", condition1=9, condition1_comparison=5, condition1_value=13.5, dead_pan=1, action1=0, action1_function=14, action_email=1)
		ncbw.update_logging(1, relay1=(1, 1), relay2=(1, 1), relay3=(1, 1), relay4=(1, 1), digital1=(1, 1), digital2=(1, 1), digital3=(1, 1), digital4=(1, 1),
						vin=(1, 1), register=(1, 1), one_wire=(1, 1), xml_logging=1, modbus_logging=1, snmp_logging=1, email_logging=1, email_address=1)
		ncbw.set_header_logo("C:\\Users\\Nate Turner\\Downloads\\VALORENCE320 L0G0.png")
		control_page_order = "02010300070405060000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
		footer = "COVERT LAW ENFORCEMENT - 24/7 SUPPORT: 888-621-5558"
		header = "Valorence LLC"
		ids_to_add = [11, 9, 0]
		del_ids = [3, 2, 4, 1]
		for i in del_ids:
			ncbw.delete_control_page_element(i)
		for i in ids_to_add:
			ncbw.add_control_page_element(i)
		ncbw.submit_control_page(page_header=header, page_footer=footer, control_page_order=control_page_order)
		print("finished in: ", time.time() - start_time)
			
	except requests.exceptions.ConnectTimeout as e:
		print("Device timed out")