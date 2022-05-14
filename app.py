#!/usr/bin/python 
#-*- coding: utf-8 -*-
import pytesseract
from PySimpleGUI import PySimpleGUI as sg
import cv2

class Window:

    def __init__(self):
        sg.theme('Black')
        layout = [
            [sg.Text('Informe a lingua do currículo', size=(10, 1)), 
            sg.Input(key='lingua', size=(20, 1))],
            [sg.Button('Confirmar')]
        ]

        self.janela = sg.Window('Lingua do currículo', layout)


    def Iniciar(self):
        while True:
            evento, valores = self.janela.read()
            if evento == sg.WINDOW_CLOSED:
                break
            if evento == 'Confirmar':
                lan = self.get_lang(valores)
                self.read_cur(lan)



    def get_lang(self, valores):
        match valores['lingua']: 
            case 'english':
                return 'eng'
            case 'portugues':
                return 'por'
            case 'espanhol':
                return 'spa'
            case _:
                return 'por'
        

    def read_cur(self, lan):
        imagem = cv2.imread("Curriculo.JPG")
            
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
        config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(imagem, lang=lan, config=config) #
        with open('curriculo.txt', 'a', newline='') as arquivo:
            arquivo.write(texto)

            print('Currículo salvo!')

win = Window()
win.Iniciar                                                

#img = cv2.imread('Curriculo.jpg')
#cv2.imshow('img', img)

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('cinza', gray)

#_, bin = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
#cv2.imshow('bin', bin)

#desfoque = cv2.GaussianBlur(bin, (5,5), 0)
#cv2.imshow('des', desfoque)

#TODO: Ver sobre contornos de texto
#_, contornos, hier = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#cv2.drawContours(img, contornos, -1, (0, 255, 0), 2)
#cv2.imshow('cont', img)

"""for c in contornos:

    perimetro = cv2.arcLength(c, True)
    aprox = cv2.approxPolyDP(c, 0.03 * perimetro, True)

    if len(aprox) == 4:
        (x, y, altura, largura) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + altura, y + largura), (0, 255, 0), 2)
        curriculo = img[y:y + largura, x:x + altura]
        cv2.imwrite('currilo2.jpg', curriculo)"""

#cv2.imshow('draw', img)

#cv2.waitKey(0)
#cv2.destroyAllWindows()
