from flask import Flask, jsonify, make_response
from flask_cors import CORS
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)

import pandas as pd
import requests
from bs4 import BeautifulSoup

# GLOBAL VARIABLES
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}


# ALL THE PLATFORMS REQUIRE AUTHENTICATION TO ACCESS THE PRIVATE DATA

@app.route('/scrap-data', methods=['GET'])
def scrape_data():

    phone_number = "+919425919685"
    username = 'virat'
    email_address = "akshatbjain.aj@gmail.com"

    # WHATSAPP

    url = f"https://web.whatsapp.com/{phone_number}"
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    registered = "No"
    if soup.find('div', {'class': '_1WZqU PNlAR'}):
        registered = "Yes"

    name_element = soup.find('span', {'class': '_1wjpf'})
    name = name_element.text if name_element else None

    status_element = soup.find('div', {'class': '_2hqOq _3xI7T'})
    status = status_element.text if status_element else None

    last_seen_element = soup.find('div', {'class': '_3H4MS'})
    last_seen = last_seen_element.text if last_seen_element else None

    profile_pic_element = soup.find('div', {'class': '_2ruVH'})
    profile_pic = profile_pic_element.img['src'] if profile_pic_element else None

    whatsapp_data = {
        "Registered": registered,
        "Name": name,
        "Status": status,
        "Last Seen": last_seen,
        "Profile Picture": profile_pic
    }

    # TRUECALLER

    url = f"https://www.truecaller.com/search/in/{phone_number}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered_element = soup.find('div', {'class': "font-montserrat text-lg sm:text-2xl flex-none"})
    registered = registered_element.text if registered_element else None

    name_element = soup.find('div', {'class': "font-montserrat text-lg sm:text-2xl flex-none"})
    name = name_element.text if name_element else None

    email_element = soup.findAll('div', {'class': "field__content"})
    email = email_element[-1].text if email_element and len(email_element) > 2 else None

    truecaller_data = {
        "Registered": registered,
        "Name": name,
        "Email id": email
    }

    # FACEBOOK

    url = f"https://www.facebook.com/{username}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    registered = "No"
    if soup.find('img', {'preserveAspectRatio': "xMidYMid slice"}):
        registered = "Yes"


    name_element = soup.find('h1', {'class': "x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz"})
    name = name_element.text.split('<!-- -->')[0] if name_element else None


    username = response.url.split('https://www.facebook.com/')[1] if registered == "Yes" else None

    profile_url_element = soup.find('img', {'preserveAspectRatio': "xMidYMid slice"})
    profile_url = profile_url_element['xlink:href'] if profile_url_element else None

    facebook_data = {
        "Registered": registered,
        "Name": name,
        "Username": username,
        "Profile URL": profile_url
    }

    # GPAY

    url = f"https://gpay.app.goo.gl/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    registered_element = soup.find('div', {'class': 'DfTQ5d'})
    registered = registered_element.text if registered_element else None

    name = registered
    upi_id_elements = soup.find_all('div', {'class': 'DfTQ5d'})
    upi_ids = [element.text for element in upi_id_elements]

    gpay_data = {
        "Registered": registered,
        "Name": name,
        "UPI IDs": upi_ids
    }

    results = []

    results.append(("WhatsApp", whatsapp_data))


    results.append(("Truecaller", truecaller_data))

    results.append(("Facebook", facebook_data))

    results.append(("Gpay", gpay_data))

    df = pd.DataFrame(results, columns=["Platform", "Data"])
    
    # Data presented in Tabular format

    print(df)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5002)