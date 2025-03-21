import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv


url = 'https://www.tgju.org'
file = 'everyday-price.csv'
TOKEN = '8104820211:AAG7bPbfA5JOFBnxNVweX50D_6tM5yczJ_A'
CHAT_ID = '6697062444'



def goto_site(url):
	response = requests.get(url)
	if response.status_code == 200:
		return response
	else:
		print("Poor Connection")


def get_dollar_price(response):
	soup = BeautifulSoup(response.text, 'html.parser')
	dollar_price_tag = soup.find_all('span', class_= 'info-price')[5]
	return dollar_price_tag.text


def save_price(file, price, date):
	with open(file, "a+", newline="") as f:
		writer = csv.writer(f)

		f.seek(0, 2)
		if f.tell() == 0:
			writer.writerow(['date', 'price'])
			
		writer.writerow([date, price])


def send_telegram(response):
	telegram_api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

	data = {
		"chat_id": CHAT_ID, 
		"text": f"""
					📢 گزارش قیمت دلار 💰

					📅 تاریخ: {datetime.now().strftime("%Y-%m-%d")}
					⏳ ساعت: {datetime.now().strftime("%H:%M:%S")}
					💵 قیمت فعلی: {get_dollar_price(response)} ریال
		"""
	}
	return requests.post(telegram_api, data=data)


r = goto_site(url)
price = get_dollar_price(response= r)
save_price(file, price, datetime.now())
print(price)
print(datetime.now())
tel = send_telegram(goto_site(url))
print(tel.json())

