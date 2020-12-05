from rasa_sdk import Action
import requests
import ast
from rasa_sdk.events import SlotSet

class ActionSetLocation(Action):

    def name(self):
        return "action_set_location"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message['text']

        dispatcher.utter_message(
            template="Thanks for sharing you location. " + str(user_input).capitalize() + " is pretty place.")
        return [SlotSet("location", str(user_input))]

class Zomato:

    def __init__(self):
        self.api_key = "bd67fe47d5dafc4e4e5dafc4e4e92"  # Update Zomato API key here
        self.base_url = "https://developers.zomato.com/api/v2.1/"

    def getZomatoLocationInfo(self, location):

        location_info = []

        queryString = {"query": location}

        headers = {'Accept': 'application/json', 'user-key': self.api_key}

        res = requests.get(self.base_url + "locations", params=queryString, headers=headers)

        data = res.json()

        if len(data['location_suggestions']) == 0:
            raise Exception('invalid_location')

        else:
            location_info.append(data["location_suggestions"][0]["latitude"])
            location_info.append(data["location_suggestions"][0]["longitude"])
            location_info.append(data["location_suggestions"][0]["entity_id"])
            location_info.append(data["location_suggestions"][0]["entity_type"])
            return location_info

    def get_cuisines(self, location_info):

        headers = {'Accept': 'application/json', 'user-key': self.api_key}

        queryString = {
            "lat": location_info[0],
            "lon": location_info[1]
        }

        res = requests.get(self.base_url + "cuisines", params=queryString, headers=headers).content.decode("utf-8")

        a = ast.literal_eval(res)
        all_cuisines_in_a_city = a['cuisines']

        cuisines = {}

        for cuisine in all_cuisines_in_a_city:
            current_cuisine = cuisine['cuisine']
            cuisines[current_cuisine['cuisine_name'].lower()] = current_cuisine['cuisine_id']

        return cuisines

    def get_cuisine_id(self, cuisine_name, location_info):

        cuisines = self.get_cuisines(location_info)

        return cuisines[cuisine_name.lower()]

    def get_all_restraunts(self, location, cuisine):

        location_info = self.getZomatoLocationInfo(location)
        cuisine_id = self.get_cuisine_id(cuisine, location_info)

        queryString = {
            "entity_type": location_info[3],
            "entity_id": location_info[2],
            "cuisines": cuisine_id,
            "count": 5
        }

        headers = {'Accept': 'application/json', 'user-key': self.api_key}
        res = requests.get(self.base_url + "search", params=queryString, headers=headers)

        list_of_all_rest = res.json()["restaurants"]

        json = []
        for rest in list_of_all_rest:
            name = rest["restaurant"]["name"]
            thumb = rest["restaurant"]["thumb"]
            url = rest["restaurant"]["url"]
            json.append(name)
            json.append(thumb)
            json.append(url)

        return json

    def get_all_restraunts_without_cuisne(self, location):

        location_info = self.getZomatoLocationInfo(location)

        queryString = {
            "entity_type": location_info[3],
            "entity_id": location_info[2],
            "count": 5
        }

        headers = {'Accept': 'application/json', 'user-key': self.api_key}
        res = requests.get(self.base_url + "search", params=queryString, headers=headers)

        list_ofall_rest = res.json()["restaurants"]
        names_of_all_rest = []
        for rest in list_ofall_rest:
            name = rest["restaurant"]["name"]
            thumb = rest["restaurant"]["thumb"]
            url = rest["restaurant"]["url"]
            list_ofall_rest.append(name)
            list_ofall_rest.append(thumb)
            list_ofall_rest.append(url)

        return names_of_all_rest


class ActionShowRestaurants(Action):

    def name(self):
        return "action_show_restaurants"

    def run(self, dispatcher, tracker, domain):

        user_input = tracker.latest_message['text']

        zo = Zomato()

        cuisine_type = tracker.get_slot('cuisine')
        list_all_restaurants = zo.get_all_restraunts(location=str(user_input), cuisine=str(cuisine_type))

        if list_all_restaurants:
            finaldata = []
            for i in range(len(list_all_restaurants)):
                if i % 3 != 0:
                    continue

                mydata = {
                    "title": list_all_restaurants[i],
                    "image_url": list_all_restaurants[i + 1],
                    "subtitle": "I don't know anything about it",
                    "default_action": {
                        "type": "web_url",
                        "url": list_all_restaurants[i + 2],
                        "webview_height_ratio": "tall"
                    },
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": list_all_restaurants[i + 2],
                            "title": "View Website"
                        }, {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "DEVELOPER_DEFINED_PAYLOAD"
                        }
                    ]
                }

                finaldata.append(mydata)

            message = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": "{}".format(finaldata)
                    }
                }
            }

            dispatcher.utter_message(json_message=message)
        else:
            dispatcher.utter_message(template=
                                        "Sorry no such restaurant of " + cuisine_type.capitalize() + " available at " + str(user_input) + ". Try looking for some other cuisine.")

        return []