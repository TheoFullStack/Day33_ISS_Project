import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time

MY_LAT = 43.70011 # Your latitude
MY_LONG = -79.4163# Your longitude
sunset = 0
sunrise = 0
iss_latitude = None
iss_longitude = None
def API_connector():
    global iss_longitude, iss_latitude
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
API_connector()

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
def sunset_connector():
    global parameters,sunrise,sunset
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
sunset_connector()
time_now = datetime.now()

iss_above = False
#If the ISS is close to my current position
def iss_proximity_locator():
    global iss_above
    if iss_latitude > (MY_LAT-5) and iss_latitude < (MY_LAT+5):
        if iss_longitude < (MY_LONG + 5) and iss_latitude > (MY_LONG - 5):
            print("ISS is above!")
            iss_above = True
    else:
        print("Iss is not above.")

iss_proximity_locator()
print(f'iss lat:',iss_latitude)
print(f'iss long:',iss_longitude)
print(f'my lat: {MY_LAT}')
print(f'my long: {MY_LONG}')
print("sunset:",sunset)
print('sunrise:',sunrise)

# and it is currently dark
hour = time_now.hour

# Then send me an email to tell me to look up.
my_email = " ENTER E MAIL HERE"
password = "ENTER PASS HERE"
msg = None

connection = smtplib.SMTP("smtp.gmail.com")
#makes connection secure, encrypts it
connection.starttls()

connection.login(user=my_email,password=password)



while True:
    time.sleep(30)
    API_connector()
    sunset_connector()
    if hour >= sunset:
        iss_proximity_locator()
        if iss_above:
            msg = MIMEText("ISS is currently above you!\nlook up and enjoy the moment.", 'plain', 'utf-8')
            msg['Subject'] = "ISS notification"
            connection.sendmail(from_addr=my_email, to_addrs="ENTER EMAIL TO BE SENT TO", msg=msg.as_string())
        else:
            msg= MIMEText(f"It is dark but ISS is not above you, indeed ISS is at here:\nLat: {iss_latitude}\nLong:{iss_longitude}")
            msg['Subject'] = "ISS notification"
            connection.sendmail(from_addr=my_email, to_addrs="teomanaknc@outlook.com", msg=msg.as_string())
    else:
        msg= MIMEText(f"It is not dark and ISS is not above you, indeed ISS is at here:\nLat: {iss_latitude}\nLong: {iss_longitude}")
        msg['Subject'] = "ISS notification"
        connection.sendmail(from_addr=my_email, to_addrs="teomanaknc@outlook.com", msg=msg.as_string())

connection.close()



# BONUS: run the code every 60 seconds.



