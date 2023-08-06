...


class APIRenderer:
    def render(self, response_obj):
        if isinstance(response_obj, list):
            output = []
            for response in response_obj:
                output.append(self.render(response))
        elif isinstance(response_obj, dict):
            output = {}
            for key, value in response_obj.items():
                output_key = self.render_key(key)
                output[output_key] = value
        return output
    
    def render_key(self, key):
        key = self.snakify(key)
        
        if ("_high_") in key:
            key = key.replace("_high_", "_h_")
        if ("_low_") in key:
            key = key.replace("_low_", "_l_")
        if ("_set_point") in key:
            key = key.replace("_set_point", "_sp")
        if ("_humidity_") in key:
            key = key.replace("_humidity_", "_hum_")
        if ("_temperature_") in key:
            key = key.replace("_temperature_", "_temp_")

        return key
    
    def snakify(self, camel):
        snake_output = ""
        for char in camel:
            if char.isupper():
                char = f"_{char.lower()}"
            snake_output += char
        return snake_output