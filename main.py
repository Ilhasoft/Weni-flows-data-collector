import sys, os

import requests
import yaml, json
import pandas as pd
from datetime import datetime


def format_date(inicial_date, final_date):
    inicial_date = inicial_date + "T00:00:01.0000"
    final_date = final_date + "T23:59:59.0000"
    pass



def catch_urls(service_name):
    services_urls = {
        "flows": "https://new.push.al/api/v2/flows.json",
        "flow_starts": "https://new.push.al/api/v2/flow_starts.json",
        "fields": "https://new.push.al/api/v2/fields.json",
        "contacts": "https://new.push.al/api/v2/contacts.json",
        "classifiers": "https://new.push.al/api/v2/classifiers.json",
        "channel_events": "https://new.push.al/api/v2/channel_events.json",
        "channels": "https://new.push.al/api/v2/channels.json",
        "campaigns": "https://new.push.al/api/v2/campaigns.json",
        "campaign_events": "https://new.push.al/api/v2/campaign_events.json",
        "flow_runs": "https://new.push.al/api/v2/analytics/flow-runs.json",
        "contacts_stats": "https://new.push.al/api/v2/analytics/contacts.json",
        "channel_stats": "https://new.push.al/api/v2/channel_stats.json",
        "runs": "https://new.push.al/api/v2/runs.json",
        "messages": "https://new.push.al/api/v2/messages.json",
        "labels": "https://new.push.al/api/v2/labels.json",
        "groups": "https://new.push.al/api/v2/groups.json",
        "globals": "https://new.push.al/api/v2/globals.json"
    }
    url = str(services_urls.get(service_name, False))
    if url == "False":
        print(f"the service {service_name} dont have Url... try review the payload.yaml")
        sys.exit()
    return url


def get_data(endpoint, authorization, document_name):
    response = requests.get(endpoint, headers={"authorization": authorization})
    json_response = response.json()

    try:
        sheet_data = []
        for data in json_response['results']:
            sheet_data.append(data)
        df = pd.DataFrame(sheet_data)
        writer = pd.ExcelWriter(f'teste/xlsx/{document_name}.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()

    except KeyError:
        print("cannot find any response!")

    with open(f"teste/json/{document_name}.json", 'w') as json_doucument:
        json.dump(json_response, json_doucument)


def data_to_spreasheet():
    pass


def post_in_google_sperasheets():
    pass


if __name__ == '__main__':
    with open("payload.yaml", 'r') as payload:
        is_recurrence = payload_doc['informations']['is_recurrence']
        recurrence_type = payload_doc['informations']['recurrence_type']
        if is_recurrence is True:
            if recurrence_type = "D":
                now = datetime.now()
                inicial_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "T00:00:01.0000"
                final_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "T23:59:59.0000"

            elif recurrence_type = "M":
                now = datetime.now()
                if now.month = 1:
                    inicial_date = str(now.day) + "-" + str(12) + "-" + str(now.year - 1) + "T00:00:01.0000"
                    final_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "T23:59:59.0000"
                else:
                    inicial_date = str(now.day) + "-" + str(now.month - 1) + "-" + str(now.year) + "T00:00:01.0000"
                    final_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "T23:59:59.0000"
                        

            elif recurrence_type = "Y":
                now = datetime.now()
                inicial_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year - 1) + "T00:00:01.0000"
                final_date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "T23:59:59.0000"

            else:
                pass
        
        else:
            inicial_date = payload_doc['informations']['inicial_date']
            final_date = payload_doc['informations']['final_date']
            format_date(inicial_date, final_date)

        try:
            """
                busque pela data do .yaml e insira o período entre elas como
                base_path (lembrando de verificar e calcular as datas iniciais
                e finais de acordo com o período caso seja recorrente)
            """
            base_path = f"{inicial_date}_to_{final_date}"
            json_path = f"{base_path}/json/"
            xlsx_path = f"{base_path}/xlsx/"

            os.mkdir(base_path)
            os.mkdir(json_path)
            os.mkdir(xlsx_path)

        except FileExistsError:
            pass

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

                except KeyError:
                    print("internal problem")
                document_name = payload_doc['functions'][service]["document_name"]

                # concatenar com a data inicial e a data final correspondente ao período
                endpoint = url + params
                get_data(endpoint, authorization, document_name)

        except yaml.YAMLError as exc:
            print(exc)
