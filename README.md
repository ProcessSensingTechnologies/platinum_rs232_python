# Platinum RS232 Python


See `Platinum Sensor User Manual TDS129` for techical details of the sensor.
See `Premier Sensor Communications protocol TDS0045` for further details on communication with Premier/Platinum sensors.

This repository provides Python code for receiving data from the from a Dynament platinum/premier sensor.

## Getting Started

### Prerequisites

- Python 3.11 or newer (https://www.python.org/downloads/)
    - Older Python revisions are untested but may work.
- Package for Serial communication in Python:
    - Recommended: PySerial
- Suitable connection to Platinum Sensor
    - Recommended: PST Dev kit - Platinum

### Installation

#### Clone this repository:

```bash
git clone https://github.com/ProcessSensingTechnologies/platinum_rs232_python.git
```

#### Install dependencies:

*It is highly recommended to use a virtual environment to isolate your project's dependencies and avoid conflicts with other Python projects.*
```Bash
cd platinum_rs232_python

python -m pip install -r requirements.txt
```
## Usage

- An example can be found in `example_1.py` where the sensor reading and current sensor temperature is returned.

## Additional Notes

- **Supplied code currently only reads "Live Data" from sensors using Version 4 of the live data structure**

## Contributing

Please feel free to open issues for support or to suggest changes.

## License

This repository is licensed under the BSD 3-Clause License. See the LICENSE file for details.
