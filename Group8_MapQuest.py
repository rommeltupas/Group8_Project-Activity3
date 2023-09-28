import urllib.parse
import requests
from colorama import Fore, Style

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "5BlULEjWtVkquPIfVQBGiH6FIjQ9eAXq"

orig = input("Starting Location: ")

if orig != "quit" and orig != "q":
    destinations = []

    while True:
        dest = input("Enter a Destination (or 'quit' to finish): ")
        if dest == "quit" or dest == "q":
            break
        destinations.append(dest)

    if destinations:
        units = input("Choose units (1 for miles, 2 for kilometers): ")
        if units != "quit" and units != "q":
            if units == "1":
                units_str = "miles"
                conversion_factor = 1.0
            elif units == "2":
                units_str = "kilometers"
                conversion_factor = 1.60934
            else:
                print("Invalid unit selection. Please choose 1 or 2.")
            for dest in destinations:
                url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
                print("URL: " + url)
                json_data = requests.get(url).json()
                json_status = json_data["info"]["statuscode"]
                if json_status == 0:
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
                    print(Fore.GREEN + "You have arrived at your destination." + Style.RESET_ALL)
                    print("=" * 50)
                elif json_status == 402:
                    print(Fore.RED + "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations." + Style.RESET_ALL)
                    print("=" * 50)
                elif json_status == 611:
                    print(Fore.RED + "Status Code: " + str(json_status) + "; Missing an entry for one or both locations." + Style.RESET_ALL)
                    print("=" * 50)
                else:
                    print(Fore.RED + "For Status Code: " + str(json_status) + "; Refer to:")
                    print("https://developer.mapquest.com/documentation/directions-api/status-codes")
                    print("=" * 50)
