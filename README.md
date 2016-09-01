# Stalk the DMV
A good friend of mine, Juho, casually mentioned how much of a pain it was to get an appointment for a driving test at the DMV. The only available appointments were in 3 months, and although it was possible to secure an earlier appointment if someone else deleted theirs - it was way too tedious (and mundane) to manually check the DMV page ever so often.

Enter, [Selenium](http://selenium-python.readthedocs.io/).

We originally wanted to programmatically send POST requests to their web form and scrape the response for any available appointments, but this proved tricky as the DMV page was being dynamically generated with Javascript. Thankfully, Selenium (originally a web testing tool), provides us with an amazing set of tools to interact with their web page through a headless browser, as though the program is a real person.

## Installation and Usage
Grab your local copy.
```
git clone https://github.com/thisisandreeeee/stalk-the-DMV.git
```
Install the dependencies, which includes python libraries and phantomjs.
```
pip install -r requirements.txt

# On OSX
brew install phantomjs

# On Linux
cd ~
export PHANTOM_JS="phantomjs-1.9.8-linux-x86_64"
wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
sudo tar xvjf $PHANTOM_JS.tar.bz2
sudo mv $PHANTOM_JS /usr/local/share
sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin
```
Obtain a [slack token](https://api.slack.com/docs/oauth-test-tokens). Then, create a config file - this should be kept hidden! In the current directory, enter the following:
```
echo "SLACK_TOKEN='your-token-here'" >> creds.py
```
Don't forget to replace the string above with your own slack token. When that is done, open `settings.py` and update it with your information.
```python
SLACK_CHANNEL = '#dmv' # this should be the slack channel which you want to send messages to
URL = 'https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do' # the url for the DMV web form
LOCATIONS = {
    'San Mateo': '130', # the office ID obtained by inspecting the xpath, this is what selenium uses to identify the correct option
    'Redwood City': '109',
    'San Jose': '125',
    'Daly City': '28'
}
PROFILE = {
    'first_name': 'ANDRE',
    'last_name': 'TAN',
    'mm': '09',
    'dd': '28',
    'yyyy': '1993',
    'dl_number': 'your-dl-number-here',
    'tel_prefix': 'your-area-code-here',
    'tel_suffix1': 'your-prefix-here',
    'tel_suffix2': 'your-line-number-here'
    # format: (area-code) prefix - lineNumber
}
```
Run the bot.
```
python main.py
```

## So what exactly does it do?
The bot will run once every 15 minutes, provided that the current time is during the day. It checks whether there are any available appointments at the predefined locations, and posts the earliest appointment in the slack channel. 

## Cool features
- If the next appointment is coming up real soon, we want to know ASAP. The bot will recognize when the earliest appointment for a specific DMV office is in the current month, and tag the users within the slack channel to bring the information immediately to attention. All other appointments will still be posted in the slack channel, but users will not be tagged. Although this can be improved to check for appointments that are within X number of days, this program was written at the beginning of the month and I did not foresee my hunt for an appointment extending towards the end of the month - hence there was no need for premature optimization and this hackish solution would suffice.
- Everytime a new appointment is found at an office, the data will be stored in an SQLite database if it does not already exist within the database. Then, whenever a bot wishes to send a notification on a new appointment to the channel, it checks the database to ensure that it has not already notified users of an existing appointment.
- All actions within the script are being logged, which makes it extremely easy to debug in the case that something goes awry.
- Selenium enables us to mimic the actual action of a human. To view this with a GUI, go to `scraper.py` and swap out the following two lines.
```python
browser = webdriver.PhantomJS('phantomjs') # phantomjs is a headless browser which lets us run the script in a CLI environment
browser = webdriver.Chrome('./chromedriver') # replace the above line with this, which instantiates with a chrome driver instead
```
If you do not have the chromedriver file installed, enter the following into your terminal (OSX only, with wget installed) while in the same directory as `main.py`.
```
wget http://chromedriver.storage.googleapis.com/2.23/chromedriver_mac64.zip
unzip chromedriver_mac64.zip
rm chromedriver_mac64.zip
```

