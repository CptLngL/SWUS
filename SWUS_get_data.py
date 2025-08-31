
import requests
import json
import os 

playset_cards = {"sor": 252, "shd": 262, "twi": 257, "jtl": 262, "lof" : 260}
gamedata: dict = {}

def GetSet(set_name):

    # Get the set json card data from swu-db
    set = set_name
    os.makedirs("data//" + set, exist_ok=True)

    url = "https://api.swu-db.com/cards/" + set
    params = {"format": "json", "pretty": "true", "order": "Number"}

    set_filepath = "data//"+set+".json"

    # If we have the json file locally already, just open the local file
    if not os.path.exists(set_filepath):
        # Get data from URL    
        response = requests.get(url, params)

        # Put in a JSON object
        data = response.json()

        with open(set_filepath, "w") as file:
            file.write(json.dumps(data, indent=4))

    else: 
         with open(set_filepath, "r") as file:
             data = json.load(file)

    # For every card download the associated card image if not done already
    for item in data["data"]:
        if (int(item["Number"]) > playset_cards[set]):
            continue;

        filepath = "data//" + set + "//" + item["Number"] + ".png"
        
        if not os.path.exists(filepath):

            # Get the image from swudb.com as their assets are better quality than swu-db
            frontArtURL = "https://swudb.com/cdn-cgi/image/quality=100/images/cards/" + set.upper() + "/" + item["Number"] + ".png" 
            
            response = requests.get(frontArtURL)

            if response.status_code == 404:
                card_id = set + "-" + item["Number"]
                raise Exception(f"Could not find URL for card {card_id}")                    
            
            print(f"Saving {filepath}")
            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        # Leader cards are double-sided, so download the back image as well            
        if item["Type"] == "Leader":
            
            filepath = "data//" + set + "//" + item["Number"] + "-b" + ".png"

            if not os.path.exists(filepath):

                # there's no standard for the name of the backside of cards. It's generally the card number post-fixed with wither -portrait,
                # -back or -b. Try until we find the correct one, or else raise an exeption
                backArtURL = "https://swudb.com/cdn-cgi/image/quality=100/images/cards/" + set.upper() + "/" + item["Number"] + "-portrait.png"

                response = requests.get(backArtURL)

                if response.status_code == 404:
                    backArtURL = "https://swudb.com/cdn-cgi/image/quality=100/images/cards/" + set.upper() + "/" + item["Number"] + "-back.png"
                    response = requests.get(backArtURL)

                if response.status_code == 404:
                    backArtURL = "https://swudb.com/cdn-cgi/image/quality=100/images/cards/" + set.upper() + "/" + item["Number"] + "-b.png"
                    response = requests.get(backArtURL)

                if response.status_code == 404:
                    card_id = set + "-" + item["Number"]
                    raise Exception(f"Could not find URL for card {card_id}")
                
                print(f"Saving {filepath}")
                with open(filepath, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

    # Delete from the json structure all elements that we don't need for gameplay
    gamedata[data["data"][0]["Set"]] = {}
    set_gamedata = gamedata[data["data"][0]["Set"]]
    for item in data["data"]: 
        if int(item["Number"]) <= playset_cards[item["Set"].lower()]:
            item.pop("BackArt", None)
            item.pop("Artist", None)
            item.pop("VariantType", None)
            item.pop("MarketPrice", None)
            item.pop("FoilPrice", None)
            item.pop("FrontArt", None)
            item.pop("LowPrice", None)
            item.pop("LowFoilPrice", None)
        
            set_gamedata[item["Number"]] = item
         

os.makedirs("data//", exist_ok=True)

GetSet("sor") # Spark of Rebellion
GetSet("shd") # Shadows of the Galaxy
GetSet("twi") # Twilight of the Republic
GetSet("jtl") # Jump to Lightspeed
GetSet("lof") # Legends of the Force

card_gamedatapath = "data//carddata.json"

print(f"Saving {card_gamedatapath}")
with open(card_gamedatapath , "w") as json_file:
     json.dump(gamedata, json_file, indent=4)
