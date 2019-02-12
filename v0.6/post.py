import requests

class http:
    def post(self, web_address, json_to_send, debug=False):
        if debug == True:
            print("Web address: ", web_address)
            print("Data to send: ", json_to_send)
        requests.post(web_address, json=json_to_send, verify=False)
