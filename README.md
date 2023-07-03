## Profile Scraper Web App

This is a simple profile scraper which can be used to scrap data from variety of web app like WhatsApp, Facebook, TrueCaller, GooglePay.
It is build using:

- **Flask**: Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. 
- **Selenium**: Selenium is an open source umbrella project for a range of tools and libraries aimed at supporting browser automation. It provides a playback tool for authoring functional tests across most modern web browsers, without the need to learn a test scripting language.
- **BeautifulSoup** - Beautiful Soup is a Python package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML, which is useful for web scraping.

### Note:

- App is running on port 5002 so you can send the request using any browser or Postman to the endpoint /scrap-data to scrap the data for a particular number & username for example:
http://localhost:5002/scrap-data?username=virat&phone_number=7021292055

- A lot of things needs to be done manually, like Authenticating in whatsapp and clicking checkbox in confirm box and confirm box in whatsapp to allow whatsapp open a chat on the browser.

- Driver will run twice: Once on initially running the app and once after the flask server will be started. So close the initially runned driver and authenticate the whatsaoo runned after the server has been started coz all the requests will be send to the instance started after running the server. I have tried multple ways to run the driver only once after the server has started like Multi-processing, Multi-threading, Using Flask-Socket.io to run the driver only once after the server has started and not on every refresh, using " app_context " provided by flask itself but nothing worked well, the first three ways are crashing the browser whereas app_context is running the driver twice, not solving the problem in hand.

- You can adjust time.sleep( X ) based on how fast your browser is loading and your data speed. If it is super fast you can decrease the amount of time kept the code for waiting to laod a window.

- Add facebook cookies in JSON format to a file in the base folder with the name " cookies.txt ". You can use Chrome extensions like "Export cookie JSON file for Puppeteer" to export all the cookies in JSON format. If the cookies won't be send with the request facebook restricts the request.

- Learning: The script will be executed twice no matter where you place the script. Whether you keep it:

1. Above Flask instance

	`< Some Script/code >

	app = Flask(__name__)
	CORS(app)`
	
2. Below Flask instance

    `
    app = Flask(__name__)
   
    CORS(app)
	
    < Some script >
	`

4. In "__main__" section:
`
	< Some Script >

	app.run()
`

And when placed after app.run(), No Script will be executed.


### How to Run the Flask App?

1. Clone the repository.
   
`git clone https://github.com/Akshatjainbafna/Dinosys-Web-Scrapping-Assignment.git`

2. Install all the dependencies 

`pip install -r requirements.txt`

3. Run the Flask Server

`python module1.py`

4. You can request the API now.
   
`http://localhost:5002/scrap-data?username=virat&phone_number=7021292055`
