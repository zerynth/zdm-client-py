import adm
import click
import time


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
def test(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    print("Test scrti")
