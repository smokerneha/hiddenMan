import os

from Parser import Parser
import asyncio
from assist_func import add_to_existing_file, convert_to_csv
from account_manager import auth_for_parsing


from colorama import Fore, Style
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
ascii_art = [
    f"{Fore.RED}.____       {Fore.YELLOW}_____  {Fore.GREEN}_______________.___. {Fore.CYAN}________  {Fore.MAGENTA}_______________   {Fore.BLUE}____",
    f"{Fore.RED}|    |     {Fore.YELLOW}/  _  \\ {Fore.GREEN}\\____    /\\__  |   | {Fore.CYAN}\\______ \\ {Fore.MAGENTA}\\_   _____/\\   \\ {Fore.BLUE}/   /",
    f"{Fore.RED}|    |    {Fore.YELLOW}/  /_\\  \\ {Fore.GREEN} /     /  /   |   | {Fore.CYAN} |    |  \\ {Fore.MAGENTA}|    __)_  \\   Y   {Fore.BLUE}/",
    f"{Fore.RED}|    |___{Fore.YELLOW}/    |    \\{Fore.GREEN}/     /_  \\____   | {Fore.CYAN} |    `   \\{Fore.MAGENTA}|        \\  \\     {Fore.BLUE}/",
    f"{Fore.RED}|_______ \\{Fore.YELLOW}____|__  / {Fore.GREEN}_______ \\ / ______| {Fore.CYAN}/_______  /{Fore.MAGENTA}_______  /   \\___/ ",
    f"{Fore.RED}        \\/{Fore.YELLOW}       \\/  {Fore.GREEN}       \\/ \\/        {Fore.CYAN}        \\/ {Fore.MAGENTA}       \\/           {Style.RESET_ALL}"
]

def what_to_do():
    clear_screen()
    for line in ascii_art:
        print(line)
    parser_menu = input (f"{Fore.YELLOW}Choose how to scrape users:{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}1.{Style.RESET_ALL} Scrape users only with status {Fore.GREEN}Last seen Recently{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}2.{Style.RESET_ALL} Parse {Fore.MAGENTA}without any filter{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}3.{Style.RESET_ALL} Scrape users {Fore.BLUE}from comments in the channel{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}4.{Style.RESET_ALL} Scrape users, who were {Fore.RED}online later than a certain date{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}5.{Style.RESET_ALL} Scrape users, who reacted {Fore.YELLOW}in the group {Fore.WHITE}(by specific emoji or with any emoji){Style.RESET_ALL}\n"
                         f"{Fore.CYAN}6.{Style.RESET_ALL} Scrape users, who were {Fore.GREEN}online later than a certain date n time{Style.RESET_ALL}\n"
                         f"{Fore.CYAN}7.{Style.RESET_ALL} {Fore.RED}Quit{Style.RESET_ALL}\n - ")

    while parser_menu not in '1234567':
        parser_menu = input (f"{Fore.YELLOW}Choose how to scrape users:{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}1.{Style.RESET_ALL} Scrape users only with status {Fore.GREEN}Last seen Recently{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}2.{Style.RESET_ALL} Parse {Fore.MAGENTA}without any filter{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}3.{Style.RESET_ALL} Scrape users {Fore.BLUE}from comments in the channel{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}4.{Style.RESET_ALL} Scrape users, who were {Fore.RED}online later than a certain date{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}5.{Style.RESET_ALL} Scrape users, who reacted {Fore.YELLOW}in the group {Fore.WHITE}(by specific emoji or with any emoji){Style.RESET_ALL}\n"
                             f"{Fore.CYAN}6.{Style.RESET_ALL} Scrape users, who were {Fore.GREEN}online later than a certain date n time{Style.RESET_ALL}\n"
                             f"{Fore.CYAN}7.{Style.RESET_ALL} {Fore.RED}Quit{Style.RESET_ALL}\n - ")

    return int(parser_menu)



async def extended_parser():
    client = await auth_for_parsing ()
    if client is None:
        return
    if not os.path.exists ('users.csv'):
        open ('users.csv', 'w')
    option = what_to_do()
    if option == 1:
        await parser(client)
    elif option == 2:
        await parser(client, without_filter=True)
    elif option == 3:
        # parse from channel worked
        users = await Parser(client).get_from_comments()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 4:
        # parse by specific date
        limit = input ('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
        if limit.isdigit ():
            limit = int (limit)
            users = await Parser (client).users_by_day_filter (limit=limit)
        else:
            users = await Parser (client).users_by_day_filter ()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 5:
        # get users that reacted in chat
        users = await Parser(client).get_user_that_reacted_in_chat()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 6:
        users = await Parser (client).users_by_time_filter ()
        if users:
            add_to_existing_file (users)
            print ('successfully parsed')
    elif option == 7:
        return


# fully functional old parser

async def parser(client, without_filter=None):
    limit = input('How many users do u want to parse? Press enter if all (tg limit is 10000 from one group): ')
    if limit.isdigit():
        limit = int(limit)
        if without_filter:
            users = await Parser (client).parse_members (limit=limit, status_filter=None)
        else:
            users = await Parser (client).parse_members (limit=limit)
    else:
        if without_filter:
            users = await Parser(client).parse_members(status_filter=None)
        else:
            users = await Parser(client).parse_members()

    add_to_existing_file(users)
    print('successfully parsed')


asyncio.run(extended_parser())
