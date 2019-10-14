import os
import configparser

##learnfile sudo python python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65c5$


config = configparser.ConfigParser()
initcfg = configparser.ConfigParser()
initcfg.read('cfg.ini')

rmSendPath = "sudo python python-broadlink/cli/./broadlink_cli --type 0x2737 --host 192.168.1.104 --mac 65$

def cfgcompare():##Reads cfg for changes to apply
        config.read("cfg.ini")

        for section in initcfg.sections():

                for key in initcfg[section]:

                        if initcfg[section][key] != config[section][key]:
                                print(key+" changed from "+initcfg[section][key]+ " to "+  config[section]$
                                decidemethod(config[section]['type'],initcfg[section],key,config[section][$



def decidemethod(type,section = "11001",key = "3",value = "0"):### picks type and way to proceed

        if type == "rf":
                os.system("sudo raspberry-remote/./send "+str(section)[10:][:-1]+ " "+str(key)+" "+str(val$


        if type == "ir":
                print("in ir")
                # print(rmSendPath+"@python-broadlink/cli/"+str(section)[10:][:-1]+"-"+str(key)+"."+str(va$
                if key == "vol_up" or key == "vol_down" or key == "brightness_up" or key == "brightness_do$

                        if int(value)> 10:
                                value = "10"
                        for x in range(0,abs(int(value))+1):
                                print("in specials")

                                if key == "vol_up":
                                        print("volume up")
                                        os.system(rmSendPath+"@python-broadlink/cli/"+str(section)[10:][:-$
                                if key == "vol_down":
                                        print("volume down")
                                        os.system(rmSendPath+"@python-broadlink/cli/"+str(section)[10:][:-$
                                if key == "brightness_up":
                                        print("brightness_up")
                                        os.system(rmSendPath+"@python-broadlink/cli/couchled-up.brightness$
                                if key == "brightness_down":
                                        print("brightness_down")
                                        os.system(rmSendPath+"@python-broadlink/cli/couchled-down.brightne$

                                config = configparser.ConfigParser()
                                config.read(os.path.join(os.getcwd(), 'cfg.ini'))
                                config['philips']['vol_up'] = '0'
                                config['philips']['vol_down'] = '0'
                                config['couchled']['brightness_up'] = '0'
                                config['couchled']['brightness_down'] = '0'
                                with open('cfg.ini', 'w') as configfile:
                                        config.write(configfile)


                else:
                        os.system(rmSendPath+"@python-broadlink/cli/"+str(section)[10:][:-1]+"-"+str(value$
        # if type == "software":
        global initcfg
        initcfg.read('cfg.ini')
while True:


        cfgcompare()

