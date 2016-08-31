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
