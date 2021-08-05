# Discord bot by Bronko

## Setup

### Create bot account, generate token, invite to server
[How to create bot and generate its token?](https://discordpy.readthedocs.io/en/stable/discord.html)

### To use riot api features you have to obtain riot api key
[How to register product and get riot api key?](https://developer.riotgames.com/docs/portal)

### Install python and pip if it's not already installed

### Download the bot
```
git clone https://github.com/MBronko/discord_bot
cd discord_bot
```

### create .env file using .env.temp template and put previously generated token and key inside

### create virtual environment, activate it and install required modules
#### linux
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
#### windows
```
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

### finally run your bot
#### linux
```
python3 main.py           # with venv activated
                          # or
venv/bin/python3 main.py  # with venv deactivated
```
#### windows
```
python main.py                # with venv activated
                              # or
venv\Scripts\python main.py  # with venv deactivated
```

## Setup as Systemd service

Create SERVICE_NAME.service file in "/etc/systemd/system/" directory \
(you will later address the service by the filename used here)

Inside the file put following configuration
```
[Unit]
Description=My Discord Bot
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
WorkingDirectory=BOT_DIRECTORY
ExecStart=BOT_DIRECTORY/venv/bin/python3 BOT_DIRECTORY/main.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
replace BOT_DIRECTORY with absolute path to your bot  
i.e. /home/bronko/discord_bot

then run command\
```sudo systemctl daemon-reload```


finally you can use following commands
```
sudo systemctl status SERVICE_NAME
sudo systemctl enable SERVICE_NAME
sudo systemctl disable SERVICE_NAME
sudo systemctl start SERVICE_NAME
sudo systemctl stop SERVICE_NAME
```
