import requests
from datetime import datetime, timedelta
from googletrans import Translator
import pycountry_convert as pc
import json
import os
from functools import lru_cache


def translate_to_turkish(text):
    translator = Translator()
    translation = translator.translate(text, dest='tr')
    return translation.text

def get_continent(country_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_map = {
            'AF': 'Afrika',
            'NA': 'Kuzey Amerika',
            'SA': 'Güney Amerika',
            'AS': 'Asya',
            'EU': 'Avrupa',
            'OC': 'Okyanusya',
            'AN': 'Antarktika'
        }
        return continent_map.get(continent_code, 'Bilinmeyen')
    except KeyError:
        return 'Bilinmeyen'
    
def get_continent_english(country_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_map = {
            'AF': 'Africa',
            'NA': 'North America',
            'SA': 'South America',
            'AS': 'Asia',
            'EU': 'Europe',
            'OC': 'Oceania',
            'AN': 'Antarctica'
        }
        return continent_map.get(continent_code, 'Unknown')
    except KeyError:
        return 'Unknown'

@lru_cache(maxsize=128)
def get_country_name(country_code):
    try:
        return pc.country_alpha2_to_country_name(country_code)
    except KeyError:
        return 'Unknown'

def fetch_and_save_data(day, lang):
    url = 'https://api.ransomware.live/recentvictims'
    response = requests.get(url)
    data = response.json()

    last_n_days = datetime.now() - timedelta(days=day)
    recent_data = []

    for entry in data:
        try:
            published_date = datetime.strptime(entry['published'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            published_date = datetime.strptime(entry['published'], '%Y-%m-%d')
        if published_date >= last_n_days:
            try:
                if entry['activity'] == 'Not Found':
                    entry['activity'] = 'Unknown'
                if lang == 'tr':
                    sectors = {
                        "Construction" : "İnşaat",
                        "Hospitality and Tourism" : "Turizm",
                        "Manufacturing" : "Üretim",
                        "Business Services" : "Profesyonel Hizmetler",
                    }
                    if entry['activity'] in sectors:
                        sector = sectors[entry['activity']]
                    else:
                        sector = translate_to_turkish(entry['activity'])
                elif lang == 'en':
                    sector = entry['activity']

                group = (entry['group_name']).capitalize()
                country_code = entry['country']

                country_dict_tr = {
                    'US': 'Amerika Birleşik Devletleri',
                    'DE': 'Almanya',
                    'TR': 'Türkiye',
                    'FR': 'Fransa',
                    'IT': 'İtalya',
                    'GB': 'Birleşik Krallık',
                    'CA': 'Kanada',
                    'NL': 'Hollanda',
                    'SE': 'İsveç',
                    'DK': 'Danimarka',
                    'ES': 'İspanya'
                }

                country_dict_en = {
                    'US': 'United States',
                    'DE': 'Germany',
                    'TR': 'Turkey',
                    'FR': 'France',
                    'IT': 'Italy',
                    'GB': 'United Kingdom',
                    'CA': 'Canada',
                    'NL': 'Netherlands',
                    'SE': 'Sweden',
                    'DK': 'Denmark',
                    'ES': 'Spain'
                }

                if lang == 'en':
                    if country_code in country_dict_en:
                        country_name = country_dict_en[country_code]
                    else:
                        country_name = get_country_name(country_code)
                elif lang == 'tr':
                    if country_code in country_dict_tr:
                        country_name = country_dict_tr[country_code]
                    else:
                        country_name = translate_to_turkish(get_country_name(country_code))

                if lang == 'en':
                    continent = get_continent_english(country_code)
                elif lang == 'tr':    
                    continent = get_continent(country_code)

                recent_data.append({
                    'group_name': group,
                    'country': country_name,
                    'continent': continent,
                    'sector': sector,
                    'published': entry['published']
                })

            except:
                pass

    json_file_name = f'data/ransomware_data_{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}.json'
    os.makedirs("data", exist_ok=True)

    try:
        with open(json_file_name, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_keys = {item['published'] + item['group_name'] for item in existing_data}
    recent_data = [item for item in recent_data if item['published'] + item['group_name'] not in existing_keys]

    with open(json_file_name, 'w', encoding='utf-8') as f:
        json.dump(existing_data + recent_data, f, ensure_ascii=False, indent=4)
    
    return json_file_name