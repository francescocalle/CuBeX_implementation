import cv2
import numpy as np
import serial
import serial.tools
import serial.tools.list_ports
#VALORI MODIFICABILI
rapportoH = 0.5 #rapporto altezza larghezza video
cr = 3  #distanza croce colori
soglia_errore = 0.7 #soglia errore per il riconoscimento

#VALORI FISSI
dis= 2  #distanza tra cubetti nella rappresentazione
trovato = 0 #variabile di controllo per trovare la misura del video
dc = 0 #dimensione cubetti
rapportovideo = 0.2 #fattore di riduzione video
exit = 0 #variabile di uscita
tr = 0 #variabile per il training
trainer = 0 #variabile per il trainer
controllo = 0 #variabile per il controllo
colorazioni = np.array([[235, 235, 235],    #BIANCO
                        [  0, 255, 255],    #GIALLO
                        [  0, 255,   0],    #VERDE
                        [255,   0,   0],    #BLU
                        [  0,   0, 255],    #ROSSO
                        [  0, 110, 255],    #ARANCIONE
                        [ 80,  40,  37]])   #NERO
STRINGA_FACCE = np.array([[6,6,6,6,6,6,6,6],    #BIANCO
                          [6,6,6,6,6,6,6,6],    #GIALLO
                          [6,6,6,6,6,6,6,6],    #VERDE
                          [6,6,6,6,6,6,6,6],    #BLU
                          [6,6,6,6,6,6,6,6],    #ROSSO
                          [6,6,6,6,6,6,6,6]])   #ARANCIONE
ingressi1 = np.array([[163/255, 178/255, 209/255],  #BIANCO           #INPUT
                      [ 68/255, 183/255, 215/255],  #GIALLO
                      [ 85/255, 165/255, 130/255],  #VERDE
                      [143/255, 127/255,  28/255],  #BLU
                      [ 15/255,   5/255, 180/255],  #ROSSO
                      [  5/255,  82/255, 236/255]]) #ARANCIONE

