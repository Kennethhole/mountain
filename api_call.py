import requests
from xml.etree import ElementTree as ET

"""
This file gives some examples of API calls
"""

# Settings
api_key = '<API token key>'
SECURE_SITE_URL = 'https://ucrdm.tind.io'

"""
Other examples:

em=B
https://knowledge.uchicago.edu/search?ln=en&p=336%3ADataset&f=&action_search=Search&rm=&ln=en&sf=&so=d&rg=50&c=Knowledge+UChicago&of=hb&em=B

custom
https://xfel.tind.io/search?ln=en&cc=Thesis&p=&f=&action_search=Search&rm=&ln=en&sf=&so=d&rg=10&c=Thesis&c=&of=html&em=B

statistics
https://ucrdm.tind.io/tindstats/bibdoc_downloads?recid=14&group_by=days

"""


"""
Curl commands

curl https://ucrdm.tind.io/record/1/export/xm?apikey=<API token key>

curl -H "Authorization: Token <API token key>" https://ucrdm.tind.io/api/v1/search?ln=en&p=&f=&sf=&so=d&rg=10&of=xm




curl https://ucrdm.tind.io/search?ln=en&p=&f=&sf=&so=d&rg=10&of=xm&apikey=<API token key>
"""


def run_search_api():
    # Search API
    query_string = SECURE_SITE_URL + '/search?ln=en&p=&f=&sf=&so=d&rg=10&of=xm&apikey={}'.format(
        api_key)

    response = requests.get(query_string)
    content = response.content.decode('utf-8')
    content = content.replace('xmlns="http://www.loc.gov/MARC21/slim"', '')
    # print(content)

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

    for i, recid in enumerate(recids):
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
                                print(i, subfield.text)


# Just a change to create a new release. V3


# Start script
if __name__ == "__main__":
    print("Run search API \n")
    run_search_api()

    print("Run export API \n")
    run_export_api()
