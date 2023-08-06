import requests
import json

from typing import Union, Any

class Connect:
    def __init__(self, api_key: str = None):
        self.model = None
        self.endpoint = None
        self.background_job = None
        self.flow = None
        self.beautify = False
        self.get_response = True
        self.base_domain = "https://inference.plugger.ai"
        self.test_temporary_image_domain = "https://tmp.cameralyze.co"
        self.upload_url = "https://platform.api.plugger.ai/tmp/upload"
        self.platform_url = "https://platform.cameralyze.co"
        self.api_key = api_key
        self.configuration = None
        
    def beautify_response(self):
        self.beautify = True
        
        return self
        
    def open_response(self):
        self.get_response = True
        
        return self
        
    def close_response(self):
        self.get_response = False
        
        return self
        
    def set_api_key(self, api_key: str):
        self.api_key = api_key
        
        return self
        
    def set_model(self, model: str):
        """
        Args:
            model (str): Model UUID or model alias name
        """
        self.model = model
        
        return self   

    def read_file(self, path: str) -> str:
        file = path.split("/")[-1]
        
        with open(path, 'rb') as local_file:
            local_file_body = local_file.read()
            
        response = requests.put(
            "{url}/{file}".format(url=self.upload_url, file=file), 
            data=local_file_body,
            headers={'Content-Type': 'application/octet-stream'}
        )
        
        print(response.status_code)

        return "{test_temporary_image_domain}/{file}".format(
            test_temporary_image_domain=self.test_temporary_image_domain, 
            file=file
        )

    def __get_json(self, image: Union[str, tuple] = None, text:str = None, **kwargs: Any) -> dict:
        json={"rawResponse": not self.beautify, "getResponse": self.get_response, "input": kwargs}

        if image != None:
            if isinstance(image, tuple):
                json["fileId"] = image[0]
                json["fileType"] = image[1]
            elif image.startswith("http"):
                json["url"] = image
            elif image != None:
                json["image"] = image
            
        if text != None:
            json["text"] = text
            
        if self.model:
            json["itemUuid"] = self.model
        
        if self.configuration != None:
            json["configuration"] = self.configuration

        return json

    def predict(self, image: Union[str, tuple] = None, text: str = None, **kwargs: Any) -> dict:
        api_call = requests.post(
            self.base_domain,
            headers={"x-api-key": self.api_key, "Content-Type": "application/json"},
            data=json.dumps(self.__get_json(image=image, text=text, **kwargs))
        )

        return api_call.json() 

    def show_configuration(self):
        print(
            "You can see configuration in here:\n{platform_url}/model-detail/{model}".format(
                platform_url=self.platform_url,
                model=self.model
            )
        )
    
    def set_configuration(self, configuration: dict):
        self.configuration = configuration

        return self
