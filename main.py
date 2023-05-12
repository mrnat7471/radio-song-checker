import requests
import json
from datetime import datetime
import logging
import os 
from discord_webhook import DiscordWebhook

def find_non_unknown():
    try:
        logging.info(f"Finding new data")
        for song2 in newdata['_embedded']:
            if song2['extraInfo']['primaryGenreName']:
                if song2['extraInfo']['primaryGenreName'] == 'Karaoke':
                    print("Karaoke song passing")
                    pass
            if song2['album'] == 'Unknown Album':
                print("Unknown Album passing")
                pass
            elif 'karaoke' in song2['title']:
                print("Karaoke song passing")
                pass
            else:
                test = requests.put(f"https://app.radiopanel.co/api/v1/songs/{songuuid}",json=song2, headers={"x-tenant":"", "Authorization": ""})
                test = test.json()
                logging.info(test)
                test2 = requests.get(f"https://app.radiopanel.co/api/v1/songs/{songuuid}", headers={"x-tenant":"", "Authorization": ""})
                test2 = test2.json()
                logging.info(test2)
                if song2['extraInfo']['primaryGenreName'] == 'Karaoke':
                    logging.info("Unable to find acceptable data!")
                    webhook2 = DiscordWebhook(url='', content=f'Unable to find acceptable data for {song3} (https://cms.reachradio.co.uk/songs/{songuuid})')
                    webhook2.execute()
                elif song2['album'] == 'Unknown Album':
                    logging.info("Unable to find acceptable data!")   
                break
            logging.info("here")
    except:
        logging.info("fuck")

dir_path = os.path.dirname(os.path.realpath(__file__))
LOG_FILENAME = datetime.now().strftime(f'{dir_path}/logs/logfile_%H_%M_%S_%d_%m_%Y.log')
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)    
logging.info('Lets get started....')



r = requests.get("https://app.radiopanel.co/api/v1/songs?pagesize=100000", headers={"x-tenant":"", "Authorization": ""})
r = r.json()
for song in r['_embedded']: 
    try:  
        karaoke = song['extraInfo']['primaryGenreName']
    except:
        karaoke = "non"
    if song['album'] == 'Unknown Album':
        logging.info(song) 
        songuuid = song['uuid']
        song3 = f"{song['artist']} - {song['title']}"
        song2 = f"{song['artist']} - {song['title']} (https://cms.reachradio.co.uk/songs/{songuuid})"
        logging.info(song2)
        newdata = requests.get(f"https://app.radiopanel.co/api/v1/songs/search?title={song3}", headers={"x-tenant":"", "Authorization": ""})
        newdata = newdata.json()
        find_non_unknown()
    elif karaoke == 'Karaoke':
        songuuid = song['uuid']
        song3 = f"{song['artist']} - {song['title']}"
        song2 = f"{song['artist']} - {song['title']} (https://cms.reachradio.co.uk/songs/{songuuid})"
        logging.info(song2)
        newdata = requests.get(f"https://app.radiopanel.co/api/v1/songs/search?title={song3}", headers={"x-tenant":"", "Authorization": ""})
        newdata = newdata.json()
        find_non_unknown()
    elif 'karaoke' in song['title']:
        songuuid = song['uuid']
        song3 = f"{song['artist']} - {song['title']}"
        song2 = f"{song['artist']} - {song['title']} (https://cms.reachradio.co.uk/songs/{songuuid})"
        logging.info(song2)
        newdata = requests.get(f"https://app.radiopanel.co/api/v1/songs/search?title={song3}", headers={"x-tenant":"c9a65443-eed1-41ed-b9d2-743223b5ee75", "Authorization": "Basic ZDI1ZWFiZGItYTk0MC00Mjg4LTg2MTMtMDkxZjBjNzg1NTg0Og=="})
        newdata = newdata.json()
        find_non_unknown()
logging.info("No new songs to edit!")


