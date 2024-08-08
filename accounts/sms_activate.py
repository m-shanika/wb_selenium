from dataclasses import dataclass
import requests
import time

@dataclass
class SMSActivate:
    API_KEY: str
    base_url: str = "https://api.sms-activate.io/stubs/handler_api.php"

    def __request(self, action: str, params: dict = {}):
        query = {
            'api_key': self.API_KEY,
            'action': action,
        }
        query.update(params)
        response = requests.get(self.base_url, params=query)
        response.raise_for_status()  
        return response.text

    def get_balance(self):
        response = self.__request("getBalance")
        return float(response.split(':')[1])

    def get_number(self):
        response = self.__request("getNumber", {'service': 'uu', 'country': '0'})
        data = response.split(':')
        print(data)
        if data[0] == "ACCESS_NUMBER":
            return {'activationId': data[1], 'phoneNumber': data[2]}
        else:
            raise Exception(f"Failed to get number: {response}")

    def get_status(self, id: str):
        response = self.__request("getStatus", {'id': id})
        return response

    def set_status(self, id: str, status: int):
        response = self.__request("setStatus", {'id': id, 'status': status})
        return response

    def wait_for_sms(self, id: str, timeout: int = 300):
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status(id)
            if "STATUS_OK" in status:
                return status.split(':')[1]
            elif "STATUS_WAIT_CODE" in status:
                print("Number is ready to receive SMS, waiting for SMS...")
            time.sleep(5)
        raise TimeoutError("Timeout waiting for SMS")
