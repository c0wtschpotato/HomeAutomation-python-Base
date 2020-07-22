import os
import configparser, time, json, HomaClass as home
##learnfile sudo python python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --learn --learnfile python-broadlink/cli/philips-up.vol_change


import paho.mqtt.client as mqtt
HOST = 'localhost'
PORT = 1883
client = mqtt.Client()

cfgpath = "/var/lib/snips/skills/Snips-HomA/cfg.ini"
config = configparser.ConfigParser()
initcfg = configparser.ConfigParser()
initcfg.read(cfgpath)
print initcfg.sections()
# old send path rmSendPath = "sudo python python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --send "
rmSendPath = "sudo python /home/pi/python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c55834ea34 --send "
syn_IR = ["vol_up","vol_down","brightness_up", "brightness_down","targetchannel"]
def cfgcompare():##Reads cfg for changes to apply
        config.read(cfgpath)
        
        for section in initcfg.sections():
                
                for key in initcfg[section]:
                        
                        if initcfg[section][key] != config[section][key]:
                                print(key+" changed from "+initcfg[section][key]+ " to "+  config[section][key] )
                                decidemethod(config[section]['type'],initcfg[section],key,config[section][key])
                                
def on_connect(client, userdata, flags, rc):
        print("Connected to {0} with result code {1}".format(HOST, rc))
        client.subscribe("hermes/hotword/default/detected")
        client.subscribe("hermes/hotword/toggleOn")
        client.subscribe("HomA/ledstrip1/get_status")
        client.subscribe("HomA/ledstrip1/set_status")
        client.subscribe("HomA/test")
        client.subscribe("HomA/hts/cmd")
        client.subscribe("HomA/status")
        client.subscribe("HomA/mhz/cmd")
        client.subscribe("HomA/pc/cmd")


def decidemethod(type,section = "11001",key = "3",value = "0"):### picks type and way to proceed
        
        if type == "rf":
                os.system("sudo /home/pi/raspberry-remote/./send "+str(section)[10:][:-1]+ " "+str(key)+" "+str(value))
                
                
        if type == "ir":
                print("in ir")
                # print(rmSendPath+"@python-broadlink/cli/"+str(section)[10:][:-1]+"-"+str(key)+"."+str(value))
                if key in syn_IR:##if its volume change for philips
                        
                        if int(value)> 10:
                                value = "10"
                        for x in range(0,abs(int(value))+1):
                                print("in specials")
                                
                                if key == "vol_up":
                                        print("volume up")
                                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/philips-up.vol_change")
                                if key == "vol_down":
                                        print("volume down")
                                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/philips-down.vol_change")
                                if key == "brightness_up":      
                                        print("brightness_up")          
                                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/couchled-up.brightness")
                                if key == "brightness_down":    
                                        print("brightness_down")                                        
                                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/couchled-down.brightness")
                                if key == "targetchannel":##actuellen channel holen und pushes bis hdmi hochrechnen
                                        config = configparser.ConfigParser()
                                        config.read(cfgpath)
                                        curr_channel = int(config["philips"]["channel"])#0 hdmi, 1 fm, 2 bt, 3 apps, 4bd in, 5 aux
                                        targetchannel =  int(config["philips"]["targetchannel"])
                                        if curr_channel == targetchannel:## ist bereits current channel
                                                print("already on targetchannel"+str(curr_channel)+ " of "+str(targetchannel))
                                                
                                        else:
                                                print ("started from "+str(curr_channel)+ " to ")

                                                for i in range(curr_channel,6):
                                                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/philips-switch.source")

                                                        time.sleep(1)
                                                        i = i+1
                                                        print("switch to"+ str(i))
                                                        if i == targetchannel:
                                                                print("channel bereits erreicht")
                                                                break

                                                        if i == 6:
                                                                i = 0
                                                                print("reached 5")
                                                config.read(os.path.join(os.getcwd(), cfgpath))
                                                config["philips"]["channel"] = config["philips"]["targetchannel"]
                                                with open(cfgpath, 'w') as configfile:
                                                        config.write(configfile)
                                                return

                                                
                                config = configparser.ConfigParser()
                                config.read(os.path.join(os.getcwd(), cfgpath))
                                config['philips']['vol_up'] = '0'
                                config['philips']['vol_down'] = '0'     
                                config['couchled']['brightness_up'] = '0'
                                config['couchled']['brightness_down'] = '0'             
                                with open(cfgpath, 'w') as configfile:
                                        config.write(configfile)


                else:
                        os.system(rmSendPath+"@/home/pi/python-broadlink/cli/"+str(section)[10:][:-1]+"-"+str(value)+"."+str(key))
        # if type == "software":
        global initcfg
        initcfg.read(cfgpath)

def on_message(client, userdata, msg):
        print(msg.payload)
        if msg.topic == "HomA/status":
                print("Status request for "+str(msg.payload))
                if msg.payload == "hts":
                        print("sending status: ")
                        print(home.hts.__dict__)
                        client.publish("HomA/status",json.loads(home.hts.__dict__))


client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)

client.loop_forever()














