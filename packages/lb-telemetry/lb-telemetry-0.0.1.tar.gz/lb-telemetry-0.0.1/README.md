# LHCb Package Usage Logger

A utility for logging usage data about LHCb packages to [MONIT](https://monit.web.cern.ch/).
Usage data graphs specific to each package can be viewed on the [MONIT Grafana](https://monit-grafana.cern.ch/d/Q78h6E-nz/home?orgId=46). 

The package is not user-callable. It is intended to be imported and called by other LHCb packages such as [PIDCalib2](https://gitlab.cern.ch/lhcb-rta/pidcalib2).

## Setup

### Installing from PyPI

The package is available on [PyPI](https://pypi.org/project/lhcb_package_usage_logger/).
It can be installed on any computer via `pip` by running (preferably in a [virtual environment](https://docs.python.org/3/library/venv.html)):
```sh
pip install lb_telemetry
```
