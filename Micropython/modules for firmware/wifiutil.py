#wifiutil.py
def loadConfig():
    from ujson import load
    file = open("config.json", "r")
    cfg = load(file)
    file.close()
    return cfg

#
def saveConfig(cfg):
    from ujson import dump
    from machine import reset
    origCfg = loadConfig() #cache original_config
    file = open('backup.json', 'w')
    config = origCfg.copy()
    c = dump(origCfg, file)
    file.close()
    # set new values
    ssid = cfg['ssid']
    pwd = cfg['pwd']
    mode = cfg['mode']
    if mode == 0:
        mode = 'station'
    elif mode == 1:
        mode = 'accesspoint'
    # cache values
    c_ssid = config['credentials']['ssid']
    c_pwd = config['credentials']['pwd']
    c_mode = config['credentials']['mode']
    # swap new values
    config['credentials']['ssid'] = ssid
    config['credentials']['pwd'] = pwd
    config['credentials']['mode'] = mode
    file = open('config.json', 'w')
    config = dump(config, file)
    file.close()
    # after saving reset machine
    reset()


def startWifi(cfg):
    from utime import sleep_ms
    from network import WLAN, STA_IF, AP_IF
    
    mode = cfg["settings"]["mode"]
    ssid = cfg["credentials"]["ssid"]
    pwd = cfg["credentials"]["pwd"]
    
    sta = WLAN(STA_IF)
    ap = WLAN(AP_IF)
    ap.active(False)
    
    timeout = 0
    maxtries = 30
    if mode == 'station':
        if not sta.isconnected():
            ap.active(False)
            sta.active(True)
            sta.connect(ssid, pwd)
            while not sta.isconnected():
                sleep_ms(1000) # sleep for 1 second
                timeout += 1
                if timeout > maxtries:
                    mode = 'accesspoint'
                    # maxtries reached
                    # givingup on Station Mode switching to AP Mode
                    break
        else:
            pass
    if mode == 'accesspoint':
        sta.active(False)
        ap.active(True)
        ap.config(essid='ESP8266-Access Point', password='1234567890')
        while ap.active() == False:
            pass


