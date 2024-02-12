import requests
import urllib.parse


class OverpassApi:
    def __init__(self):
        self.overpass_url = "https://overpass-api.de/api/interpreter/"

    def post_request(self):
        query = """
            [bbox:30.618338,-96.323712,30.591028,-96.330826]
            [out:json]
            [timeout:90]
            ;
            (
                way
                    (
                         57.04771,
                         -96.348809105664,
                     );
            );
            out geom;
        """


        # Define the URL
        url = "https://overpass-api.de/api/interpreter"

        # Make the POST request
        response = requests.post(self.overpass_url, data={"data": query})

        # Get the JSON response
        json_response = response.json()

        # Print the JSON response
        print(json_response)


if __name__ == "__main__":
    overpass = OverpassApi()
    overpass.post_request()
