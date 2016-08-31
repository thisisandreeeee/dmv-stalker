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

## How It Works
The bot will run once every 15 minutes, provided that the current time is during the day. It checks whether there are any available appointments at the predefined locations, and posts the earliest appointment in the slack channel. If the earliest appointment is during the current month, that's really awesome - so the bot will tag all users within that channel to bring the information immediately to attention.
