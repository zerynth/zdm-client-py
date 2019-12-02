import adm
import click
import time
import json

@click.group()
def main():
    """CLI of the ADM SDK."""
    click.echo('Hello from ADM dev!')

@main.command()
@click.option('--device-id', default="dev01", help='Device ID')
@click.option('--mqtt-hostname', default='rmq.zerinth.com', help='Mqqt hostname')
@click.option('--mqtt-port', default=1883, help='Mqqt port')
@click.option('--mqtt-user', default='mqtt', help='Mqqt user')
@click.option('--mqtt-password', default='mqtt', help='Mqqt password')
@click.option('--count', default=1000, help='Number of messages to publish')
@click.argument('message')
def publish(device_id, mqtt_hostname, mqtt_port, mqtt_user, mqtt_password, count, message):
    """Simple program that create a device and publish 1000 messages into the Mqtt broker"""
    device = adm.Device(device_id, hostname=mqtt_hostname, port=mqtt_port, user=mqtt_user, password=mqtt_password)
    device.connect()

    # Publish message into the topic "data/<devid>"
    for x in range (count):
        time.sleep(2)
        payload = {"msg": message, "num":x}
        device.publish_data(payload)

@main.command()
@click.option('--rpc-url', default='http://127.0.0.1:7777', help='Endpoint of the RPC Service')
@click.argument('method')
@click.argument('params')
@click.argument('device')
def rpc(rpc_url, method, params, device):
    """Send an RPC to a device"""
    client = adm.ADMClient(rpc_url=rpc_url)
    rpc = {'method': method, 'parameters': params, "devices":[device]}
    client.send_rpc(payload=rpc)