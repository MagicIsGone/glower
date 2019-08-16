import pymem
import pymem.process
from time import sleep
import keyboard

#offsets
dwGlowObjectManager = (0x52470F0)
dwEntityList = (0x4D06CB4)
m_iTeamNum = (0xF4)
m_iGlowIndex = (0xA40C)
dwLocalPlayer = (0xCF4A3C)

try: #hook to csgo
    pym = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll
except:
    print("CSGO was not detected, closing application.")
    sleep(3)
    exit()

#color vars 
tcolorr = None 
tcolorb = None
ctcolorr = None 
ctcolorb = None

key = "right shift"

while True:
    if keyboard.is_pressed(key):
        sleep(0.1)
        while True:
            try:
                glow = pym.read_int(dwGlowObjectManager + client)
                lp = pym.read_int(dwLocalPlayer + client)
                lpt = pym.read_int(lp + m_iTeamNum) #local player's team

                if lpt == 2: #t
                    ctcolorr = 1
                    ctcolorb = 0
                    tcolorr = 0
                    tcolorb = 1

                elif lpt == 3: #ct
                    tcolorr = 1
                    tcolorb = 0 
                    ctcolorr = 0
                    ctcolorb = 1

                for i in range(1, 25):
                    player = pym.read_int(client + dwEntityList + i * 0x10)

                    if player:
                        team = pym.read_int(player + m_iTeamNum)
                        playerglow = pym.read_int(player + m_iGlowIndex)

                        if team == 2: #t
                            pym.write_float(glow + playerglow * 0x38 + 0x4, float(tcolorr)) #Red
                            pym.write_float(glow + playerglow * 0x38 + 0xC, float(tcolorb)) #Blue
                            pym.write_float(glow + playerglow * 0x38 + 0x10, float(0.8)) #Opacity
                            pym.write_int(glow + playerglow * 0x38 + 0x24, int(1)) 
                        
                        elif team == 3: #ct
                            pym.write_float(glow + playerglow * 0x38 + 0x4, float(ctcolorr)) #Red
                            pym.write_float(glow + playerglow * 0x38 + 0xC, float(ctcolorb)) #Blue
                            pym.write_float(glow + playerglow * 0x38 + 0x10, float(0.8)) #Opacity
                            pym.write_int(glow + playerglow * 0x38 + 0x24, int(1))      
                
                            
            except pymem.exception.MemoryReadError:
                pass
        
            if keyboard.is_pressed(key):
                sleep(0.1)
                break






