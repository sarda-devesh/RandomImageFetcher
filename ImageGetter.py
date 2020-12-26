import random
import string
import requests
from requests.models import Response

class ImageGenerator:
    def generate_random_string(length): 
      ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def __init__(self, file_path):
      self.image_urls = {}
      with open(file_path, 'r') as input_file: 
          lines = input_file.readlines()
          for line in lines: 
              line_broken = line.split(",")
              key_value = line_broken[0].strip()
              url_template = line_broken[1].strip()
              self.image_urls[key_value] = [url_template]
              if(len(line_broken) > 2): 
                  self.image_urls[key_value].append(line_broken[2].strip())
    
    def get_random_image_url(self, source_name): 
        if(source_name not in self.image_urls):
            return ""
        source_name_data = self.image_urls[source_name]
        url_template = source_name_data[0]
        while("<" in url_template):
            starting_index = url_template.index("<")
            end_index = starting_index
            while(url_template[end_index] != ">"):
                end_index += 1
            random_data_info = url_template[starting_index + 1 : end_index].split(":")
            data_type = random_data_info[0].strip()
            data_range = random_data_info[1].split("-")
            lower_value, upper_value = data_range[0].strip(), data_range[1].strip()
            to_subtitue = ""
            if(data_type == "int"):
                lower_value = int(lower_value)
                upper_value = int(upper_value)
                to_subtitue = str(random.randint(lower_value, upper_value))
            elif(data_type == "float"): 
                lower_value = float(lower_value)
                upper_value = float(upper_value)
                to_subtitue = str(random.uniform(lower_value, upper_value))
            else: 
                lower_value = int(lower_value)
                upper_value = int(upper_value)
                to_subtitue = self.generate_random_string(random.randint(lower_value, upper_value))
            url_template = url_template[:starting_index] + to_subtitue + url_template[end_index + 1 : ]
        response = requests.get(url_template)
        image_url = response.url
        if(len(source_name_data) > 1):
            url_key = source_name_data[1]
            image_url = response.json()[url_key]
        return image_url
