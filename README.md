# create-discord-bot - CLI to setup functional discord bot environment

The create-discord-bot CLI tool allows you to quickly create a discord bot from stratch with a predefined project
structure. You can also quickly create new Cogs, uncategorised commands or dockerise the entire bot.

The bot project has the following features upon creation:
- Logging enabled with custom logger support via config file
- Log all discordpy related information into a file
- Log all other logs to console during development
- Create discordpy Cogs 
- Default Admin Cog enabled with the functionality to:
    - Unload Cogs
    - Load Cogs
    - Reload Cogs
    - Set Bot presence
- Create commands, which are uncategorised
- automatically load Cogs and Commands from files
- possible disabling of Cogs and Command loading
- pre-created unittest files (no unittest framework enforced!)
- switch between MVC structure and bare Cog setup
- DEBUG switch for development
- Multiple .env file support
- Dockerfile and docker-compose creation for both development and production
- predefined .gitignore for python development and for ignoring irrelevant files in project
- fully documented

The intention is to quickly setup a new discord bot project. You do not need to dockerise the bot to run it.
Since every line is documented it should be straightforward to change/add/remove behaviour to your preferences. 


The project uses ```discordpy``` for the actual bot development. It also uses ```PyYaml``` to ```safe_load``` 
the ```logger.yml``` file. And lastly it uses ```python-dotenv``` to load the debug/development ```.env``` file, when
not using docker during development.

By default voice support for ```discordpy``` is not in the requirements.txt. You need to install it as described in 
the official documentation. This is only required, if you want your bot to use voice in voice channels, i.e. playing music.


# Installation

Install the package globally
```
pip install creatediscordbot
```

Install the package in a virtual environment
```
virtualenv .venv
. .venv/bin/activate
pip install creatediscordbot
```

## Instructions to setup demo project
1. Create a new project folder
2. Create a virtual environment folder in there (highly recommended!)
3. run ```create-discord-bot createbot animals``` to create a new discord bot folder named ```animals```
Replace ```animals``` with your actual bot name

4. Check that the following folder & file structure has been created successfully:
```
├── animals
│   ├── cogs
│   │   ├── __init__.py
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── controller.py
│   │   │   ├── converter.py
│   │   │   ├── model.py
│   │   │   └── tests
│   │   │       ├── __init__.py
│   │   │       ├── test_controller.py
│   │   │       ├── test_converter.py
│   │   │       └── test_model.py
│   │   └── animals
│   │       ├── __init__.py
│   │       ├── animals.py
│   │       ├── controller.py
│   │       ├── converter.py
│   │       ├── model.py
│   │       └── tests
│   │           ├── __init__.py
│   │           ├── test_controller.py
│   │           ├── test_converter.py
│   │           └── test_model.py
│   ├── logger.yml
│   ├── main.py
│   ├── requirements.txt
│   ├── settings.py
│   ├── settings_files
│   │   ├── __init__.py 
│   │   ├── _global.py
│   │   ├── development.py
│   │   └── production.py
│   └── uncategorised_commands
│       ├── __init__.py
│       └── loader.py
├── logs
└── .creatediscordbot.conf
```

5.Create a ```.env.debug``` file in the botfolder ```animals``` and paste the following code in:
```
DISCORD_BOT_TOKEN=


DB_HOST_NAME=
DB_DATABASE_NAME=
DB_USER=
DB_PASSWORD=
```

(*Note: for production just call the file ```.env``` - Both are specified in .gitignore and 
will not be committed to the repository you are using*)

6.Supply your Discord Bot Token to the ```.env.debug``` file via ```DISCORD_BOT_TOKEN=``` 

7.Install the requirements via pip:
```
pip install -r animals/requirements.txt
```

8.Run the following command: ```DEBUG=True python animals/main.py``` to start your bot


## Requirements:
```
python 3.6
```

# Usage

### Show Help
```
# --help also works
create-discord-bot -h 
```

### Create new bot
```
create-discord-bot createbot animals
```

Creates a new bot project with the project structure seen in the instructions section.

The discordpy bot will have the following requirements:
```
aiohttp==3.6.2
async-timeout==3.0.1
attrs==19.3.0
chardet==3.0.4
discord.py==1.3.3
idna==2.9
multidict==4.7.5
python-dotenv==0.13.0
websockets==8.1
yarl==1.4.2
PyYAML==5.3.1
```

You will find them in the requirements.txt that is generated with the project. You should then install them via pip:
```
pip install -r botfolder/requirements.txt
```

### Create new Cog
To create a new cog module for the bot you can use ```createcog <cogname>```. By default this creates a new Cog with 
a controller file, a model file, a converter file and a folder with ```tests``` for unittests.

If you do not want these you can supply the parameter ```--bare```.

If you want to overwrite the default behaviour to NOT create a full Cog structure open your ```.creatediscordbot.conf```
and set ```cog_bare_default=True```. This sets the ```--bare``` parameter as default
```
# --bare at the end prevents creation of unittests folder, controller/model and converter
create-discord-bot createcog cat
create-discord-bot createcog fish --bare
create-discord-bot createcog dog --tests
```

If you do not want to create the unittests in a full setup you can use ```--tests``` to prevent the creation of the test
folder.

If you want to overwrite the default behaviour to NOT unittests in a full Cog structure open your ```.creatediscordbot.conf```
and set ```cog_create_unittests_default=False```. This sets the ```--tests``` parameter as default


### Dockerise the deployment
```
create-discord-bot makedocker
```
If you want to deploy your bot via docker container than you can call ```makedocker```. This will create three files 
for you:
```
# In the Bot folder
- Dockerfile
# In the Project folder
- docker-compose.yml
- docker-compose-dev.yml
```

The ```Dockerfile``` in the bot folder uses ```python 3.8.2``` as a base image and copies your bot folder and installs 
the ```requirements.txt``` pip requirements.

To start the bot you can use ```docker-compose up --build``` for production, 
or ```docker-compose -f docker-compose-dev.yml up --build``` for development/testing. 

The docker-compose configuration files have the ```.env``` and ```.env.debug``` files set as their environment files. 

If there are already docker related files it will ask you, if you wanted to overwrite them.


# License
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007