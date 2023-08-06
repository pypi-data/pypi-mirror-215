import json


class Dict:

    def set_attribute(self, data):

        for k, v in data.items():
            if isinstance(v, str)or isinstance(v, int) or isinstance(v, float) or isinstance(v,bool):
                setattr(self, f"{k}", v)
            elif isinstance(v, dict):
                my_dict = Dict()
                my_dict.set_attribute(v)
                setattr(self, f"{k}", my_dict)
            elif isinstance(v, list):
                my_list = List()
                my_list_data = my_list.set_attribute(data=v, parent=k)
                if my_list_data is None:
                    setattr(self, f"{k}", v)
                setattr(self, f"{k}", my_list_data)


class List:

    def set_attribute(self, data, parent=None):

        self.temp_list = []
        for iteam in data:
            if isinstance(iteam, str)or isinstance(iteam, int) or isinstance(iteam, float) or isinstance(iteam,bool):
                self.temp_list.append(iteam)
            elif isinstance(iteam, dict):
                my_dict = Dict()
                my_dict.set_attribute(iteam)
                self.temp_list.append(my_dict)
            elif isinstance(iteam, list):
                my_list = List()
                self.temp_list.append(my_list.set_attribute(data=iteam, parent=f"{parent}+counter"))

        if len(self.temp_list) > 0:
            return self.temp_list


class JsonDecoder:

    def read_json_file(self, json_path):
        self.json_path = json_path
        self.get_data()

    def read_string(self, json_string):
        data = json.loads(json_string)
        if isinstance(data, dict):
            self.my_dict(data)
        if isinstance(data, str)or isinstance(data, int) or isinstance(data, float) or isinstance(data,bool):
            setattr(self, f"{data}", data)

    def get_data(self):
        f = open(self.json_path, 'r')
        data = json.load(f)
        if isinstance(data, dict):
            self.my_dict(data)
        if isinstance(data, list) or isinstance(data,tuple):
            self.my_list(data)
        if isinstance(data, str)or isinstance(data, int) or isinstance(data, float) or isinstance(data,bool):
            setattr(self, f"{data}", data)

    def my_dict(self, data):

        for k, v in data.items():
            if isinstance(v, str)or isinstance(v, int) or isinstance(v, float) or isinstance(v,bool):
                setattr(self, f"{k}", v)
            elif isinstance(v, dict):
                my_dict = Dict()
                my_dict.set_attribute(v)
                setattr(self, f"{k}", my_dict)
            elif isinstance(v, list):
                my_list = List()
                my_list_data = my_list.set_attribute(data=v, parent=k)
                setattr(self, f"{k}", my_list_data)

    def my_list(self, data,parent=None):
        self.temp_list = []
        for iteam in data:
            if isinstance(iteam, str) or isinstance(iteam, int) or isinstance(iteam, float) or isinstance(iteam, bool):
                self.temp_list.append(iteam)
            elif isinstance(iteam, dict):
                my_dict = Dict()
                my_dict.set_attribute(iteam)
                self.temp_list.append(my_dict)
            elif isinstance(iteam, list):
                my_list = List()
                self.temp_list.append(my_list.set_attribute(data=iteam, parent=f"{parent}+counter"))

        if len(self.temp_list) > 0:
            if parent is None:
                setattr(self, f"{0}", self.temp_list)
            else:
                setattr(self, f"{parent}", self.temp_list)

class JsonParser:

    @staticmethod
    def decode(json_object):
        json_decoder = JsonDecoder()
        try:
            if isinstance(json_object, _io.IOBase):
                json_decoder.read_json_file(json_object)
            if isinstance(json_object, str):
                json_decoder.read_string(json_object)
            if isinstance(json_decoder, dict):
                json_decoder.read_string(str(json_object))
            return json_decoder
        except Exception:
            raise TypeError("Object type is not supported")
