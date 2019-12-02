from aws.iot import iot
from toi.fourzeromanager import fzmfota
import json
import mcu
import vm
import fota

def cmd_jobs(obj, payload):
#-if DEBUG_FZM
    obj.FZprint("received a job")
#-endif
    try:
        jobid = payload["jobid"]
        status = payload["status"]
        #let's do the job
        if payload['job'] == "fota":
            if status == "pending":
                status, message = fzmfota.is_fota_possible(payload['payload'])
                obj.upd_job(jobid, status, message)
                sleep(2000)
                if status == "accepted":
                    obj.fota_ongoing = True
                    # if "mode" in payload and payload["mode"] == "running":
                    #     pass
                    # else:
                    # disconnect mqtt
                    obj.device.mqtt.disconnect()
                    obj.device.mqtt.close()
                    status, message = fzmfota.handle_fota(payload["payload"])
                    # obj.upd_job(jobid, status, message)
                    sleep(500)
                    mcu.reset()
            elif status == "accepted":
                status, message = fzmfota.is_fota_valid(payload['payload'])
                obj.upd_job(jobid, status, message)
                sleep(2000)
                status, message, reset_cause = fzmfota.finalize_fota(status)
                obj.upd_job(jobid, status, message)
                sleep(2000)
                mcu.reset()
            else:
                obj.upd_job(jobid,"rejected","job not allowed")
        else:
            pass
            # unexpected type
    except Exception as e:
        print(e)
#-if DEBUG_FZM
        obj.FZprint("cmd_jobs", e)
#-endif
fzp_cmd = {
    "jobs": cmd_jobs,
}
def rpc_reset_mcu(obj, *args):
    mcu.reset()
def rpc_list(obj, *args):
    return json.dumps({'res':[k for k in obj.rpc]})
def rpc_check_jobs(obj, *args):
    obj.check_job()
rpc_std = {
    "reseet_mcu": rpc_reset_mcu,
    "rpc_list": rpc_list,
    "check_jobs": rpc_check_jobs
}
new_exception(CloudInitError, Exception)
new_exception(CloudConfigError, Exception)
new_exception(CloudSubscriptionError, Exception)
new_exception(CloudConnectionError, Exception)
new_exception(CloudPublishError, Exception)

class FourZeroManager():
    def __init__(self, fzbox, endpoint=None, project=None, thingname=None, rpc=None):
        record = fota.get_record()
        vminfo = vm.info()
        print("FZM Status")
        print("===========")
        print("BC_SLOT    ", record[4],record[5])  #current, last working
        print("VM_SLOT    ", record[2],record[3])  #current, last working
        print("VM_UID     ", vminfo[0])
        print("===========")
        try:
            self.fzbox = fzbox
            if not endpoint or not project or not thingname:
                try:
                    endpoint, project, thingname = self._thing_data_load()
                except Exception as e:
                    print(e)
#-if DEBUG_FZM
                    self.FZprint(e)
#-endif
                    raise ValueError
            self.pub_topic = "/".join([project, thingname, "sink"]) //
            self.sub_topic = "/".join([project, thingname, "adm_in"]) 
            self.rpy_topic = "/".join([project, thingname, "adm_out"])
            self.endpoint = endpoint
            self.thingname = thingname
            self.rpc = rpc_std
            self.fota_ongoing = False
            if rpc:
                self.rpc.update(rpc)
            pkey, clicert = self._certificate_load()
            self.device = iot.Thing(self.endpoint, self.thingname, clicert, pkey, thingname=self.thingname)
#-if DEBUG_FZM
            self.FZprint("FourZeroManager init done")
#-endif
        except Exception as e:
#-if DEBUG_FZM
            self.FZprint("FourZeroManager exception,",e)
#-endif
            raise CloudInitError
#-if DEBUG_FZM
    def FZprint(self, *args):
        print(*args)
#-endif
    def _load_from_resource(self, mresource):
        mstream = open(mresource)
        barray = bytearray()
        while True:
            rd = mstream.read(1)
            if not rd:
                barray.append(0x0)
                break
            barray.append(rd[0])
        return barray
    def _thing_data_load(self):
        start_addr = 0x00352000
        tot_size = 4096
        tdata = self.fzbox.flash_load(start_addr, tot_size, rjson=True)
        project = tdata["sink"].split('/')[0]
        return tdata["endpoint"], project, tdata["thing"]
    def _load_from_flash(self):
        start_addr = 0x00350000
        tot_size = 4096
        return self.fzbox.flash_load(start_addr, tot_size)
    def _certificate_load(self):
        pkey = ''
        clicert = ''
