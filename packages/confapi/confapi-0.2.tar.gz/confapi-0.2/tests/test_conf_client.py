# pylint: disable-all

import pytest
from tests.conf import conf

from confclient import ConfClient
from confclient.confexcept import BadRPCRequestException, BadRestRequestException


@pytest.fixture
def conf_client():
    return ConfClient(conf["url"], conf["username"], conf["password"])


def test_rpc_add_user_good(conf_client: ConfClient):

    resp = conf_client.add_user("test_user_123", "Test User", "test@testuser.com")

    assert resp.status_code == 200


def test_rpc_add_user_bad(conf_client: ConfClient):

    with pytest.raises(BadRPCRequestException):
        resp = conf_client.add_user("test_user_123", "Test User", "test@testuser.com")


def test_rpc_remove_user_good(conf_client: ConfClient):

    resp = conf_client.remove_user("test_user_123")

    assert resp.status_code == 200


def test_rpc_remove_user_bad(conf_client: ConfClient):

    with pytest.raises(BadRPCRequestException):
        resp = conf_client.remove_user("test_user_12")


def test_rpc_create_group_good(conf_client: ConfClient):

    conf_client.add_group("test_group_123")

    groups = [g["groupname"] for g in conf_client.get_groups()["groups"]]

    assert "test_group_123" in groups


# TODO: Figure out how to determine if a create group fails, response doesn't seem to differ
# def test_rpc_create_group_bad(conf_client: ConfClient):

#     with pytest.raises(BadRPCRequestException):
#         resp = conf_client.add_group("test_group_123")


def test_rpc_remove_group_good(conf_client: ConfClient):

    conf_client.remove_group("test_group_123")

    groups = [g["groupname"] for g in conf_client.get_groups()["groups"]]

    assert "test_group_123" not in groups


# TODO: Figure out how to determine if a delete group fails, response doesn't seem to differ
# def test_rpc_remove_group_bad(conf_client: ConfClient, rest_client: RestClient):

#     conf_client.remove_group("test_group_123")

#     groups = [g["groupname"] for g in rest_client.get_groups()["groups"]]

#     assert "test_group_123" not in groups


def test_rpc_add_user_to_group(conf_client: ConfClient):

    conf_client.add_user("test_user_123", "Test User", "test@testuser.com")

    conf_client.add_group("test_group_123")

    conf_client.add_user_to_group("test_user_123", "test_group_123")

    resp = conf_client.get_users_in_group("test_group_123")

    assert "test_user_123" in [u["username"] for u in resp["users"]]


def test_rpc_remove_user_from_group(conf_client: ConfClient):

    conf_client.remove_user_from_group("test_user_123", "test_group_123")

    resp = conf_client.get_users_in_group("test_group_123")

    assert "test_user_123" not in [u["username"] for u in resp["users"]]

    # Clean up
    conf_client.remove_user("test_user_123")
    conf_client.remove_group("test_group_123")


def test_get_all_users(conf_client: ConfClient):

    resp = conf_client.get_all_users(13, 0)

    assert len(resp["users"]) == 13

    resp = conf_client.get_all_users(17, 0)

    assert len(resp["users"]) == 17


def test_bad_auth():

    bad_client = ConfClient(conf["url"], "baduser", "badpassword")

    with pytest.raises(BadRestRequestException):
        bad_client.get_all_users(17, 2)

