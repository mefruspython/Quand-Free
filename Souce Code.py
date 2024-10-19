import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import whois
import ipaddress
from ipwhois import IPWhois
import socket
import requests
import logging
import os
from urllib.parse import quote
import webbrowser
import json
#import exiftool
#from scapy.all import IP, ICMP, send
import time
import pystyle 
from pystyle import *
import os

COLOR_CODE = {
    "RESET": "\033[0m",
    "UNDERLINE": "\033[04m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "RED": "\033[31m",
    "CYAN": "\033[36m",
    "BOLD": "\033[01m",
    "PINK": "\033[95m",
    "URL_L": "\033[36m",
    "LI_G": "\033[92m",
    "F_CL": "\033[0m",
    "DARK": "\033[90m",
}
def get_phone_info(phone_number: str) -> str:
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return "Номер телефона недействителен."
        
        country = geocoder.description_for_number(parsed_number, "ru")
        operator = carrier.name_for_number(parsed_number, "ru")
        timezones = timezone.time_zones_for_number(parsed_number)
        number_type = "мобильный" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "стационарный"
        
        return  (f"QUAND FREE\n"
                f"Страна: {country}\n"
                f"Оператор: {operator}\n"
                f"Тип номера: {number_type}\n"
                f"Часовые пояса: {', '.join(timezones)}\n"
                f"Купите платную версию для расширеного поиска")
    except phonenumbers.phonenumberutil.NumberParseException:
        return "Неверный формат номера телефона. Пожалуйста, используйте международный формат."
def get_ip_from_domain(domain: str) -> str:
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        logging.error(f"Ошибка получения IP для домена {domain}: {e}")
        return None

def get_ip_info(ip: str) -> str:
    obj = IPWhois(ip)
    res = obj.lookup_rdap()
    network = res.get('network', {})
    asn_info = f"ASN: {res['asn']} ({res['asn_description']})" if res.get('asn') else "ASN: Не доступно"
    return (f"QUAND FREE\n"
            f"IP: {ip}\n"
            f"Страна: {network.get('country', 'Не доступно')}\n"
            f"Организация: {network.get('name', 'Не доступно')}\n"
            f"CIDR: {network.get('cidr', 'Не доступно')}\n"
            f"Дата начала: {network.get('start_address', 'Не доступно')}\n"
            f"Дата окончания: {network.get('end_address', 'Не доступно')}\n"
            f"{asn_info}")

def get_domain_ip_info(query: str) -> str:
    try:
        ipaddress.ip_address(query)
        return get_ip_info(query)
    except ValueError:
        try:
            ip = get_ip_from_domain(query)
            if ip:
                return get_ip_info(ip)
            else:
                return "Не удалось получить IP-адрес для данного домена."
        except Exception as e:
            logging.error(f"Ошибка при получении информации о домене {query}: {e}")
            return f"Ошибка при получении информации о домене: {e}"

logo = fr'''

                                                   .o8      .o88o.
                                                  "888      888 `"
 .ooooo oo oooo  oooo   .oooo.   ooo. .oo.    .oooo888     o888oo  oooo d8b  .ooooo.   .ooooo.
d88' `888  `888  `888  `P  )88b  `888P"Y88b  d88' `888      888    `888""8P d88' `88b d88' `88b
888   888   888   888   .oP"888   888   888  888   888      888     888     888ooo888 888ooo888
888   888   888   888  d8(  888   888   888  888   888      888     888     888    .o 888    .o
`V8bod888   `V88V"V8P' `Y888""8o o888o o888o `Y8bod88P"    o888o   d888b    `Y8bod8P' `Y8bod8P'
      888.
      8P'
      "


'''
menu =fr'''
                Free version
╔                                                ╗
  1. Поиск по номеру    | 3. Купить платную версию
  2. Поиск по ip        | 4. Скоро      
╚                                                ╝
'''

buypremlogo =fr'''

  ,---,                                   ,----.                                                    ,---,
,---.'|             ,--,                 /   /  \-.          ,--,                      ,---,      ,---.'|
|   | :           ,'_ /|                |   :    :|        ,'_ /|                  ,-+-. /  |     |   | :
:   : :      .--. |  | :        .--,    |   | .\  .   .--. |  | :     ,--.--.     ,--.'|'   |     |   | |
:     |,-. ,'_ /| :  . |      /_ ./|    .   ; |:  | ,'_ /| :  . |    /       \   |   |  ,"' |   ,--.__| |
|   : '  | |  ' | |  . .   , ' , ' :    '   .  \  | |  ' | |  . .   .--.  .-. |  |   | /  | |  /   ,'   |
|   |  / : |  | ' |  | |  /___/ \: |     \   `.   | |  | ' |  | |    \__\/: . .  |   | |  | | .   '  /  |
'   : |: | :  | : ;  ; |   .  \  ' |      `--'""| | :  | : ;  ; |    ," .--.; |  |   | |  |/  '   ; |:  |
|   | '/ : '  :  `--'   \   \  ;   :        |   | | '  :  `--'   \  /  /  ,.  |  |   | |--'   |   | '/  '
|   :    | :  ,      .-./    \  \  ;        |   | : :  ,      .-./ ;  :   .'   \ |   |/       |   :    :|
/    \  /   `--`----'         :  \  \       `---'.|  `--`----'     |  ,     .-./ '---'         \   \  /
`-'----'                       \  ' ;         `---`                 `--`---'                    `----'
                                `--`                 
'''
buyprem = '''
 Купить можно у создателя:
 Discord: 1_month_1
 Telegram: @TRUE_CBATEP

 quand NextGen - 299 Руб
 quand Premium - 499 Руб

 Вес базы данных
 NextGen: 489 GB
 Premium: 1.5 TRB

'''
soon =fr'''
                ,---.      ,---.         ,---,
  .--.--.      '   ,'\    '   ,'\    ,-+-. /  |
 /  /    '    /   /   |  /   /   |  ,--.'|'   |
|  :  /`./   .   ; ,. : .   ; ,. : |   |  ,"' |
|  :  ;_     '   | |: : '   | |: : |   | /  | |
 \  \    `.  '   | .; : '   | .; : |   | |  | |
  `----.   \ |   :    | |   :    | |   | |  |/
 /  /`--'  /  \   \  /   \   \  /  |   | |--'
'--'.     /    `----'     `----'   |   |/
  `--'---'                         '---'

Скоро чтото добавиться об этом мы сообщим в Telegram @QUAND_CBAT
Там еще продаем другие софты!
'''
grad_menu = Colorate.Horizontal(Colors.white_to_green, Center.XCenter(menu))
grad_banner = Colorate.Horizontal(Colors.white_to_green, Center.XCenter(logo))
grad_buyprem = Colorate.Horizontal(Colors.white_to_green, Center.XCenter(buyprem))
grad_buypremlogo = Colorate.Horizontal(Colors.white_to_green, Center.XCenter(buypremlogo))
grad_soon = Colorate.Horizontal(Colors.white_to_green, Center.XCenter(soon))
os.system('cls' if os.name == 'nt' else 'clear')
print(grad_banner)
time.sleep(1)
print(grad_menu)
option = int(input('Введите:  '))
if option == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            phone_number = input("Введите номер телефона в международном формате (например, +79876543210): ")
            info = get_phone_info(phone_number)
            print(info)
            input('')
            
elif option == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            query = input("Введите домен или IP-адрес: ")
            info = get_domain_ip_info(query)
            print(info)
            input()
            (option)
elif option == 3:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(grad_buypremlogo)
    print(grad_buyprem)
    input()
    (option)
elif option == 4:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(grad_soon)
    input()
    (option)
