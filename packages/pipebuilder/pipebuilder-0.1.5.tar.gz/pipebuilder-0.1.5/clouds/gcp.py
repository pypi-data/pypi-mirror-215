import googlemaps
from pipebuilder.core import core as pbcore


def get_geocode_result(address, gmaps):
    return gmaps.geocode(address)

def process_geocode_result(geocode_result, flatten_func):
    address_dict = flatten_func()
    if geocode_result:
        for dictionary in geocode_result[:2]:
            address_dict = process_address_component(dictionary, address_dict)
            address_dict = assign_additional_address_fields(dictionary, address_dict)
        return flatten_func(address_dict)
    else:
        return flatten_func()

def process_address_component(dictionary, address_dict):
    for component in dictionary['address_components']:
        address_dict[component['types'][0]] = component.short_name
    return address_dict

def assign_additional_address_fields(dictionary, address_dict):
    if address_dict.get('street_number'):
        address_dict['street_address'] = f"{address_dict['street_number']} {address_dict['route']}"
    elif address_dict.get('route'):
        address_dict['street_address'] = f"{address_dict['route']}"
    elif address_dict.get('intersection'):
        address_dict['street_address'] = f"{address_dict['intersection']}"
    else:
        address_dict['street_address'] = 'Missing Street'

    address_dict.city = address_dict.locality or address_dict.administrative_area_level_2
    address_dict.state = address_dict.administrative_area_level_1
    address_dict.formatted_address = dictionary.formatted_address
    address_dict.postal_code = address_dict.postal_code
    return address_dict

def get_googled_address(address, google_maps_key, gmaps_client=googlemaps.Client, flatten_func=pbcore.flatten):
    gmaps = gmaps_client(key=google_maps_key)
    geocode_result = flatten_func(gmaps.geocode(address))
    return process_geocode_result(geocode_result, flatten_func)
