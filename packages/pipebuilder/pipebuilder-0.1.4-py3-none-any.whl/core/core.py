import json
import pandas as pd
import xmltodict

from box import BoxList, SBox

def convert_str_to_bool(value):
    if isinstance(value, str):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
    return value


def replace_at_symbol(d):
    new_dict = {}
    for key, value in d.items():
        new_key = key.lstrip('@')  # Remove '@' at the start of the key
        if isinstance(value, dict):  # If value is a dictionary, call the function recursively
            new_dict[new_key] = replace_at_symbol(value)
        else:
            new_dict[new_key] = value
    return new_dict


def convert_dict_values(d):
    for key, value in d.items():
        if isinstance(value, dict):
            d[key] = convert_dict_values(value)
        else:
            d[key] = convert_str_to_bool(value)
    return d


def convert_columns_to_boolean(df):
    for col in df.columns:
        unique_values = df[col].dropna().unique()
        true_false_values = {'true', 'false'}

        if set(unique_values).issubset(true_false_values):
            df[col] = df[col].apply(lambda x: pd.NA if pd.isnull(x) else x.lower() == 'true')
        else:
            df[col] = df[col].apply(lambda x: pd.NA if pd.isnull(x) else x)

    return df

def explode_on(d, col):
        d = d.reset_index(drop=True)
        d[col] = d[col].fillna({i: {} for i in d.index})
        d = d.join(pd.json_normalize(d[col]), rsuffix=f"_{col}")
        d = d.drop(columns=[col])


def handle_str(d):
    return json.loads(d)

def handle_dataframe(d, sort_dict_keys=False):
    if d.shape[0] == 1:
        d = d.iloc[0].to_json(date_format="iso")
        d = dict(handle_str(d))
    return d

def handle_series(d):
    d = d.to_json(date_format="iso")
    return dict(handle_str(d))

def handle_dict(d, sort_dict_keys=False):
    d = json.dumps(d, indent=4, sort_keys=sort_dict_keys, default=str)
    d = json.loads(d)
    d = dict(convert_dict_values(d))
    d = dict(replace_at_symbol(d))
    return d

def handle_list(d, slug=True):
    d = BoxList(
        d,
        box_class=SBox,
        camel_killer_box=slug,
        default_box=True,
        default_box_none_transform=True,
        box_dots=True,
    )
    return d

def handle_dataframe_final(d, slug=True):
    d = convert_columns_to_boolean(d)
    d = d.to_json(orient="records", date_format="iso")
    d = handle_str(d)
    d = BoxList(
        d,
        box_class=SBox,
        camel_killer_box=slug,
        default_box=True,
        default_box_none_transform=True,
        box_dots=True,
    )
    d = pd.DataFrame(d.to_list())
    return d

def clean_dict(d):
    keys_to_remove_if_empty=['read', 'iter']
    return {key: value for key, value in d.items() if not (key in keys_to_remove_if_empty and value == {})}

def flatten(d={}, sort_dict_keys=False, slug=True):
    try:
        d = xmltodict.parse(d)
    except:
        pass

    if isinstance(d, str):
        d = handle_str(d)
    elif isinstance(d, pd.DataFrame):
        d = handle_dataframe(d, sort_dict_keys)
    elif isinstance(d, pd.Series):
        d = handle_series(d)
    elif isinstance(d, dict):
        d = handle_dict(d, sort_dict_keys)
        d = SBox(
            d,
            camel_killer_box=slug,
            default_box=True,
            default_box_none_transform=True,
            box_dots=True,
        )
    elif isinstance(d, list):
        d = handle_list(d, slug)
    elif isinstance(d, pd.DataFrame):
        d = handle_dataframe_final(d, slug)

    d = clean_dict(d)
    
    return d
