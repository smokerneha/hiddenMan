
<h4 align="center">
👑 LAZY PREMIUM SCRAPPING TOOL 👑
</h4>


# Installation and usage on Windows
- Install python at least version 3.10 [how to install](https://www.digitalocean.com/community/tutorials/install-python-windows-10)
- Download the archive directly and unzip it or u can install git and download archive using git clone [install git](https://github.com/git-guides/install-git) (https://github.com/git-guides/install-git)

## Usage via terminal 
- Open terminal - click win + R and then type cmd.exe
- ```git clone https://github.com/lazydeveloperr/lazyscript``
- ```cd Tg_adder_with_proxy``` change directory to downloaded folder.
- ```exclude_list.txt``` - it'll open exclude_list.txt. If u want to filter users by first name run it and add words. Users with these words in first name will be excluded
- ```python account_manager.py```  -  To run account manager. Now u can add account(s) w or without proxy, delete account(s), change proxy for the specific account(s), view all accounts and test the ability to log in to account(s)
- ```python main_parser.py``` - To scrape members from the group
- ```python main_adder.py``` - Add scraped members to ur group


### Using session files for authorisation
- Delete examples of session + json files in session_dir folder 
- Add session + json files to the session_dir folder. U can add any number of accounts
- Run ```account_manager.py``` - click Add account - add account using session
- After adding accounts don't delete session + json files
- If u latter want to add more accounts just add more session + json files and again run ```account_manager.py``` ...

### Restriction feature
- When adding users to a group and one of the following errors occurs - PeerFloodError, UserBannedInChannelError, a note will be added to the account with current date n time
- After 3 days note will be automatically deleted. 
- U can manually delete this note in account_manager.py by clicking change restrictions
- When adding users to chats u can automatically skip an account if it have some restrictions

### Warm up feature
- To warm up, accounts will chat with each other in a group or/n dm
- Accounts will chat with each other using copied messages from the provided group and reactions
- At startup, u need to provide links to a chat from which accounts will copy messages and a chat in which accounts will chat among themself
- Not properly tested and may lead to a ban

#### Some examples of supported  MTProxies
ip: 170.187.188.55 port: 443 secret: eec210ca2aa6d3d81670ed32899925445b626c6f672e636c6f7564666c6172652e636f6d
ip: 46.149.73.29 port: 443 secret: ee1603010200010001fc030386e24c3add646e2e79656b74616e65742e636f6d646c2e676f6f676c652e636f6d666172616b61762e636f6d160301020001000100000000000000000000000000000000 

I am not responsible for the work of the public proxies above, at the time of the release, the proxies were working

#### Device model, system and app version for each account
If u want u may add device model, system and app version in system_model_app_versions.txt or even replace existing lines

