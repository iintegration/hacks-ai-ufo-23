import json

import requests
from bs4 import BeautifulSoup

content = open("parsing/dates.csv").read()

dates = []

for i in content.split()[1::2]:
    _, date = i.split(",")
    date = date.replace(".", "/")
    dates.append(date)

print(dates)

base_url = "http://old.meteoinfo.ru/archive-forecast/russia/moscow-area/moscow/{date}"

parsed_dates = {}

for date in dates:
    year, month, day = map(int, date.split("/"))

    content = requests.get(base_url.format(date=f"{year}/{month}/{day-1}")).text
    soup = BeautifulSoup(content)

    trs = soup.find_all("tr", height="50")
    temps = trs[1].find_all("td", class_="pogodacell")
    precipitation = trs[4].find_all("td", class_="pogodacell")
    probability_of_precipitation = trs[5].find_all("td", class_="pogodacell")

    parsed_temps = []
    parsed_precipitation = []
    parsed_probability_of_precipitation = []

    for temp in temps:
        text = temp.text
        parsed = text[-2] if text[-2] == "-" else ""
        parsed = f"{parsed}{text[-1]}"
        parsed_temps.append(parsed)

    for prec in precipitation:
        parsed_precipitation.append(prec.text.strip())

    for prob in probability_of_precipitation:
        parsed_probability_of_precipitation.append(prob.text.strip())

    for i in range(len(parsed_temps)):
        parsed_dates[f"{year}.{month}.{day+i}"] = {"temp": parsed_temps[i], "precipitation": parsed_precipitation[i], "probability_of_precipitation": parsed_probability_of_precipitation[i]}


json.dump(parsed_dates, open("forecast.json", "w"))
