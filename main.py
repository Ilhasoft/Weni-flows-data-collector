import yaml, requests
import sys

def catch_urls(service_name):
    services_urls = {
        "flows": "https://new.push.al/api/v2/flows.json",
        "flow_starts": "",
        "fields": "",
        "contacts": "",
        "classifiers": "",
        "channel_evetns": "",
        "channels": "",
        "campaigns": "",
        "campaign_events": "https://new.push.al/api/v2/campaign_events.json",
        "flow_runs": "",
        "contacts_stats": "",
        "channel_stats": "",
        "runs": "",
        "messages": "",
        "labels": "",
        "groups": "",
        "globas": ""
    }
    teste = str(services_urls.get(service_name, False))
    print(teste)
    if teste == "False":
        print(f"the service {service_name} dont have Url... try review the payload.yaml")
        sys.exit() 
    return teste

def get_data(endpoint, authorization):
    response = requests.get(endpoint, headers={"authorization": authorization})
    json_response = response.json()
    print(json_response)

    return json_response

def data_to_spreasheet():
    pass

def post_in_google_sperasheets():
    pass

if __name__ == '__main__':

    with open("payload.yaml", 'r') as payload:
        try:
            payload_doc = yaml.load(payload, Loader=yaml.FullLoader)
            authorization = payload_doc['informations']['api_token']

            for service in payload_doc['functions']:
                url = catch_urls(service)
                params = "?"

                try: 
                    for param in payload_doc['functions'][service]["params"]:
                        param_value = payload_doc['functions'][service]["params"][param]
                        if params == '?':
                            params += param + "=" + param_value
                        else:
                            params += "&" + param + "=" + param_value
                
                except TypeError as exc:
                    continue
                
                name_of_doc = payload_doc['functions'][service]["spreadsheet_name"]
                endpoint = url + params

                #print(f"Documento = {name_of_doc}\nEndpoint = {endpoint}")
                get_data(endpoint, authorization)
                #print(service)
                
        except yaml.YAMLError as exc:
            print(exc)
        