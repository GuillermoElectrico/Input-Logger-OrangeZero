# Input-Logger-OrangeZero
Log inputs status on a Orange Pi zero and plot graphs of your data.
Its been verified to work with a orange pi zero with simple 8 inputs module (coming soon PCB). By changing the inputspins.yml file and making a corresponding GPIO inputs relation.

### Requirements

#### Hardware

* Orange Pi Zero
* 8 inputs module (coming soon PCB) or other module DIY

#### Software

* Armbian
* Python 3.4 and PIP3
* [OPi.GPIO](https://pypi.org/project/OPi.GPIO/)
* [InfluxDB](https://docs.influxdata.com/influxdb/v1.3/)
* [Grafana](http://docs.grafana.org/)

### Prerequisite

### Installation
#### Install InfluxDB*

##### Step-by-step instructions
* Add the InfluxData repository
    ```sh
    $ curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    $ source /etc/os-release
    $ test $VERSION_ID = "9" && echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    ```
* Download and install
    ```sh
    $ sudo apt-get update && sudo apt-get install influxdb
    ```
* Start the influxdb service
    ```sh
    $ sudo service influxdb start
    ```
* Create the database
    ```sh
    $ influx
    CREATE DATABASE db_inputs
    exit 
    ```
[*source](https://docs.influxdata.com/influxdb/v1.3/introduction/installation/)

#### Install Grafana*

##### Step-by-step instructions
* Add APT Repository
    ```sh
    $ echo "deb https://dl.bintray.com/fg2it/deb-rpi-1b jessie main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
    ```
* Add Bintray key
    ```sh
    $ curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
    ```
* Now install
    ```sh
    $ sudo apt-get update && sudo apt-get install grafana 
    ```
* Start the service using systemd:
    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl start grafana-server
    $ systemctl status grafana-server
    ```
* Enable the systemd service so that Grafana starts at boot.
    ```sh
    $ sudo systemctl enable grafana-server.service
    ```
* Go to http://localhost:3000 and login using admin / admin (remember to change password)
[*source](http://docs.grafana.org/installation/debian/)

#### Install Input-Logger-OrangeZero:
* Download and install from Github and install pip3
    ```sh
    $ git clone https://github.com/GuillermoElectrico/Input-Logger-OrangeZero.git
	$ sudo apt-get install python3-pip
    ```
* Run setup script (must be executed as root (sudo) if the application needs to be started from rc.local, see below)
    ```sh
    $ cd Input-Logger-OrangeZero
    $ sudo python3 setup.py install
    ```    
* Make script file executable
    ```sh
    $ chmod 777 read_input_orangezero.py
    ```
* Edit inputs.yml to match your configuration
* Test the configuration by running:
    ```sh
    ./read_input_orangezero.py
    ./read_input_orangezero.py --help # Shows you all available parameters
    ```
* To run the python script at system startup. Add to following lines to the end of /etc/rc.local but before exit:
    ```sh
    # Start Energy Meter Logger
    /home/pi/energy-meter-logger/read_input_orangezero.py > /var/log/inputs-logger.log &
    ```
    Log with potential errors are found in /var/log/inputs-logger.log
