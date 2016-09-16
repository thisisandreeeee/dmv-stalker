SLACK_CHANNEL = '#dmv' # this should be the slack channel which you want to send messages to
URL = 'https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do' # the url for the DMV web form
LOCATIONS = {
    #'San Mateo': '130'
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
    'dl_number': 'Y4497779',
    'tel_prefix': '650',
    'tel_suffix1': '660',
    'tel_suffix2': '7970'
    # format: (area-code) prefix - lineNumber
}

