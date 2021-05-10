import yaml

teste = {
            "teste": {
                "a": "b"
            }
        }  

with open('./testedsaddsd.yaml', 'w') as payload_doc:
    yaml.dump(teste, payload_doc, default_flow_style=False) 