#CODICE PER LE INTERAZIONI
def mouse_callback(event, x, y, flags, param):
    global exit
    global ltot
    global schermo
    global dis
    global dc
    global tr
    global colore1
    global ingressi1
    global enable
    if event == cv2.EVENT_LBUTTONDOWN:  # Controlla se il tasto sinistro del mouse è stato premuto
        if int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciabianca(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[0][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[0][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[0][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[0][0]*255),int(ingressi1[0][1]*255),int(ingressi1[0][2]*255)), thickness=-1)
                enable[0] = 1

        if int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciagialla(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[1][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[1][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[1][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[1][0]*255),int(ingressi1[1][1]*255),int(ingressi1[1][2]*255)), thickness=-1)
                enable[1] = 1

        if int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciaverde(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[2][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[2][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[2][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[2][0]*255),int(ingressi1[2][1]*255),int(ingressi1[2][2]*255)), thickness=-1)
                enable[2] = 1

        if int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciablu(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[3][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[3][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[3][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[3][0]*255),int(ingressi1[3][1]*255),int(ingressi1[3][2]*255)), thickness=-1)
                enable[3] = 1

        if int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciarossa(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[4][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[4][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[4][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[4][0]*255),int(ingressi1[4][1]*255),int(ingressi1[4][2]*255)), thickness=-1)
                enable[4] = 1

        if int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            if tr == 0:
                facciaarancione(dis, dc, colore1, schermo)
            elif tr == 1:
                ingressi1[5][0] = (colore1[0][0]/255+colore1[1][0]/255+colore1[2][0]/255+colore1[3][0]/255+colore1[4][0]/255+colore1[5][0]/255+colore1[6][0]/255+colore1[7][0]/255)/8
                ingressi1[5][1] = (colore1[0][1]/255+colore1[1][1]/255+colore1[2][1]/255+colore1[3][1]/255+colore1[4][1]/255+colore1[5][1]/255+colore1[6][1]/255+colore1[7][1]/255)/8
                ingressi1[5][2] = (colore1[0][2]/255+colore1[1][2]/255+colore1[2][2]/255+colore1[3][2]/255+colore1[4][2]/255+colore1[5][2]/255+colore1[6][2]/255+colore1[7][2]/255)/8
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(ingressi1[5][0]*255),int(ingressi1[5][1]*255),int(ingressi1[5][2]*255)), thickness=-1)
                enable[5] = 1
        if int(schermo.shape[1]*0.75-(dc*0.5))+dis <= x <= int(schermo.shape[1]*0.75+(dc*0.5))-dis and int(schermo.shape[0]*0.25-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.25+(dc*0.5))-dis: 
            cleaner(dis, dc, colore1, schermo)
            enable[0] = 0
            enable[1] = 0
            enable[2] = 0
            enable[3] = 0
            enable[4] = 0
            enable[5] = 0
        if ltot-40 <= x <= ltot and 0 <= y <= 30:
            exit = 1
        if int(ltot*0.6) <= x <= int(ltot*0.7) and int(htot*0.5)-30 <= y <= int(htot*0.5)+30:
            if tr == 0:
                tr = 1
                cleaner(dis, dc, colore1, schermo)
                enable[0] = 0
                enable[1] = 0
                enable[2] = 0
                enable[3] = 0
                enable[4] = 0
                enable[5] = 0
                training()
        if int(ltot*0.8) <= x <= int(ltot*0.9) and int(htot*0.5)-30 <= y <= int(htot*0.5)+30:
            if tr == 0:
                inviovalori()

    if event == cv2.EVENT_MOUSEMOVE:
        if ltot-40 <= x <= ltot and 0 <= y <= 30:
            schermo = cv2.rectangle(schermo, (ltot,0), (ltot-40,30), color=(0,0,255), thickness=-1)
            schermo = cv2.line(schermo, (ltot-25,10), (ltot-15,20), color=(255, 255, 255), thickness=1)
            schermo = cv2.line(schermo, (ltot-15,10), (ltot-25,20), color=(255, 255, 255), thickness=1)
        else:
            schermo = cv2.rectangle(schermo, (ltot,0), (ltot-40,30), color=(205,205,205), thickness=-1)
            schermo = cv2.line(schermo, (ltot-25,10), (ltot-15,20), color=(0, 0, 0), thickness=1)
            schermo = cv2.line(schermo, (ltot-15,10), (ltot-25,20), color=(0, 0, 0), thickness=1)
        
        if int(schermo.shape[1]*0.75-(dc*0.5))+dis <= x <= int(schermo.shape[1]*0.75+(dc*0.5))-dis and int(schermo.shape[0]*0.25-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.25+(dc*0.5))-dis: 
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=(120, 80, 80), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=( 80, 40, 37), thickness=-1)
        
        if int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(190, 190, 190), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=( 235,  235,  235), thickness=-1)
        
        if int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(0, 190, 190), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  255,  255), thickness=-1)

        if int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0, 190,  0), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  255,  0), thickness=-1)

        if int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  170,  0, 0), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  255,  0,  0), thickness=-1)

        if int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  0,  190), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  0,  255), thickness=-1)
        
        if int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis <= x <= int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis and int(schermo.shape[0]*0.75-(dc*0.5))+dis <= y <= int(schermo.shape[0]*0.75+(dc*0.5))-dis:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  90,  210), thickness=-1)
        else:
            schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(  0,  110,  255), thickness=-1)
        
        if int(ltot*0.6) <= x <= int(ltot*0.7) and int(htot*0.5)-30 <= y <= int(htot*0.5)+30:
            schermo = cv2.rectangle(schermo, (int(ltot*0.6), int(htot*0.5)-30), (int(ltot*0.7), int(htot*0.5)+30), color=(190,190,190), thickness=-1)
            schermo = cv2.putText(schermo, "TRAIN", (int(ltot*0.616), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)
        else:
            schermo = cv2.rectangle(schermo, (int(ltot*0.6), int(htot*0.5)-30), (int(ltot*0.7), int(htot*0.5)+30), color=(235,235,235), thickness=-1)
            schermo = cv2.putText(schermo, "TRAIN", (int(ltot*0.616), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)
            
        if int(ltot*0.8) <= x <= int(ltot*0.9) and int(htot*0.5)-30 <= y <= int(htot*0.5)+30:
            if tr == 0:
                schermo = cv2.rectangle(schermo, (int(ltot*0.8), int(htot*0.5)-30), (int(ltot*0.9), int(htot*0.5)+30), color=(190,190,190), thickness=-1)
                schermo = cv2.putText(schermo, "INVIO", (int(ltot*0.821), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)
        else:
            if tr == 0:
                schermo = cv2.rectangle(schermo, (int(ltot*0.8), int(htot*0.5)-30), (int(ltot*0.9), int(htot*0.5)+30), color=(235,235,235), thickness=-1)
                schermo = cv2.putText(schermo, "INVIO", (int(ltot*0.821), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)

def training():
    global tr
    global exit
    global schermo
    global ltot
    global htot
    global frame
    global dis
    global dc
    global colore1
    global colore2
    global colore3
    global colore4
    global colore5
    global colorazioni
    global STRINGA_FACCE
    global pesi1
    global pesi2
    global ingressi1
    global uscite
    global enable
    global lvid
    global hvid
    for i in range(0,8):
        STRINGA_FACCE[0][i] = 6
        STRINGA_FACCE[1][i] = 6
        STRINGA_FACCE[2][i] = 6
        STRINGA_FACCE[3][i] = 6
        STRINGA_FACCE[4][i] = 6
        STRINGA_FACCE[5][i] = 6
    while tr == 1:
        ret, frame = stream.read()  #leggo il frame dalla videocamera
        if not ret:
            print("non va")
        frame = cv2.flip(frame, 1)  #inverto il frame per avere l'immagine speculare
        frame = cv2.resize(frame, (lvid,hvid))  #ridimensiono il frame

        #genero la griglia sul video
        h=frame.shape[1]//2
        l=frame.shape[0]//2
        frame = cv2.line(frame, (h-dc//2, l-(dc+dc//2)), (h-dc//2, l+(dc+dc//2)), color=(255, 255, 255), thickness=2)
        frame = cv2.line(frame, (h+dc//2, l-(dc+dc//2)), (h+dc//2, l+(dc+dc//2)), color=(255, 255, 255), thickness=2)
        frame = cv2.line(frame, (h-(dc+dc//2), l-dc//2), (h+(dc+dc//2), l-dc//2), color=(255, 255, 255), thickness=2)
        frame = cv2.line(frame, (h-(dc+dc//2), l+dc//2), (h+(dc+dc//2), l+dc//2), color=(255, 255, 255), thickness=2)
        colore1[0]=frame[l-dc, h-dc]   #mi prendo i colori al centro dei cubetti
        colore1[1]=frame[l-dc, h   ]
        colore1[2]=frame[l-dc, h+dc]
        colore1[3]=frame[l,    h-dc]
        colore1[4]=frame[l,    h+dc]
        colore1[5]=frame[l+dc, h-dc]
        colore1[6]=frame[l+dc, h   ]
        colore1[7]=frame[l+dc, h+dc]

        colore2[0]=frame[l-dc+cr, h-dc]   #mi prendo i colori al centro dei cubetti
        colore2[1]=frame[l-dc+cr, h   ]
        colore2[2]=frame[l-dc+cr, h+dc]
        colore2[3]=frame[l+cr,    h-dc]
        colore2[4]=frame[l+cr,    h+dc]
        colore2[5]=frame[l+dc+cr, h-dc]
        colore2[6]=frame[l+dc+cr, h   ]
        colore2[7]=frame[l+dc+cr, h+dc]

        colore3[0]=frame[l-dc-cr, h-dc]   #mi prendo i colori al centro dei cubetti
        colore3[1]=frame[l-dc-cr, h   ]
        colore3[2]=frame[l-dc-cr, h+dc]
        colore3[3]=frame[l-cr,    h-dc]
        colore3[4]=frame[l-cr,    h+dc]
        colore3[5]=frame[l+dc-cr, h-dc]
        colore3[6]=frame[l+dc-cr, h   ]
        colore3[7]=frame[l+dc-cr, h+dc]

        colore4[0]=frame[l-dc, h-dc-cr]   #mi prendo i colori al centro dei cubetti
        colore4[1]=frame[l-dc, h-cr   ]
        colore4[2]=frame[l-dc, h+dc-cr]
        colore4[3]=frame[l,    h-dc-cr]
        colore4[4]=frame[l,    h+dc-cr]
        colore4[5]=frame[l+dc, h-dc-cr]
        colore4[6]=frame[l+dc, h-cr   ]
        colore4[7]=frame[l+dc, h+dc-cr]

        colore5[0]=frame[l-dc, h-dc+cr]   #mi prendo i colori al centro dei cubetti
        colore5[1]=frame[l-dc, h+cr   ]
        colore5[2]=frame[l-dc, h+dc+cr]
        colore5[3]=frame[l,    h-dc+cr]
        colore5[4]=frame[l,    h+dc+cr]
        colore5[5]=frame[l+dc, h-dc+cr]
        colore5[6]=frame[l+dc, h+cr   ]
        colore5[7]=frame[l+dc, h+dc+cr]

        for i in range(0,8):  #media dei colori delle facce
            colore1[i][0]=(colore1[i][0]//5+colore2[i][0]//5+colore3[i][0]//5+colore4[i][0]//5+colore5[i][0]//5)
            colore1[i][1]=(colore1[i][1]//5+colore2[i][1]//5+colore3[i][1]//5+colore4[i][1]//5+colore5[i][1]//5)
            colore1[i][2]=(colore1[i][2]//5+colore2[i][2]//5+colore3[i][2]//5+colore4[i][2]//5+colore5[i][2]//5)

        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
        schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
        schermo[:hvid, :lvid-1] = frame[:hvid, :lvid-1]

        if(enable[0] == 1 and enable[1] == 1 and enable[2] == 1 and enable[3] == 1 and enable[4] == 1 and enable[5] == 1):
            cleaner(dis, dc, colore1, schermo)
            enable[0] = 0
            enable[1] = 0
            enable[2] = 0
            enable[3] = 0
            enable[4] = 0
            enable[5] = 0
            cv2.imshow("finestra", schermo)      #mostro il frame a schermo
            # Parametri di training
            epoche = 10001
            tasso_apprendimento = 1
            pesi1 = inizializza_pesi(3, 10)
            pesi2 = inizializza_pesi(10, 6)
            pesi1, pesi2 = addestra_rete(ingressi1, uscite, pesi1, pesi2, epoche, tasso_apprendimento)
            break
        else:
            cv2.imshow("finestra", schermo)      #mostro il frame a schermo
        if exit == 1:
            break
        if cv2.waitKey(1) & 0xFF == 1234567:
            break


def inviovalori():
    global facciaI
    global STRINGA_FACCE
    global controllo
    global ser
    print("")
    print("  0% - Controllo valori")
    controllo = 0
    for i in range(0,6):
        for j in range(0,8):
            if STRINGA_FACCE[i][j] == 6:
                controllo = 1
    if controllo == 1:
        print("  #% - colori mancanti")
    else:
        print(" 50% - Invio valori")
        for i in range(0,6):
            facciaI[i] = str(STRINGA_FACCE[i][2]) + str(STRINGA_FACCE[i][1]) + str(STRINGA_FACCE[i][0]) + str(STRINGA_FACCE[i][4]) + str(STRINGA_FACCE[i][3]) + str(STRINGA_FACCE[i][7]) + str(STRINGA_FACCE[i][6]) + str(STRINGA_FACCE[i][5])
        stringafacce = str(facciaI[0]) + str(facciaI[1]) + str(facciaI[2]) + str(facciaI[3]) + str(facciaI[4]) + str(facciaI[5])
        ser.write(stringafacce.encode())
        cleaner(dis, dc, colore1, schermo)
        print("100% - Valori inviati: " + stringafacce)

def facciabianca(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[0][i] = colore[i]

def facciagialla(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[1][i] = colore[i]

def facciaverde(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[2][i] = colore[i]

def facciablu(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[3][i] = colore[i]

def facciarossa(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[4][i] = colore[i]

def facciaarancione(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[5][i] = colore[i]

def cleaner(dis, dc, colore1, schermo):
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*1)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[0][i] = 6
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*2)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[1][i] = 6
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*3)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[2][i] = 6
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*4)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[3][i] = 6
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*5)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[4][i] = 6
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*1.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75-(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*1.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*0.5))+dis, int(schermo.shape[0]*0.75+(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*6)-0.06)+(dc*1.5))-dis, int(schermo.shape[0]*0.75+(dc*1.5))-dis), color=(80,40,37), thickness=-1)
    for i in range(0,8):
        STRINGA_FACCE[5][i] = 6

#CODICE PER RETE NEURALE
# Funzione per inizializzare i pesi della rete
def inizializza_pesi(dimensione_input, dimensione_output):
    return np.random.uniform(-1, 1, (dimensione_input, dimensione_output))

# Funzione di attivazione (Sigmoide)
def sigmoide(x):
    return 1 / (1 + np.exp(-x))

# Derivata della funzione sigmoide
def derivata_sigmoide(x):
    return x * (1 - x)

# Funzione per il training della rete neurale
def addestra_rete(ingressi, uscite, pesi1, pesi2, epoche, tasso_apprendimento):
    global trainer
    for epoca in range(epoche):
        # Passaggio in avanti
        livello1 = sigmoide(np.dot(ingressi, pesi1))
        livello2 = sigmoide(np.dot(livello1, pesi2))

        # Calcolo dell'errore
        errore = uscite - livello2

        # Retropropagazione
        delta_livello2 = errore * derivata_sigmoide(livello2)
        errore_livello1 = np.dot(delta_livello2, pesi2.T)
        delta_livello1 = errore_livello1 * derivata_sigmoide(livello1)

        # Aggiornamento dei pesi
        pesi2 += np.dot(livello1.T, delta_livello2) * tasso_apprendimento
        pesi1 += np.dot(ingressi.T, delta_livello1) * tasso_apprendimento

    # Stampa dell'errore alla fine del training
    if trainer == 0:
        print(f" 80% - Epoca: {epoche-1}, Errore: {np.mean(np.abs(errore))}")
        trainer = 1
    else:
        print( "")
        print( "  0% - Re-Training in corso...")
        print(f" 50% - Epoca: {epoche-1}, Errore: {np.mean(np.abs(errore))}")
        print( "100% - Re-Training completato")

    return pesi1, pesi2

# Funzione per testare la rete neurale
def testa_rete(ingressi, pesi1, pesi2):
    livello1 = sigmoide(np.dot(ingressi, pesi1))
    livello2 = sigmoide(np.dot(livello1, pesi2))
    return livello2

# Parametri di training
epoche = 10001
tasso_apprendimento = 1
pesi1 = inizializza_pesi(3, 10)
pesi2 = inizializza_pesi(10, 6)

print("  0% - Inizializzazione comunicazione seriale...")
#CODICE COMUNICAZIONE SERIALE
porta = ""
coms = serial.tools.list_ports.comports()
for com in coms:
    descrizione = com.description
    for i in range(len(descrizione)-5):
        if(descrizione[i] == "C" and descrizione[i+1] == "P" and descrizione[i+2] == "2" and descrizione[i+3] == "1" and descrizione[i+4] == "0" and descrizione[i+5] == "x"):
            porta = com.device
if porta == "":
    print("  0% - Nessun dispositivo trovato...")
    print("")
    print("  #% - ARRESTO FORZATO")
    while True:
        #non fafre nulla
        nulla = 0
    exit(0)
else:
    print(" 20% - PORTA SCELTA: ", porta)

ser = serial.Serial(port=porta, baudrate=115200)
print(" 40% - Inizializzaizone schermata...")

#CODICE PER LO SCHERMO
cv2.namedWindow("finestra", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("finestra", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("finestra", mouse_callback)
ltot = cv2.getWindowImageRect("finestra")[2]
htot = cv2.getWindowImageRect("finestra")[3]
schermo = np.zeros((htot,ltot,3), np.uint8)  #creo uno schemo nero
schermo = cv2.rectangle(schermo, (0,0), (ltot,htot), color=(80,40,37), thickness=-1)
schermo = cv2.rectangle(schermo, (ltot,0), (ltot-40,30), color=(205,205,205), thickness=-1)
schermo = cv2.line(schermo, (ltot-25,10), (ltot-15,20), color=(0, 0, 0), thickness=1)
schermo = cv2.line(schermo, (ltot-15,10), (ltot-25,20), color=(0, 0, 0), thickness=1)
schermo = cv2.rectangle(schermo, (int(ltot*0.6), int(htot*0.5)-30), (int(ltot*0.7), int(htot*0.5)+30), color=(235,235,235), thickness=-1)
schermo = cv2.rectangle(schermo, (int(ltot*0.8), int(htot*0.5)-30), (int(ltot*0.9), int(htot*0.5)+30), color=(235,235,235), thickness=-1)
schermo = cv2.putText(schermo, "TRAIN", (int(ltot*0.616), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)
schermo = cv2.putText(schermo, "INVIO", (int(ltot*0.821), int(htot*0.515)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 143), 2, cv2.LINE_AA)
dc = ltot//21  #dimensione del cubo
#croce alta
schermo = cv2.line(schermo, (int(schermo.shape[1]*0.75-dc//2), schermo.shape[0]//4-(dc+dc//2)), (int(schermo.shape[1]*0.75-dc//2), schermo.shape[0]//4+(dc+dc//2)), color=(255, 255, 255), thickness=2)
schermo = cv2.line(schermo, (int(schermo.shape[1]*0.75+dc//2), schermo.shape[0]//4-(dc+dc//2)), (int(schermo.shape[1]*0.75+dc//2), schermo.shape[0]//4+(dc+dc//2)), color=(255, 255, 255), thickness=2)
schermo = cv2.line(schermo, (int(schermo.shape[1]*0.75-(dc+dc//2)), schermo.shape[0]//4-dc//2), (int(schermo.shape[1]*0.75+(dc+dc//2)), schermo.shape[0]//4-dc//2), color=(255, 255, 255), thickness=2)
schermo = cv2.line(schermo, (int(schermo.shape[1]*0.75-(dc+dc//2)), schermo.shape[0]//4+dc//2), (int(schermo.shape[1]*0.75+(dc+dc//2)), schermo.shape[0]//4+dc//2), color=(255, 255, 255), thickness=2)
#croci basse
for i in range(1,7):
    ofset = (0.16*i)-0.06
    schermo = cv2.line(schermo, (int(schermo.shape[1]*ofset-dc//2), int(schermo.shape[0]*0.75-(dc+dc//2))), (int(schermo.shape[1]*ofset-dc//2), int(schermo.shape[0]*0.75+(dc+dc//2))), color=(255, 255, 255), thickness=2)
    schermo = cv2.line(schermo, (int(schermo.shape[1]*ofset+dc//2), int(schermo.shape[0]*0.75-(dc+dc//2))), (int(schermo.shape[1]*ofset+dc//2), int(schermo.shape[0]*0.75+(dc+dc//2))), color=(255, 255, 255), thickness=2)
    schermo = cv2.line(schermo, (int(schermo.shape[1]*ofset-(dc+dc//2)), int(schermo.shape[0]*0.75-dc//2)), (int(schermo.shape[1]*ofset+(dc+dc//2)), int(schermo.shape[0]*0.75-dc//2)), color=(255, 255, 255), thickness=2)
    schermo = cv2.line(schermo, (int(schermo.shape[1]*ofset-(dc+dc//2)), int(schermo.shape[0]*0.75+dc//2)), (int(schermo.shape[1]*ofset+(dc+dc//2)), int(schermo.shape[0]*0.75+dc//2)), color=(255, 255, 255), thickness=2)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*((0.16*i)-0.06)-(dc*0.5))+dis, int(schermo.shape[0]*0.75-(dc*0.5))+dis), (int(schermo.shape[1]*((0.16*i)-0.06)+(dc*0.5))-dis, int(schermo.shape[0]*0.75+(dc*0.5))-dis), color=tuple(map(int, colorazioni[i-1])), thickness=-1)

enable  = [0]*6  #creo una lista per i colori delle facce rappresentate
facciaI  = [0]*6  #creo una lista per i colori delle facce rappresentate
colore  = [0]*8  #creo una lista per i colori delle facce rappresentate
colore1 = [0]*8    #creo una lista per i colori delle facce rappresentate
colore2 = [0]*8    #creo una lista per i colori delle facce rappresentate
colore3 = [0]*8    #creo una lista per i colori delle facce rappresentate
colore4 = [0]*8    #creo una lista per i colori delle facce rappresentate
colore5 = [0]*8    #creo una lista per i colori delle facce rappresentate
stream = cv2.VideoCapture(0)  #inizializzo la videocamera
if not stream.isOpened():   #controllo se la videocamera è aperta
    print("non va")
    exit()


#CODICE DI TRAINING INIZIALE
# Inizializzazione dei dati
ingressi = np.array([[163/255, 178/255, 209/255],  #BIANCO           #INPUT
                     [ 68/255, 183/255, 215/255],  #GIALLO
                     [ 85/255, 165/255, 130/255],  #VERDE
                     [143/255, 127/255,  28/255],  #BLU
                     [ 15/255,   5/255, 180/255],  #ROSSO
                     [  5/255,  82/255, 236/255]]) #ARANCIONE

uscite   = np.array([[1, 0, 0, 0, 0, 0],  #BIANCO           #OUTPUT
                     [0, 1, 0, 0, 0, 0],  #GIALLO
                     [0, 0, 1, 0, 0, 0],  #VERDE
                     [0, 0, 0, 1, 0, 0],  #BLU
                     [0, 0, 0, 0, 1, 0],  #ROSSO
                     [0, 0, 0, 0, 0, 1]]) #ARANCIONE

print(" 60% - Inizializzazione della Intelligenza Artificiale...")
#TRANING CON QUESTI VALORI
pesi1, pesi2 = addestra_rete(ingressi, uscite, pesi1, pesi2, epoche, tasso_apprendimento)

print("100% - Inizializzazione della schermata...")
#CODICE CHE SI RIPETE ALL INFINITO
while True:
    ret, frame = stream.read()  #leggo il frame dalla videocamera
    if not ret:
        print("non va")
    frame = cv2.flip(frame, 1)  #inverto il frame per avere l'immagine speculare
    if trovato == 0:
        while (int(ltot*rapportovideo)*frame.shape[0])//frame.shape[1] < int(htot*rapportoH):
            rapportovideo = rapportovideo + 0.01  #aumento il rapporto video
        trovato = 1  #setto trovato a 1 per non entrare più in questo ciclo
    lvid = int(ltot*rapportovideo)  #calcolo la larghezza del video
    hvid = (lvid*frame.shape[0])//frame.shape[1]  #calcolo l'altezza del video
    frame = cv2.resize(frame, (lvid,hvid))  #ridimensiono il frame
    tr = 0
    
    #genero la griglia sul video
    h=frame.shape[1]//2
    l=frame.shape[0]//2
    frame = cv2.line(frame, (h-dc//2, l-(dc+dc//2)), (h-dc//2, l+(dc+dc//2)), color=(255, 255, 255), thickness=2)
    frame = cv2.line(frame, (h+dc//2, l-(dc+dc//2)), (h+dc//2, l+(dc+dc//2)), color=(255, 255, 255), thickness=2)
    frame = cv2.line(frame, (h-(dc+dc//2), l-dc//2), (h+(dc+dc//2), l-dc//2), color=(255, 255, 255), thickness=2)
    frame = cv2.line(frame, (h-(dc+dc//2), l+dc//2), (h+(dc+dc//2), l+dc//2), color=(255, 255, 255), thickness=2)
    colore1[0]=frame[l-dc, h-dc]/255   #mi prendo i colori al centro dei cubetti
    colore1[1]=frame[l-dc, h   ]/255
    colore1[2]=frame[l-dc, h+dc]/255
    colore1[3]=frame[l,    h-dc]/255
    colore1[4]=frame[l,    h+dc]/255
    colore1[5]=frame[l+dc, h-dc]/255
    colore1[6]=frame[l+dc, h   ]/255
    colore1[7]=frame[l+dc, h+dc]/255
    
    colore2[0]=frame[l-dc+cr, h-dc]/255   #mi prendo i colori al centro dei cubetti
    colore2[1]=frame[l-dc+cr, h   ]/255
    colore2[2]=frame[l-dc+cr, h+dc]/255
    colore2[3]=frame[l+cr,    h-dc]/255
    colore2[4]=frame[l+cr,    h+dc]/255
    colore2[5]=frame[l+dc+cr, h-dc]/255
    colore2[6]=frame[l+dc+cr, h   ]/255
    colore2[7]=frame[l+dc+cr, h+dc]/255

    colore3[0]=frame[l-dc-cr, h-dc]/255   #mi prendo i colori al centro dei cubetti
    colore3[1]=frame[l-dc-cr, h   ]/255
    colore3[2]=frame[l-dc-cr, h+dc]/255
    colore3[3]=frame[l-cr,    h-dc]/255
    colore3[4]=frame[l-cr,    h+dc]/255
    colore3[5]=frame[l+dc-cr, h-dc]/255
    colore3[6]=frame[l+dc-cr, h   ]/255
    colore3[7]=frame[l+dc-cr, h+dc]/255

    colore4[0]=frame[l-dc, h-dc-cr]/255   #mi prendo i colori al centro dei cubetti
    colore4[1]=frame[l-dc, h-cr   ]/255
    colore4[2]=frame[l-dc, h+dc-cr]/255
    colore4[3]=frame[l,    h-dc-cr]/255
    colore4[4]=frame[l,    h+dc-cr]/255
    colore4[5]=frame[l+dc, h-dc-cr]/255
    colore4[6]=frame[l+dc, h-cr   ]/255
    colore4[7]=frame[l+dc, h+dc-cr]/255

    colore5[0]=frame[l-dc, h-dc+cr]/255   #mi prendo i colori al centro dei cubetti
    colore5[1]=frame[l-dc, h+cr   ]/255
    colore5[2]=frame[l-dc, h+dc+cr]/255
    colore5[3]=frame[l,    h-dc+cr]/255
    colore5[4]=frame[l,    h+dc+cr]/255
    colore5[5]=frame[l+dc, h-dc+cr]/255
    colore5[6]=frame[l+dc, h+cr   ]/255
    colore5[7]=frame[l+dc, h+dc+cr]/255
    
    for i in range(0,8):  #media dei colori delle facce
        colore1[i][0]=(colore1[i][0]/5+colore2[i][0]/5+colore3[i][0]/5+colore4[i][0]/5+colore5[i][0]/5)
        colore1[i][1]=(colore1[i][1]/5+colore2[i][1]/5+colore3[i][1]/5+colore4[i][1]/5+colore5[i][1]/5)
        colore1[i][2]=(colore1[i][2]/5+colore2[i][2]/5+colore3[i][2]/5+colore4[i][2]/5+colore5[i][2]/5)

    risultati = testa_rete(colore1, pesi1, pesi2)
    for i in range(0,8):
        colore[i] = np.argmax(risultati[i]) #mi prendo il colore piu probabile
        if risultati[i][colore[i]] <= soglia_errore:
            colore[i] = 6
        if colore[i] == 0:
            colore1[i] = colorazioni[0] #BIANCO
        if colore[i] == 1:
            colore1[i] = colorazioni[1] #GIALLO
        if colore[i] == 2:
            colore1[i] = colorazioni[2] #VERDE
        if colore[i] == 3:
            colore1[i] = colorazioni[3] #BLU
        if colore[i] == 4:
            colore1[i] = colorazioni[4] #ROSSO
        if colore[i] == 5:
            colore1[i] = colorazioni[5] #ARANCIONE
        if colore[i] == 6:
            colore1[i] = colorazioni[6] #NERO

    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[0][0]),int(colore1[0][1]),int(colore1[0][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[1][0]),int(colore1[1][1]),int(colore1[1][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*1.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25-(dc*0.5))-dis), color=(int(colore1[2][0]),int(colore1[2][1]),int(colore1[2][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=(int(colore1[3][0]),int(colore1[3][1]),int(colore1[3][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25-(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25+(dc*0.5))-dis), color=(int(colore1[4][0]),int(colore1[4][1]),int(colore1[4][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*1.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75-(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[5][0]),int(colore1[5][1]),int(colore1[5][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75-(dc*0.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*0.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[6][0]),int(colore1[6][1]),int(colore1[6][2])), thickness=-1)
    schermo = cv2.rectangle(schermo, (int(schermo.shape[1]*0.75+(dc*0.5))+dis, int(schermo.shape[0]*0.25+(dc*0.5))+dis), (int(schermo.shape[1]*0.75+(dc*1.5))-dis, int(schermo.shape[0]*0.25+(dc*1.5))-dis), color=(int(colore1[7][0]),int(colore1[7][1]),int(colore1[7][2])), thickness=-1)
    schermo[:hvid, :lvid-1] = frame[:hvid, :lvid-1]
    cv2.imshow("finestra", schermo)      #mostro il frame a schermo

    if exit == 1:  # Controlla se `exit` è stato impostato a 1
        break
    if cv2.waitKey(1) & 0xFF == 1234567:
        break

stream.release()        #detono il frame
ser.close()
cv2.destroyAllWindows()
print("")
print("  #% - ARRESTO FORZATO")
while True:
    #non fafre nulla
    nulla = 0
exit(0)