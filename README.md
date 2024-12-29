# ports-game
## About
Digital version of the scout game "The Ports".


### Port actions
Each initialized port can perform transactions involving initialized crews. In the future ports will offer a range of tasks and upgrades for crews' ships.
### Admin
Page ```/admin``` offers initialization of new ports and crews.

## Usage
### Local deployment
```bash
git clone https://github.com/lukakralik/ports-game.git
cd ports-game/ports
pip install -r requirements.txt --break-system-packages
EXPORT FLASK_APP=main.py
flask run
```

### Dockerized
```
docker build -t ports .
docker run -p 5000:5000 ports
```

## Roadmap
- [x] Admin page
- [x] Port and crew initialization
- [x] Transaction with sanitization
- [ ] Tasks
- [ ] Crew upgrades
- [ ] Loans
- [ ] Canons and pirates
- [ ] Live market evaluation
