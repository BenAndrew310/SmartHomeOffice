import time
from time import sleep
from GMR import GMR


class SHO_APP:

	def __init__(self):
		self.gmr=GMR()
		self.launch_gmr()

	def set_gmr_sleep_delay(self,sleep_delay):
		self.gmr.set_sleep_delay(sleep_delay)

	def set_gmr_time_for_push_notification(self,from_,to):
		self.gmr.set_time_for_push_notification(from_,to)

	def launch_gmr(self):
		self.gmr.set_mode(True)
		self.gmr.launch()

	def set_light_delay(self,delay):
		payload={"datapoints":[{"dataChnId":"4","values":{"value":delay}}]}
		self.gmr.post_to_mcs(payload)

	def set_automation_button(self,value):
		payload={"datapoints":[{"dataChnId":"3","values":{"value":value}}]}
		self.gmr.post_to_mcs(payload)

	def set_control_button(self,value):
		payload={"datapoints":[{"dataChnId":"2","values":{"value":value}}]}
		self.gmr.post_to_mcs(payload)

	def get_light_delay(self):
		return int(self.gmr.get_from_mcs("4"))

	def get_automation_button(self):
		return int(self.gmr.get_from_mcs("3"))

	def get_control_button(self):
		return int(self.gmr.get_from_mcs("2"))