#-if CERT_SOURCE
        new_resource('private.pem.key')
        new_resource('certificate.pem.crt')
        pkey = self._load_from_resource('resource://private.pem.key')
        clicert = self._load_from_resource('resource://certificate.pem.crt')
#-endif
#-if CERT_STORED
        from microchip.ateccx08a import ateccx08a
        ateccx08a.hwcrypto_init(I2C0, 0, i2c_addr=0x58, i2c_clock=self.fzbox.i2c_clk)
        clicert = self._load_from_flash()
#-endif
        return pkey, clicert
    def _config(self):
        try:
            self.device.mqtt.on(iot.mqtt.PUBLISH, self.handle_mqtt_msg)
            self.check_job()
            self.send_status()
        except Exception as e:
            print(e)
#-if DEBUG_FZM
            self.FZprint("FourZeroManager config failed")
#-endif
            raise CloudConfigError
    def subscribe(self):
        try:
#-if DEBUG_FZM
            self.FZprint("FourZeroManager subscribe")
#-endif
            self.device.mqtt.subscribe([[self.sub_topic,1]])
#-if DEBUG_FZM
            self.FZprint("FourZeroManager subscribe done")
#-endif
        except Exception as e:
#-if DEBUG_FZM
            self.FZprint("FourZeroManager subscribe failed")
#-endif
            raise CloudSubscriptionError
    def connect(self):
#-if DEBUG_FZM
        self.FZprint("FourZeroManager connect...")
#-endif
        for i in range(5):
            try:
#-if DEBUG_FZM
                self.FZprint("attempt",i+1,'...')
#-endif
                self.device.mqtt.connect(sock_keepalive=[1,30,60], aconnect_cb=self.subscribe)
                self.device.mqtt.loop()
#-if DEBUG_FZM
                self.FZprint("...done, connected")
#-endif
                break
            except Exception as e:
                print(e)
#-if DEBUG_FZM
                self.FZprint("... failed",e)
#-endif
        else:
#-if DEBUG_FZM
            self.FZprint("Unable to start mqtt FourZeroManager")
#-endif
            raise CloudConnectionError
        self._config()
    def handle_mqtt_msg(self, client, data):
        try:
            msg = data['message']
#-if DEBUG_FZM
            self.FZprint("------- received mqtt msg------------")
            self.FZprint(" -", msg.topic)
            self.FZprint(" -", msg.payload)
#-endif
            payload = json.loads(msg.payload)
            if 'cmd' in payload and payload['cmd'] in fzp_cmd:
                fzp_cmd[payload['cmd']](self, payload)
            elif 'rpc' in payload and payload['method'] in self.rpc:
                try:
                    res = self.rpc[payload['method']](self, *payload["args"])
                    status = 'ok'
                except Exception as e:
                    res = e
                    status = "error"
                if "ret" in payload and payload["ret"]:
                    ans = {
                        "rpc":payload["rpc"],
                        "method": payload["method"],
                        "args": payload["args"],
                        "status": status,
                        "result": res
                    }
                    self.publish(self.rpy_topic, json.dumps(ans))
            else:
#-if DEBUG_FZM
                self.FZprint("received unknown message")
#-endif
                pass
        except Exception as e:
            print(e)
#-if DEBUG_FZM
            self.FZprint("handle_mqtt_msg", e)
#-endif
    def upd_job(self, jobid, status, message):
        cmd = {
            "cmd":"job",
            "jobid":jobid,
            "status":status,
            "message":message
        }
        self.publish(self.rpy_topic, json.dumps(cmd))
    def check_job(self):
        data = {
            'cmd': "jobs"
        }
        self.publish(self.rpy_topic, json.dumps(data))
    def send_status(self):
        rec = fota.get_record()
        if rec[4]==rec[5] and rec[2]==rec[3]:
            # bytecode and vm are stable, send status
            vminfo = vm.info()
            data = {
                'cmd': "status",
                "vm_uid":vminfo[0],
                "bc_slot":rec[4],
                "vm_slot":rec[2]
            }
            self.publish(self.rpy_topic, json.dumps(data))
    # publish data
    def publish(self, topic=None, data=None):
        if topic == None:
            topic = self.pub_topic
        try:
            if not self.fota_ongoing:
                self.device.mqtt.publish(topic, data)
        except MQTTConnectionError as e:
#-if DEBUG_FZM
            self.FZprint('Publish exception: ', e)
#-endif
            raise MQTTConnectionError
        except Exception as e:
#-if DEBUG_FZM
            self.FZprint('Publish exception: ', e)
#-endif
            raise CloudPublishError