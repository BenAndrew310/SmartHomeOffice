import requests
import json
import time
import threading
from time import sleep
from datetime import *
from win10toast import ToastNotifier

class GMR:

	OPEN_WEATHER_API_KEY  = "e460e78f7225e212175be360cfb28054"
	OPEN_WEATHER_HOST     = "https://api.openweathermap.org"

	NEWS_API_KEY		  = "3873b0842df94b4a91fc3298d4e98371"
	NEWS_API_HOST		  = "https://newsapi.org"

	MCS_API_HOST		  = "http://api.mediatek.com"
	MCS_DEVICE_ID		  = "DpvsvmL1"
	MCS_DEVICE_KEY		  = "BlKrcqVKHfhSYLSi"

	COUNTER				  = 1
	SLEEP_DELAY           = 45
	DATE_FOR_PUSH_NOTIF   = date.today()

	TIME_INTERVAL_NEWSLETTER = 6 #hours

	def __init__(self,mode=None,username=""):
		try:
			if type(mode)!=bool:
				raise ValueError
			else:
				self.mode=mode
				self.username=username
				self.upload_gmr_state()
		except:
			self.mode=False
			self.username=username
			self.upload_gmr_state()

	def __bool__(self):
		return self.mode

	def set_mode(self,mode):
		self.mode=mode
		self.upload_gmr_state()

	def set_username(self,username):
		self.username=username

	def set_sleep_delay(self,sleep_delay):
		GMR.SLEEP_DELAY=sleep_delay

	def get_sleep_delay(self):
		return GMR.SLEEP_DELAY

	def set_time_for_push_notification(self,from_="6:00",to="10:00"):
		if datetime.strptime(from_,"%H:%M")>datetime.strptime(to,"%H:%M") :    # making sure that the time "from_" comes before "to" 
			self.push_from_ = datetime.strptime("6:00","%H:%M")
			self.push_to    = datetime.strptime("10:00","%H:%M")
		# elif datetime.strptime(to,"%H:%M")>datetime.strptime("12:00","%H:%M"):   # making sure that the time is in the morning
		# 	self.push_from_ = datetime.strptime(from_,"%H:%M")
		# 	self.push_to    = datetime.strptime("12:00","%H:%M")
		else:
			self.push_from_ = datetime.strptime(from_,"%H:%M")
			self.push_to    = datetime.strptime(to,"%H:%M")


	def get_weather_from_weather_api(self,cityname="Hsinchu",country="tw",units="metric"): #gets weather information from open weather map
		if self:
			endpoint="/data/2.5/weather?q="+cityname+","+country+"&units="+units+"&appid="+GMR.OPEN_WEATHER_API_KEY
			url=GMR.OPEN_WEATHER_HOST+endpoint
			r=requests.get(url)
			description = r.json()["weather"][0]['description']
			temperature = str(r.json()["main"]['temp'])
			wind_speed  = str(r.json()["wind"]["speed"])
			parts       = [description,temperature,wind_speed]
			self.send_weather_message_to_mcs(parts)


	def send_weather_message_to_mcs(self,notif_parts): #upload the message to mcs
		message=str(date.today())+"\nGood morning "+self.username+"! The temperature outside is "+notif_parts[1]+" degrees Celcius. You can expect "+notif_parts[0]+" today and wind blowing at "+notif_parts[2]+" m/s."
		print(message)
		payload={"datapoints":[{"dataChnId":"6","values":{"value":message}}]}
		#if GMR.COUNTER==1:
		endpoint="/mcs/v2/devices/" + GMR.MCS_DEVICE_ID + "/datapoints"
		url=GMR.MCS_API_HOST+endpoint
		headers = {"Content-type": "application/json", "deviceKey": GMR.MCS_DEVICE_KEY}
		r=requests.post(url,headers=headers,data=json.dumps(payload))
		GMR.COUNTER=0
		self.Show_Notification("Good Morning!",message)

	def get_news_from_newsapi(self):
		endpoint="/v2/top-headlines?country="+self.country_of_interest+"&category="+self.category_of_interest+"&apiKey="+GMR.NEWS_API_KEY
		url=GMR.NEWS_API_HOST+endpoint
		r=requests.get(url)
		payload=[]
		for article in r.json()["articles"]:
			payload.append({"title":article["title"],"image":article["urlToImage"],"url":article["url"]})

		self.send_news_to_mcs(payload)

	def send_news_to_mcs(self,message,first_n=5):
		whole="Here are some headlines for you in "+self.category_of_interest+"\n\n"
		for i in range(first_n):
			try:
				whole+=message[i]["title"]
				whole+="\n"
				#whole+=message[i]["image"]
				#whole+="\n"
				whole+=message[i]["url"]
				whole+="\n\n"
			except:
				break
		
		payload={"datapoints":[{"dataChnId":"7","values":{"value":whole}}]}
		self.post_to_mcs(payload)


	def get_from_mcs(self,chn_id):
		endpoint="/mcs/v2/devices/" + GMR.MCS_DEVICE_ID + "/datachannels/" + chn_id + "/datapoints"
		url=GMR.MCS_API_HOST+endpoint
		headers = {"Content-type": "application/json", "deviceKey": GMR.MCS_DEVICE_KEY}
		r=requests.get(url,headers=headers)
		return r.json()["dataChannels"][0]["dataPoints"][0]["values"]["value"]

	def post_to_mcs(self,payload):
		endpoint="/mcs/v2/devices/" + GMR.MCS_DEVICE_ID + "/datapoints"
		url=GMR.MCS_API_HOST+endpoint
		headers = {"Content-type": "application/json", "deviceKey": GMR.MCS_DEVICE_KEY}
		r=requests.post(url,headers=headers,data=json.dumps(payload))

	def upload_gmr_state(self):
		if self:
			payload={"datapoints":[{"dataChnId":"5","values":{"value":1}}]}
		else:
			payload={"datapoints":[{"dataChnId":"5","values":{"value":0}}]}
		self.post_to_mcs(payload)


	def get_light_state(self):
		return self.get_from_mcs("1")

	def Show_Notification(self,title,message):
		toast=ToastNotifier()
		toast.show_toast(title,message,duration=15)


	def launch(self):
		t=threading.Thread(target=self.manage_pushnotif)
		t.deamon=False
		t.start()
		n=threading.Thread(target=self.manage_newsletter)
		n.deamon=False
		n.start()

	def manage_pushnotif(self):

		self.set_time_for_push_notification("06:00","12:00")
		sleep(5)
		while True:
			hour	=str(datetime.now().hour)
			minute  =str(datetime.now().minute)
			time_now=hour+":"+minute
			time_now=datetime.strptime(time_now,"%H:%M")
			state=self.get_light_state()

			if GMR.DATE_FOR_PUSH_NOTIF!=date.today():
				GMR.COUNTER=1
				GMR.DATE_FOR_PUSH_NOTIF=date.today()
			if GMR.COUNTER==1 and time_now.time()>=self.push_from_.time() and time_now.time()<=self.push_to.time() and state==1:
				self.get_weather_from_weather_api()

			if GMR.COUNTER==1:
				print(str(time_now.time())[0:-3]+" : The notification of the day has not been sent yet")
			else:
				print(str(time_now.time())[0:-3]+" : The notification has been sent")
			
			try:
				sleep(GMR.SLEEP_DELAY)
			except:
				print("ERROR with SLEEP_DELAY\nThe program will sleep for 1 minute")
				sleep(60)

	def manage_newsletter(self):

		self.country_of_interest="us"
		self.category_of_interest="technology"
		self.Enabled=True

		if self.Enabled:
			self.get_news_from_newsapi()

		while True:
			for i in range(GMR.TIME_INTERVAL_NEWSLETTER):   # takes approximately 6 hours
				sleep(3600)
			if self.Enabled:
				self.get_news_from_newsapi()


# def main():
# 	gmr=GMR()
# 	gmr.get_news_from_newsapi("us","technology")

# if __name__=="__main__":
# 	main()
