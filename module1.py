from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import requests
import pandas as pd
import time, csv
import json
import requests
from bs4 import BeautifulSoup
from facebook_scraper import get_profile

# from multiprocessing import Process
# import threading

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options

"""
# Helper function to easly  parallelize multiple functions
def parallelize_functions(*functions):
    processes = []
    for function in functions:
        p = Process(target=function)
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
"""

"""       
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--headless")  # Run in headless mode, i.e, to run in background without opening the browse

    #initial setup
    driver = webdriver.Chrome(options=chrome_options)

    #login to WhatsApp web
    driver.get("https://web.whatsapp.com")

    #scan QR code from phone
    wait = WebDriverWait(driver, 10)
"""


# Setting up driver
chrome_options = Options()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")  # Run in headless mode, i.e, to run in background without opening the browser as we need to authenticate (can be done either scanning QR or using number) & click the checkbox in confirm box(Can't click using selenium, have to be done manually) in the whatsapp

# initial setup
driver = webdriver.Chrome(options=chrome_options)

# login to WhatsApp web
driver.get("https://web.whatsapp.com")

# scan QR code from phone
wait = WebDriverWait(driver, 10)


# Initialize App
app = Flask(__name__)
CORS(app)


# Request http://localhost:5002/scrap-data to scrap the data with phone_number and username as query parameters or you can also change the global variables


