import requests


class http:
    def post(self, web_address, key, data_to_send, debug):
        if debug == True:
            print("Web addrs: ", web_address)
            print("Key: ", key)
            print("Data to send: ", data_to_send)
        requests.post(web_address, data={key: data_to_send})
