###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import json
import time

import requests

PRODUCER = "lb-telemetry"
MONIT_URL = "http://monit-metrics.cern.ch:10012/"
DATA_SOURCE_ID = "xH1aekXVz"
GRAFANA_TOKEN = "eyJrIjoicjlmU0VLT1FzanBzNklkWUowUVpBNXE3bUdjNlhMbWEiLCJuIjoiTW9uaXQiLCJpZCI6NDZ9"

INFLUXDB_LEGAL_TYPES = [bool, int, float, str]


def build_payload(package: str, data: dict, tags: list[str]) -> dict:
    """Builds a payload to be sent to MONIT.

    Args:
        package: The name of the calling package and ID for the table the data should be sent to.
        data: The data (tags and fields with their values) to be sent to MONIT.
        tags: Which data entries are tags (the rest are assumed to be fields).
    """
    for value in data.values():
        assert type(value) in INFLUXDB_LEGAL_TYPES

    payload = {
        "producer": PRODUCER,
        "type": package,
        "timestamp": int(time.time() * 1000),
        "idb_tags": tags,
    }

    return payload | data


def log_to_monit(package: str, data: dict, tags: list[str]) -> int:
    """Sends the provided data to MONIT.
    The logged data is accessible via MONIT Grafana.

    Args:
        package: The name of the calling package and ID for the database the data should be sent to.
        data: The data (tags and fields with their values) to be sent to MONIT.
        tags: Which data entries are tags (the rest are assumed to be fields).

    Returns:
        The timestamp of the created log entry.
    """
    payload = build_payload(package, data, tags)

    # Send the data to MONIT
    try:
        response = requests.post(
            MONIT_URL,
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            verify=False
        )
    except requests.exceptions.RequestException as e:
        print("An error occurred while logging telemetry:")
        print(e)
        raise

    if response.status_code != 200:
        print(f"Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"Payload: {json.dumps(payload)}")
        raise requests.exceptions.RequestException

    return payload["timestamp"]
