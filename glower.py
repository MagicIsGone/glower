import pymem
import pymem.process
from time import sleep

#offsets
dwGlowObjectManager = (0x52470F0)
dwEntityList = (0x4D06CB4)
m_iTeamNum = (0xF4)
m_iGlowIndex = (0xA40C)

try: #hook to csgo
    pym = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pym.process_handle, "client_panorama.dll").lpBaseOfDll
except:
    print("CSGO was not detected, closing application.")
    sleep(5)
    exit()


while True:
    glow = pym.read_int(dwGlowObjectManager + client)

    for i in range(1, 20): #should be entities 1-10 but chickens fuck shit up   
        player = pym.read_int(client + dwEntityList + i * 0x10)

        if player:
            team = pym.read_int(player + m_iTeamNum)
            playerglow = pym.read_int(player + m_iGlowIndex)

            if team == 2: #t
                pym.write_float(glow + playerglow * 0x38 + 0x4, float(0.7)) #Red 
                pym.write_float(glow + playerglow * 0x38 + 0x10, float(1)) #Opacity
                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1)) #Enable Glow
                
            elif team == 3: #ct
                pym.write_float(glow + playerglow * 0x38 + 0xC, float(0.7)) #Blue
                pym.write_float(glow + playerglow * 0x38 + 0x10, float(1)) #Opacity
                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1)) #Enable Glow 


