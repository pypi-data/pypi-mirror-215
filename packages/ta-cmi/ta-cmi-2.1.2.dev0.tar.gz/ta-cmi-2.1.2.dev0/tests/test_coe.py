from unittest.mock import patch

import pytest

from ta_cmi import ChannelMode, ChannelType
from ta_cmi.coe import CoE
from ta_cmi.coe_api import CoEAPI
from ta_cmi.coe_channel import CoEChannel
from tests import (
    COE_DATA_PACKAGE,
    COE_SEND_ANALOG_PACKAGE,
    COE_SEND_DIGITAL_PACKAGE,
    COE_VERSION_PACKAGE,
)

TEST_HOST = "http://localhost"

DATA_RESPONSE = {
    "digital": [{"value": True, "unit": 43}],
    "analog": [{"value": 34.4, "unit": 1}],
    "last_update_unix": 1680410064.03764,
    "last_update": "2023-04-01T12:00:00",
}

DATA_RESPONSE_WITH_EMPTY_SLOTS = {
    "digital": [{"value": True, "unit": 43}, {"value": False, "unit": 0}],
    "analog": [{"value": 34.4, "unit": 1}, {"value": 0.0, "unit": 0}],
    "last_update_unix": 1680410064.03764,
    "last_update": "2023-04-01T12:00:00",
}


@pytest.mark.asyncio
async def test_update_no_data_received():
    """Test the update method with empty data."""
    coe = CoE(TEST_HOST)

    coe._channels = {}

    with patch(COE_DATA_PACKAGE, return_value=None) as data_mock:
        await coe.update()

        assert coe._channels == {}

        data_mock.assert_called_once()


@pytest.mark.asyncio
async def test_update_old_data_received():
    """Test the update method with old data."""
    coe = CoE(TEST_HOST)

    coe._channels = {ChannelType.INPUT: {}}
    coe.last_update = DATA_RESPONSE["last_update_unix"]

    with patch(COE_DATA_PACKAGE, return_value=DATA_RESPONSE) as data_mock:
        await coe.update()

        assert coe._channels == {ChannelType.INPUT: {}}

        data_mock.assert_called_once()


@pytest.mark.asyncio
async def test_update_data_received():
    """Test the update method with new data."""
    coe = CoE(TEST_HOST)

    assert coe._channels == {}
    assert coe.last_update == 0

    with patch(COE_DATA_PACKAGE, return_value=DATA_RESPONSE) as data_mock:
        await coe.update()

        assert coe._channels == {
            ChannelMode.DIGITAL: {1: CoEChannel(ChannelMode.DIGITAL, 1, 1, "43")},
            ChannelMode.ANALOG: {1: CoEChannel(ChannelMode.ANALOG, 1, 34.4, "1")},
        }

        assert coe.last_update == 1680410064.03764

        data_mock.assert_called_once()


@pytest.mark.asyncio
async def test_update_data_received_with_empty_slots():
    """Test the update method with new data with empty slots."""
    coe = CoE(TEST_HOST)

    assert coe._channels == {}

    with patch(
        COE_DATA_PACKAGE, return_value=DATA_RESPONSE_WITH_EMPTY_SLOTS
    ) as data_mock:
        await coe.update()

        assert coe._channels == {
            ChannelMode.DIGITAL: {1: CoEChannel(ChannelMode.DIGITAL, 1, 1, "43")},
            ChannelMode.ANALOG: {1: CoEChannel(ChannelMode.ANALOG, 1, 34.4, "1")},
        }

        data_mock.assert_called_once()


@pytest.mark.asyncio
async def test_get_server_version():
    """Test the test_get_server_version."""
    coe = CoE(TEST_HOST)

    version = "1.1.0"

    with patch(COE_VERSION_PACKAGE, return_value=version) as version_mock:
        result = await coe.get_server_version()

        assert result == version

        version_mock.assert_called_once()


@pytest.mark.asyncio
async def test_send_analog_values():
    """Test the send_analog_values."""
    coe = CoE(TEST_HOST)

    data = [CoEChannel(ChannelMode.ANALOG, 0, 1, "43")]
    page = 1

    with patch(COE_SEND_ANALOG_PACKAGE) as mock:
        await coe.send_analog_values(data, page)

        mock.assert_called_once_with(data, page)


@pytest.mark.asyncio
async def test_send_digital_values():
    """Test the send_digital_values."""
    coe = CoE(TEST_HOST)

    data = [CoEChannel(ChannelMode.DIGITAL, 0, 1, "")]
    page = False

    with patch(COE_SEND_DIGITAL_PACKAGE) as mock:
        await coe.send_digital_values(data, page)

        mock.assert_called_once_with(data, page)
