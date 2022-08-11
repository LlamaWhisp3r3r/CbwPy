import requests


class ControlByWeb:

	def __init__(self, ip, username, password, timeout=5):
		self.ip = ip
		self.username = username
		self.password = password
		self.__timeout = timeout
		self.__email_endpoint = "/email.srv"

	def set_email_alerts(self, smtp_server, host_username, host_password, host_sender_addr, email_addrs, port=465, security=1, email_content_type=0):
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
				url = "http://" + self.username + ":" + self.password + "@" + self.ip + self.__email_endpoint
				with requests.post(url, data=params, timeout=self.__timeout, stream=True) as r:
					return r

			else:
				print("Please provide at least 1 but not more than 8 eail address")
				return None
		else:
			print("Please Provide the proper argument")
			return None

if __name__ == '__main__':
	ncbw = ControlByWeb("192.168.1.3", "admin", "Avscle2010")
	try:
		print(ncbw.set_email_alerts("clealerts@gmx.org", "clealerts@gmx.com", "Covert1234", "clealerts@gmx.com", ["alarms@covertlawenforcement.com"]))
	except requests.exceptions.ConnectTimeout as e:
		print("Device timed out")
