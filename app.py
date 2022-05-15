#!/usr/bin/python 
#-*- coding: utf-8 -*-
import pytesseract
from PySimpleGUI import PySimpleGUI as sg
import cv2
class IotAm:

    def __init__(self):
        sg.theme('Reddit')
        layout = [
            [sg.Text('Lingua:', size=(10, 1)), 
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
                self.save_cur(text)
                break

    def get_lang(self, valores):
        if valores['lingua'].lower() == 'english':
            return 'eng'
        elif valores['lingua'].lower() == 'português':
            return 'por'
        elif valores['lingua'].lower() == 'spanish':
            return 'spa'
        else:
            return 'por'
        
    def treat_image(self):
        imagem = cv2.imread("Curriculo.JPG")
        imgH, imgW, _ = imagem.shape
        bil_gaussian_img = cv2.bilateralFilter(imagem, 9, 75, 75)
        cinza = cv2.cvtColor(bil_gaussian_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(cinza, 100, 255, cv2.THRESH_BINARY)
        print(ret)
        proporcao = float(imgH/imgW)
        new_Width = 620
        new_Height = int(new_Width*proporcao)
        new_Image =  cv2.resize(mask, (new_Width, new_Height), interpolation=cv2.INTER_AREA)
        cv2.imshow('Curriculo', new_Image)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return mask

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
                

win = IotAm()
win.Iniciar()                                               
