import requests
import json
import pandas as pd
import datetime
from datetime import date, time, timedelta

# returns a set of IS064 timestamps for the beginning and end of last week as a dictionary
def get_timestamps():
    # define dates for last monday and last sunday
    last_week = datetime.datetime.now() - timedelta(days= 7)
    start_last_week = last_week - timedelta(days=last_week.weekday())
    end_last_week = start_last_week + timedelta(days=6)
    # convert those dates into ISO64 timestamps for the beginning of monday and the end of sunday
    start_last_week_iso = start_last_week.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    end_last_week_iso = end_last_week.replace(hour=11, minute=59, second=59, microsecond=0).isoformat() + 'Z'
    # create a dictionary
    time_stamps = {'start_iso':start_last_week_iso, 'end_iso':end_last_week_iso}
    return(time_stamps)

def make_request_changed_providers(time_stamps):
    # make reponse using changes CQC endpoint
    response = requests.get(
        "https://api.cqc.org.uk/public/v1/changes/provider?startTimestamp={}&endTimestamp={}".format(get_timestamps()['start_iso'],get_timestamps()['end_iso'])
        )
    return(response)

def make_request_provider_information(provider_id):
    # make reponse using providers CQC endpoint
    response = requests.get(
        'https://api.cqc.org.uk/public/v1/providers/{}'.format(provider_id)
        )
    return(response)
# define an extract function which gets a list of provider information for providers who have had a changed CQC rating last week
def extract_data():
    # extract a list of organisations of the given type that have changed last week
    providers = pd.DataFrame(make_request_changed_providers(get_timestamps()).json())
    provider_id = providers['changes'].to_list()
    # for the list of providers append all data into a single list
    data = []
    for id in provider_id:
        data.append(make_request_provider_information(id).json())
    return(data)
# define a load function to write data to output
def load_data(data):
    # write json to text file
    f = open("output/data.txt", "w")
    for provider in data:
        f.write(str(provider) + '\n')
    f.close()
    return(None)

print('Extracting Data')
data = extract_data()
print('Loading Data')
load_data(data)
