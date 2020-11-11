import requests


def get_lei_legalname(payload):
    try:
        response = requests.get(
            "https://leilookup.gleif.org/api/v2/leirecords", params=payload
        )
        data = response.json()
        if len(data) == 1:
            legal_name = data[0]["Entity"]["LegalName"]["$"]
            return legal_name.strip()
        else:  # pragma: no cover
            raise Exception(
                f"Error retrieving lei:{payload['lei']} Legal Name")

    except requests.exceptions.ConnectionError as errc:
        raise Exception(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise Exception(f"Timeout Error: {errt}")
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"Http Error: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Error: {err}")
