from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QMainWindow, QComboBox
from PyQt5.QtCore import QRect
from threading import Thread
import sys
import pickle
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

app = QApplication(sys.argv)


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

def apply():
    global key, cscheme
    text = gui.line.text()
    pickle.dump(text, open("data//togglekey.dat", "wb"))
    key = text
    cscheme = gui.ls.currentText()
    pickle.dump(cscheme, open("data//colorscheme.dat", "wb"))
    


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.restore()
    
    def restore(self):
        tkey = pickle.load(open("data//togglekey.dat", "rb"))
        colorscheme = pickle.load(open("data//colorscheme.dat", "rb"))
        self.line.setText(tkey)
        self.ls.setCurrentText(colorscheme)
        
    
    def initUI(self):

        self.setGeometry(0, 0, 210, 117)
        self.setWindowTitle("glwr")
        self.setWindowIcon(QIcon("assets//ico.png"))

        schm = QLabel("Color Scheme: ", self)
        schm.move(5, 5)
        schm.setFont(QFont("Calibri", 11))

        self.ls = QComboBox(self)
        self.ls.move(50, 5)
        self.ls.setGeometry(QRect(103, 10, 100, 21))
        self.ls.setObjectName("comboBox")
        self.ls.addItem("Red & Blue")
        self.ls.addItem("Orange & Green")
        self.ls.setFont(QFont("Calibri", 9))
        

        t = QLabel("Toggle Key: ", self)
        t.move(5, 30)
        t.setFont(QFont("Calibri", 11))

        self.line = QLineEdit(self)
        self.line.resize(120, 21)
        self.line.move(83, 35)
        self.line.setFont(QFont("Calibri", 10))
        
        self.btn = QPushButton(self)
        self.btn.setText("Apply")
        self.btn.setFont(QFont("Calibri", 10))
        self.btn.resize(199, 30)
        self.btn.move(5, 60)
        self.btn.clicked.connect(apply)

        dev = QLabel(self)
        dev.setText("Developed by cududont")
        dev.setFont(QFont("Calibri", 10))
        dev.resize(130, 30)
        dev.move(5, 90)       

        self.show()



gui = main()
key = pickle.load(open("data//togglekey.dat", "rb"))
cscheme = pickle.load(open("data//colorscheme.dat", "rb"))




def newthread():
    Thread(target=glowfunc).start()


def glowfunc():
    while True:
        if keyboard.is_pressed(key):
            sleep(0.1)
            while True:
                try:
                    glow = pym.read_int(dwGlowObjectManager + client)
                    lp = pym.read_int(dwLocalPlayer + client)
                    lpt = pym.read_int(lp + m_iTeamNum) #local player's team

                    if lpt == 2: #t
                        if cscheme == "Red & Blue":
                            ctcolorr = 1
                            ctcolorb = 0
                            ctcolorg = 0
                            tcolorr = 0
                            tcolorb = 1
                            tcolorg = 0

                        elif cscheme == "Orange & Green":
                            ctcolorr = 1
                            ctcolorb = 0
                            ctcolorg = 0.4
                            tcolorr = 0
                            tcolorb = 0
                            tcolorg = 1

                    elif lpt == 3: #ct
                        if cscheme == "Red & Blue":
                            ctcolorr = 0
                            ctcolorb = 1
                            ctcolorg = 0
                            tcolorr = 1
                            tcolorb = 0
                            tcolorg = 0

                        elif cscheme == "Orange & Green":
                            ctcolorr = 0
                            ctcolorb = 0
                            ctcolorg = 1
                            tcolorr = 1
                            tcolorb = 0
                            tcolorg = 0.4
                       
                    for i in range(1, 25):
                        player = pym.read_int(client + dwEntityList + i * 0x10)

                        if player:
                            team = pym.read_int(player + m_iTeamNum)
                            playerglow = pym.read_int(player + m_iGlowIndex)

                            if team == 2: #t
                                pym.write_float(glow + playerglow * 0x38 + 0x4, float(tcolorr)) #Red
                                pym.write_float(glow + playerglow * 0x38 + 0xC, float(tcolorb)) #Blue
                                pym.write_float(glow + playerglow * 0x38 + 0x8, float(tcolorg)) #Green
                                pym.write_float(glow + playerglow * 0x38 + 0x10, float(0.8)) #Opacity
                                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1)) 
                            
                            elif team == 3: #ct
                                pym.write_float(glow + playerglow * 0x38 + 0x4, float(ctcolorr)) #Red
                                pym.write_float(glow + playerglow * 0x38 + 0xC, float(ctcolorb)) #Blue
                                pym.write_float(glow + playerglow * 0x38 + 0x8, float(ctcolorg)) #Green
                                pym.write_float(glow + playerglow * 0x38 + 0x10, float(0.8)) #Opacity
                                pym.write_int(glow + playerglow * 0x38 + 0x24, int(1))      
                    
                                
                except pymem.exception.MemoryReadError:
                    pass
            
                if keyboard.is_pressed(key):
                    sleep(0.1)
                    break

newthread()
    
sys.exit(app.exec_())
    


