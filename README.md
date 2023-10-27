# iflask-gps-sim

this package is used to simulate moving and iphone by using Apple's gps simulation tool

## Setup 

download project 
```
git clone https://github.com/ericjohnson97/iflask-gps-sim.git
```

change directory to project 
```
cd iflask-gps-sim/
```

install dependencies
```
pip3 install -r requirements.txt
```

## Run Application

mount developer image
```
python3 -m pymobiledevice3 mounter mount-developer 16.6/DeveloperDiskImage.dmg 16.6/DeveloperDiskImage.dmg
```


```
python3 app.py
```

## Using the Application

got to http://localhost:5000/
