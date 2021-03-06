# I'm going to develop some covid19 tracking for myself here.
# https://covidtracking.com/data/api

import requests
from pprint import pprint

state = 'ok'
url_current = 'https://api.covidtracking.com/v1/us/current.json'
url_state_current = f'https://api.covidtracking.com/v1/states/{state}/current.json'
url_state_historical = f'https://api.covidtracking.com/v1/states/{state}/daily.json'

page_c = requests.get(url_state_current)
page_h = requests.get(url_state_historical)

# We receive a single dictionary embedded in a list for some reason,
# so let's take it out of the list with [0].
# I'm also type-hinting here so pycharm helps with code completion.
data_current: dict = page_c.json()[0]
data_historical: dict = page_h.json()[0]

# ///////////////////////////// Data Variables. ////////////////////////////////
data_timestamp        = data_current['lastupdateEt']
data_quality          = data_historical['dataQualityGrade']
# Covid-19 Testing. ------------------------------------------------------------
pending_tests         = data_current['pending']
# Confirmed + probably cases.
positives             = data_current['positive']
# Completed antibody tests with positive result.
positives_antibody    = data_current['positiveTestsAntibody']
# Unique positive PCR or other approved NAAT test.
positives_viral       = data_current['positiveCasesViral']
positives_increase    = data_current['positiveIncrease']
# People tested per day with PCR.
daily_test_amt        = data_current['totalTestEncountersViral']
probable_cases        = data_current['probableCases']
recovered             = data_current['recovered']
national_total_est    = data_current['totalTestResults']
national_increase     = data_current['totalTestResultsIncrease']
# Casualties. ------------------------------------------------------------------
deaths                = data_current['death']
death_increase        = data_current['deathIncrease']
hospitalized_lifetime = data_current['hospitalizedCumulative']
hospitalized_current  = data_current['hospitalizedCurrently']
hospitalized_increase = data_current['hospitalizedIncrease']
ICU_current           = data_current['inIcuCurrently']
ICU_lifetime          = data_current['inIcuCumulative']
ventilator_current    = data_current['onVentilatorCurrently']
ventilator_lifetime   = data_current['onVentilatorCumulative']

# TODO: Make this a class since so many variables are the same for the
# data coming in, and the data is determined by the URL.
# For example "current" and "historical" data points use the same names but give
# different numbers of course.
# TODO: Track data in meaningful way.
# TODO: Display data in interactable, visual and meaningful way.