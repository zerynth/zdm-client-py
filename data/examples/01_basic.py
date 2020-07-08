"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import random
import time
import zdm

device_id = 'device_id'
password = 'password'

device_id = 'dev-51pqc7kv35z7'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTFwcWM3a3YzNXo3IiwidXNlciI6ImRldi01MXBxYzdrdjM1ejciLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.QAH2SEmiZyIRh4TuDeKzqlYk4NG9_7qddWM8wrFbHJI'

device_id = 'dev-51pz39f7j7k3'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNDk1OTg4NiwiaWF0IjoxNTkzNDIzODg2LCJzdWIiOiJkZXYtNTFwejM5ZjdqN2szIn0.76gpV7U_RXqEY9t_41izG2TaixEvW_RrVVy7HAm6BWA'

device_id = 'dev-50mddnjtossz'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTBtZGRuanRvc3N6IiwidXNlciI6ImRldi01MG1kZG5qdG9zc3oiLCJrZXkiOjMsImV4cCI6MjUxNjIzOTAyMn0.BY-gx9pUbiy9sAW4luJ9eDC516J0n2UQmSK49FmsMLA'

device_id = "dev-521ite43a2v9"
password = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZXYtNTIxaXRlNDNhMnY5IiwiZXhwIjoxNTk2MzgxNjgyLCJrZXkiOjEsInVzZXIiOiJkZXYtNTIxaXRlNDNhMnY5In0.0dDfn335gk7C2tq_ZFE_yW2z7cFPXFxhc-bayY4EocY"
device_id = 'dev-5216sexaivwm'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTMyNjAyMiwiaWF0IjoxNTkzNzkwMDIyLCJzdWIiOiJkZXYtNTIxNnNleGFpdndtIn0.AN_qoPDwcP7HkhnbrzccV5htqyoRXzh_T-96jv6cgJY'
device_id = 'dev-5254v7dehgl8'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNTI1NHY3ZGVoZ2w4IiwidXNlciI6ImRldi01MjU0djdkZWhnbDgiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.IFWAMVk-c3oI0Sl6lO-jREidtLk9g90HtVMCUhpki8s'

device_id = 'dev-52i83w2lk16r'
password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOjEsImV4cCI6MTYyNTY0MzY3MiwiaWF0IjoxNTk0MTA3NjcyLCJzdWIiOiJkZXYtNTJpODN3MmxrMTZyIn0.bo-ZxObPnrpV4fnU9z74gJ6T0fUkTCpf7SoFlhnRgUA'

def pub_random():
    # this function is called periodically to publish to ZDM random int value labeled with tags values
    print('------ publish random ------')
    tags = ['tag1', 'tag2', 'tag3']

    for t in tags:
        value = random.randint(0, 20)
        payload = {
            'value': value
        }
        # publish payload to ZDM
        device.publish_data(t, payload)
        print('published on tag:', t, ':', payload)

    print('pub_random done')


def pub_temp_pressure():
    # this function publish another payload with two random int values
    print('---- publish temp_pressure ----')
    tag = 'tag4'
    temp = random.randint(19, 23)
    pressure = random.randint(50, 60)
    payload = {'temp': temp, 'pressure': pressure}
    device.publish_data(tag, payload)
    print('published on tag: ', tag, ':', payload)


device = zdm.ZDMClient(device_id=device_id,  endpoint="rmq.localhost")
device.set_password(password)
device.connect()


while True:
    time.sleep(2)
    pub_random()
    pub_temp_pressure()
