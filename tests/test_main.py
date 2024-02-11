from rpc_client import JsonRpcClient
import time


def test_player_can_take_key(client: JsonRpcClient, load_scene):
    position = client.GetObjectCoordinates(objectName='Key')

    key_count = client.GetItemCount(itemName='key')
    client.TeleportPlayer(**position)
    time.sleep(0.5)
    new_key_count = client.GetItemCount(itemName='key')

    assert key_count != new_key_count


def test_player_can_open_door(client: JsonRpcClient, load_scene):
    key_position = client.GetObjectCoordinates(objectName='Key')
    client.TeleportPlayer(**key_position)
    time.sleep(0.5)
    
    door_position = client.GetObjectCoordinates(objectName='Door')
    client.TeleportPlayer(**door_position)
    time.sleep(0.5)
    assert not client.IsObjectPresent(objectName='Door')
