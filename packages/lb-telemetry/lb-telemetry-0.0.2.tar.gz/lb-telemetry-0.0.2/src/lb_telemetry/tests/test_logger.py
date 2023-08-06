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

import requests

from src.lb_telemetry import logger

TEST_PRODUCER = "pid_calib2_logger"
TEST_CONFIG = {
    "sample": "TEST",
    "magnet": "up",
    "particle": "e",
    "pid_cuts": "[]",
    "cuts": "[]",
    "max_files": 0,
    "bin_vars": "[]",
    "args": "{}",
    "exec_time": -1,
}
TEST_TAGS = ["sample", "magnet", "particle"]


def test_build_payload():
    payload: dict = logger.build_payload(
        producer=TEST_PRODUCER,
        data=TEST_CONFIG,
        tags=TEST_TAGS,
    )

    # Ensure payload has mandatory fields
    assert "producer" in payload.keys()
    assert "type" in payload.keys()
    assert "idb_tags" in payload.keys()

    # Ensure that all tags declared appear in the payload
    for tag in payload["idb_tags"]:
        assert tag in payload.keys()

    # Ensure value types are compatible with InfluxDB
    for value in TEST_CONFIG.values():
        assert type(value) in logger.INFLUXDB_LEGAL_TYPES


def can_fetch_test_log(ts: int) -> bool:
    database = f"monit_production_\\{TEST_PRODUCER}"

    try:
        response = requests.post(
            f"https://monit-grafana.cern.ch/api/datasources/proxy/{logger.DATA_SOURCE_ID}/query?db={database}",
            headers={
                "Authorization": f"Bearer {logger.GRAFANA_TOKEN}",
            },
            verify=False,
        )

        if response.status_code != 200:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        # TODO: 16/06/2023 Find out what the response looks when our test log is successfully fetched
        return "NOT IMPLEMENTED" in response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while verifying the test log")
        print(e)
        return False


def test_log_to_monit():
    # TODO: 19/06/2023 Test all producers?
    ts: int = logger.log_to_monit(TEST_PRODUCER, TEST_CONFIG, TEST_TAGS)

    # Check if the test log can be fetched
    assert ts != -1
    assert can_fetch_test_log(ts)
