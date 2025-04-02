# ports-game
Implementation of the popular scout game "Ports". The official ruleset of the original game is available [here](https://www.hranostaj.cz/hra3691) and on the website itself under the "Manual" section.

## Installation
Clone the repository with your preferred protocol.

**SSH**:

```bash
git clone git@github.com:lukakralik/ports-game.git
cd ports-game/ports
```

**HTTPS**:
```bash
git clone https://github.com/lukakralik/ports-game.git
cd ports-game/ports
```


### Local
#### Environment
**Creating a fresh virtual environment with your preferred manager is highly advised! See [venv](https://docs.python.org/3/library/venv.html).**

Once the environmetn is set up, install all required dependencies with:


```bash
pip install -r requirements.txt
```

#### Start the application 
```bash
export FLASK_APP=main.py
flask run
```

The application is now running locally at ```http://127.0.0.1``` on port ```5000```.

### Dockerized
**Only proceed with this option you have docker set up on your sytsem!**

#### Build
```bash
docker build -t ports . 
```

#### Run 
```bash
docker run -p 5000:5000 ports
```

You can choose an arbitrary free port, 5000 is recommended for development.

## Development guide
A cloned repository is already assumed, execution can be done both locally and dockerized. For compatibility reasons the dockerzied approach is preferred.

### Contributing
If you encounter a problem, feel free to open an issue or try to tackle it yourself and propose a pull request. In both cases please describe the problem you encountered, your environment setup (if it somehow deviates from the 2 recommended options), what did you attempt to do and what was the expected result. Thanks!

### Codebase setup
This service is a full-stack Flask application, thus it follows some common organization choices. All further mentioned direcories are located under ```ports/```

The directory ```migrations``` serves as a utility for ```sqlalchemy``` SQLite database migrations.


The rest of the application is fully contained within the ```src``` directory.

### Front-end
#### ```templates```
All [Jinja](https://jinja.palletsprojects.com/en/stable/) template files are located here. These files typically serve a single page withing the application, they either use a ```flask-form`` form or vanilla HTML structures.

##### ```templates/base.html```
All ```.html``` files within the project extend this base setup. It displays the top bar, options, remaining time and the logic for the game timer. The moment the game timer reaches 0 seconds, "game over" is displayed over any page inheriting from this base.

##### ```templates/admin```
Pages specifically accessed during game setup and general administration are located here.
##### ```templates/errors```
Predefined error pages for errors are located here. Covered HTTP error codes are:

- 404 Page Not Found
- 500 Internal Server Error

### Back-end

#### ```main.py```
The entry point of the application, which also serves a shell preprocessor which allows for easier acces to the DB from your shell.
#### ```__init__.py```
App startup. The application, database and logging is envoked here.
#### ```forms.py```
Forms in the ```flask-form``` format which can be accessed on given template pages.
#### ```models.py```
ORM definitions for the SQLite database.

Make sure to manage the migrations correctly once you edit the table structure:

```bash
flask db migrate -m "<message>"
```

```bash
flask db upgrade
```
#### ```routes.py```
Routing specification for template file rendering and REST API backend. So far this is a weaker point and requires further attention. Rendering routes return a specific template file at the end. 

REST API backend serves transaction operations, game timer actions and port/crew initialization/deletion.
#### ```utils.py```
Various utility functions used from ```routes.py```.
#### ```config.py```
Configuration setup used by the app. **NOT PRODUCTION READY, MAKE SURE TO SET UP A SECRET KEY FOR YOUR DATABASE**. It serves only for demo purposes.
#### ```tests.py```
So far the application doesn't have any unit test testcases. If you intend to develop a feature it is advised to first write the testcases here and state a clear purpose of the feature.
