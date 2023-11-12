import urllib.parse
import requests
from colorama import Fore, Style

# MapQuest API URL and API Key
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "5BlULEjWtVkquPIfVQBGiH6FIjQ9eAXq"

# Main loop for input and processing
while True:
    # Input for the starting location
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break

    destinations = []

    # Loop to input multiple destinations
    while True:
        dest = input("Enter a Destination (or 'quit' to finish): ")
        if dest == "quit" or dest == "q":
            break
        destinations.append(dest)

    if not destinations:
        break

    # Input for choosing units (miles or kilometers)
    units = input("Choose units (1 for miles, 2 for kilometers): ")
    if units == "quit" or units == "q":
        break

    # Check and set the unit and conversion factor
    if units == "1":
        units_str = "miles"
        conversion_factor = 1.0
    elif units == "2":
        units_str = "kilometers"
        conversion_factor = 1.60934
    else:
        print("Invalid unit selection. Please choose 1 or 2.")
        continue

    # Input for traffic information
    traffic = input("Include traffic information? (yes/no): ").lower()

    # Input for alternative routes
    alternatives = input("Include alternative routes? (yes/no): ").lower()

    for dest in destinations:
        # Construct the API request URL
        url_params = {"key": key, "from": orig, "to": dest}

        # Add traffic information parameter
        if traffic == "yes":
            url_params["routeType"] = "fastest"  # or "shortest"
            url_params["traffic"] = "true"

        # Add alternative routes parameter
        if alternatives == "yes":
            url_params["alternatives"] = "true"

        url = main_api + urllib.parse.urlencode(url_params)
        print("URL: " + url)

        # Make an API request and parse the JSON response
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            # Display successful route information
            print(Fore.GREEN + "API Status: " + str(json_status) + " = A successful route call." + Style.RESET_ALL)
            print("=" * 50)
            print(Fore.CYAN + f"Directions from {orig} to {dest}" + Style.RESET_ALL)
            print("Trip Duration: " + json_data["route"]["formattedTime"])
            print(units_str.capitalize() + ": " + str("{:.2f}".format(json_data["route"]["distance"] * conversion_factor)))
            print("=" * 50)
            print(Fore.YELLOW + "Turn-by-Turn Directions:" + Style.RESET_ALL)
            print("-" * 50)
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print(Fore.WHITE + f"{each['narrative']}" + Style.RESET_ALL)
                print(Fore.MAGENTA + f"({str('{:.2f}'.format(each['distance'] * conversion_factor))} {units_str})" + Style.RESET_ALL)
                print("-" * 50)

            # Display alternative routes
            if alternatives == "yes" and "route" in json_data and "alternateRoutes" in json_data["route"]:
                print(Fore.BLUE + "Alternative Routes:" + Style.RESET_ALL)
                for idx, alt_route in enumerate(json_data["route"]["alternateRoutes"]):
                    print(f"Route {idx + 1}")
                    print("Trip Duration: " + alt_route["formattedTime"])
                    print(units_str.capitalize() + ": " + str("{:.2f}".format(alt_route["distance"] * conversion_factor)))
                    print("-" * 50)

        elif json_status == 402:
            # Handle invalid user inputs
            print(Fore.RED + "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations." + Style.RESET_ALL)
            print("=" * 50)
        elif json_status == 611:
            # Handle missing location entries
            print(Fore.RED + "Status Code: " + str(json_status) + "; Missing an entry for one or both locations." + Style.RESET_ALL)
            print("=" * 50)
        else:
            # Display reference for other status codes
            print(Fore.RED + "For Status Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("=" * 50)
