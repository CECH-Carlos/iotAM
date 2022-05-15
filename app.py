#!/usr/bin/python 
#-*- coding: utf-8 -*-
import time
import gtts
from playsound import playsound
import pytesseract
from PySimpleGUI import PySimpleGUI as sg
import cv2
class IotAm:

    def __init__(self):
        sg.theme('Reddit')
        layout = [
            [sg.Text('Selecione a lingua em que o CV está escrito.', font='21')],
            [sg.Text('Select the language in which the CV is written.', font='21')],
            [sg.Text('Seleccione el idioma en el que está escrito el CV.', font='21')],
            [sg.Text('Lingua:', font='21', size=(10, 1)), 
            sg.Combo(values=list(["português", "english", "spanish"]), key='lingua', default_value="português", size=(20, 1))],
            [sg.Button('Confirmar')]
        ]

        self.janela = sg.Window('Lingua do currículo', layout)

    def Iniciar(self):
        while True:
            evento, valores = self.janela.read()
            if evento == sg.WINDOW_CLOSED:
                break
            if evento == 'Confirmar':
                print(valores['lingua'])
                lan = self.get_lang(valores)
                imagem = self.treat_image()
                text = self.read_cur(lan, imagem)
                arq = self.save_cur(text)
                return arq

    def get_lang(self, valores):
        if valores['lingua'].lower() == 'english':
            return 'eng'
        elif valores['lingua'].lower() == 'português':
            return 'por'
        elif valores['lingua'].lower() == 'spanish':
            return 'spa'
        
    def treat_image(self):
        imagem = cv2.imread("./assets/Curriculo_por.JPEG", 0)
        imgW = imagem.shape[1]
        imgH = imagem.shape[0]
        #bil_gaussian_img = cv2.bilateralFilter(imagem, 9, 15, 15)
        #cinza = cv2.cvtColor(bil_gaussian_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(imagem, 56, 255, cv2.THRESH_BINARY)
        mask2 = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 7)
        print(imagem.shape)
        print(ret)
        proporcao = float(imgH/imgW)
        new_Width = 620
        new_Height = int(new_Width*proporcao)
        new_Image =  cv2.resize(mask2, (new_Width, new_Height), interpolation=cv2.INTER_AREA)
        cv2.imshow('Curriculo', new_Image)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return mask2

    def read_cur(self, lan, imagem):            
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
        config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(imagem, lang=lan, config=config) #
        
        return texto

    def save_cur(self, text):
        with open('curriculo.txt', 'a', newline='') as arquivo:
                arquivo.write(text)

                print('Currículo salvo!')

        return 'curriculo.txt'

def speak_voice(arq):
    with open(arq, 'r') as arquivo:
        for linha in arquivo:
            curriculo = gtts.gTTS(linha, lang='pt-br')
            curriculo.save('curriculo.mp3')
            playsound('curriculo.mp3')

iot = IotAm()
arq = iot.Iniciar()
time.sleep(1)
speak_voice(arq)