@app.route("/scrap-data", methods=["GET"])
def scrape_data():
    # Global Variables which can be used through out the app (Default phone_number and username)
    phone_number = "8268291167"
    username = "virat"
    email_address = "akshatbjain.aj@gmail.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }

    phone_number, username = request.args.get(
        "phone_number", phone_number
    ), request.args.get("username", username)

    # WHATSAPP

    whatsapp_data = {
        "Registered": None,
        "Name": None,
        "Status": None,
        "Last Seen": None,
        "Profile Picture": None,
    }

    driver.get(f"https://api.whatsapp.com/send?phone=91{phone_number}")

    # Wait for 5 seconds to confirm and click check box in the confirm box to let the webdriver open whatsapp as using selenium we can't click the check box inside the popup boxes
    time.sleep(5)

    # wait.until(EC.alert_is_present())

    # Override the window.confirm function with custom JavaScript code (It didn't worked)
    # driver.execute_script("window.confirm = function() { return true; }")

    """
    for prompt box
    alert = Alert(driver)
    alert.accept()

    for confirm box
    alert = driver.switch_to.alert
    alert.accept()
    """

    window_1 = driver.find_element(By.LINK_TEXT, "Continue to Chat")
    window_1.click()

    time.sleep(2)

    window_2 = driver.find_element(By.LINK_TEXT, "use WhatsApp Web")
    window_2.click()

    # wait to redirect and load the whatsapp web app, if your internet is fast you can decrease the time of loading the screen
    time.sleep(25)

    try:
        chat_screen = driver.find_element(
            By.CSS_SELECTOR, '[class="_2lSWV _3cjY2 copyable-area"]'
        )
        whatsapp_data["Registered"] = "Yes"

        try:
            last_seen = driver.find_element(
                By.CSS_SELECTOR,
                '[class="ggj6brxn gfz4du6o r7fjleex lhj4utae le5p0ye3 _11JPr selectable-text copyable-text"]',
            )
            whatsapp_data["Last Seen"] = last_seen.text
        except NoSuchElementException:
            print("Last scene is disabled!")

        # Click on profile name/number of the user to view profile
        driver.find_element(By.CSS_SELECTOR, '[title="Profile Details"]').click()

        time.sleep(5)

        name_node = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="contact-info-subtitle"]'
        ).text
        check_whats_scraped_name_or_number = "".join(name_node.split())

        if phone_number == check_whats_scraped_name_or_number[3:]:
            print("Let me check if name is present")
            try:
                whatsapp_data["Name"] = driver.find_element(
                    By.CSS_SELECTOR, '[class="enbbiyaj e1gr2w1z hp667wtd"]'
                ).text
            except NoSuchElementException:
                print("No name found")
        else:
            whatsapp_data["Name"] = name_node

        try:
            profile_pic = driver.find_element(
                By.CSS_SELECTOR,
                '[class="g0rxnol2 f804f6gw ln8gz9je ppled2lx gfz4du6o r7fjleex g9p5wyxn i0tg5vk9 aoogvgrq o2zu3hjb bs7a17vp csshhazd _11JPr"]',
            )
            whatsapp_data["Profile Picture"] = profile_pic.get_attribute("src")
        except NoSuchElementException:
            print("No Display picture")

        try:
            status = driver.find_element(
                By.CSS_SELECTOR,
                '[class="cw3vfol9 _11JPr selectable-text copyable-text"]',
            )
            whatsapp_data["Status"] = status.get_attribute("title")
        except NoSuchElementException:
            print("No status found!")

    except NoSuchElementException:
        whatsapp_data["Registered"] = "No"
        print("User not found!")

    # TRUECALLER

    truecaller_data = {"Registered": None, "Name": None, "Email id": None}

    cookiesTrueCaller = [
        {
            "name": "tc:cookies",
            "value": "%7B%22necessary%22%3Atrue%2C%22marketing%22%3Atrue%7D",
            "domain": "www.truecaller.com",
            "path": "/",
            "expires": 1720017936,
            "httpOnly": False,
            "secure": False,
        },
        {
            "name": "tc:dismissexitintentpopup",
            "value": "true",
            "domain": "www.truecaller.com",
            "path": "/",
            "expires": 1688591788,
            "httpOnly": False,
            "secure": False,
        },
        {
            "name": "__gads",
            "value": "ID=31e9d8e3d0af6bb1:T=1687987499:RT=1688137401:S=ALNI_MYeaQv5o0Exvu4V7ia4OeQaWWlRIw",
            "domain": ".truecaller.com",
            "path": "/",
            "expires": 1721683499,
            "httpOnly": False,
            "secure": False,
        },
        {
            "name": "__gpi",
            "value": "UID=00000c1c61d87e62:T=1687987499:RT=1688137401:S=ALNI_MYDfRzpi6AkU3qQypK6iK3X2wqCBA",
            "domain": ".truecaller.com",
            "path": "/",
            "expires": 1721683499,
            "httpOnly": False,
            "secure": False,
        },
    ]

    try:
        session = requests.Session()

        for cookie in cookiesTrueCaller:
            session.cookies.set(cookie['name'], cookie['value'])
        
        url = f"https://www.truecaller.com/search/in/{phone_number}"
        response = session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        registered_element = soup.find(
            "div", {"class": "font-montserrat text-lg sm:text-2xl flex-none"}
        )
        truecaller_data["registered"] = (
            registered_element.text if registered_element else None
        )

        name_element = soup.find(
            "div", {"class": "font-montserrat text-lg sm:text-2xl flex-none"}
        )
        truecaller_data["name"] = name_element.text if name_element else None

        email_element = soup.findAll("div", {"class": "field__content"})
        truecaller_data["email"] = (
            email_element[-1].text if email_element and len(email_element) > 2 else None
        )

    except:
        print("error in truecaller")

    # FACEBOOK

    facebook_data = {
        "Registered": None,
        "Name": None,
        "Username": None,
        "Profile URL": None,
        "Cover URL": None,
    }

    try:
        scrap_fb = get_profile(
            username, cookies="cookies.txt"
        )  # Or get_profile("zuck", cookies="cookies.txt")

        url = f"https://www.facebook.com/{username}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        if len(scrap_fb) > 5:
            facebook_data["Registered"] = "Yes"

            facebook_data["Name"] = scrap_fb["Name"]

            # facebook_scraper package doesnot provides use the username so we are retriving it from the requests.get object
            facebook_data["Username"] = response.url.split("https://www.facebook.com/")[
                1
            ]

            facebook_data["Profile URL"] = scrap_fb["profile_picture"]

            facebook_data["Cover URL"] = scrap_fb["cover_photo"]

    except:
        facebook_data["Registered"] = "No"
        print("Username not found!")

    # GPAY

    url = f"https://gpay.app.goo.gl/{phone_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    registered_element = soup.find("div", {"class": "DfTQ5d"})
    registered = registered_element.text if registered_element else None

    name = registered
    upi_id_elements = soup.find_all("div", {"class": "DfTQ5d"})
    upi_ids = [element.text for element in upi_id_elements]

    gpay_data = {"Registered": registered, "Name": name, "UPI IDs": upi_ids}

    results = []

    results.append(("WhatsApp", whatsapp_data))

    results.append(("Truecaller", truecaller_data))

    results.append(("Facebook", facebook_data))

    results.append(("Gpay", gpay_data))

    df = pd.DataFrame(results, columns=["Platform", "Data"])

    # Data presented in Tabular format

    print(df)

    return jsonify(results)


"""
def run_app():
    app.run(debug=False, port=5002, threaded = True)
"""

if __name__ == "__main__":
    app.run(debug=True, port=5002)

    """
    # This two approaches are used to initialize_driver only once the flask server starts, as it is getting initializing twice, once on running the file itself and once after the server start
    # Multi processing
    parallelize_functions(initialize_driver, run_app)

    # Multi-threading
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=initialize_driver)
    first_thread.start()
    second_thread.start()
    """
