import requests
from xml.etree import ElementTree as ET

"""
This file gives some examples of API calls
"""

# Settings
api_key = ''
SECURE_SITE_URL = ''


def run_search_api():
    # Search API
    query_string = SECURE_SITE_URL + '/search?ln=en&p=&f=&sf=&so=d&rg=10&of=xm?apikey={}'.format(
        api_key)

    response = requests.get(query_string)
    content = response.content.decode('utf-8')
    content = content.replace('xmlns="http://www.loc.gov/MARC21/slim"', '')
    print(content)

    collection = ET.fromstring(content)
    print(ET.tostring(collection))


def run_export_api():
    # Export API. Get list of record IDs. No need for of=xm
    query_string = SECURE_SITE_URL + '/api/v1/search?ln=en&p=&f=&sf=&so=d&rg=10'

    response = requests.get(query_string, headers={"Authorization": "Token {}".format(api_key)})
    # Read content
    content = response.content

    # Read as json
    data = response.json()

    # Print a list of MARC  data fields for the record IDs in the previous query
    recids = data.get('hits')
    print(len(recids))

    print_data_fields = ['245']

    for recid in recids:
        url_call = SECURE_SITE_URL + '/record/{}/export/xm?apikey={}'.format(recid, api_key)
        response = requests.get(url_call)
        # Read content (xml)
        content = response.content.decode('utf-8')

        content = content.replace('xmlns="http://www.loc.gov/MARC21/slim"', '')

        collection = ET.fromstring(content)
        for record in collection:
            for field in record:
                if field.tag == 'datafield':
                    if field.attrib['tag'] in print_data_fields:
                        for subfield in field:
                            if subfield.attrib['code'] == 'a':
                                print(subfield.text)


# Start script
if __name__ == "__main__":
    run_export_api()
