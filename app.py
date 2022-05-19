#!/usr/bin/python 
#-*- coding: utf-8 -*-
from time import sleep
import gtts
from playsound import playsound
import pytesseract
from PySimpleGUI import PySimpleGUI as sg
import cv2
class IotAm:

    # layout da janela
    def __init__(self):
        sg.theme('Topanga')
        layout = [
            [sg.Text('Selecione o CV que deseja ler.', font='21')], # 0
            [sg.Text('Select the CV you want to read.', font='21')], # 1
            [sg.Text('Seleccione el CV que desea leer.', font='21')], # 2
            [sg.Text('Currículo:', font='21', size=(10, 1)), 
            sg.Combo(values=list(["Curriculo_exemplo", "Curriculo_por", "Curriculo_en", "Curriculo_spa"]), key='cv', default_value="Curriculo_exemplo", size=(20, 1))], # 3
            [sg.Text('Selecione a lingua em que o CV está escrito.', font='21')], # 4
            [sg.Text('Select the language in which the CV is written.', font='21')], # 5
            [sg.Text('Seleccione el idioma en el que está escrito el CV.', font='21')], # 6
            [sg.Text('Lingua:', font='21', size=(10, 1)), 
            sg.Combo(values=list(["português", "english", "spanish"]), key='lingua', default_value="português", size=(20, 1))], # 7
            [sg.Text('Você quer ver a imagem renderizada?', font='21')], # 8 
            [sg.Radio('Sim', 'group1'), sg.Radio('Não', 'group1')], # 9
            [sg.Button('Confirmar')] # 10
        ]

        #* Output: {'cv': 'lingua': (0:True 1:False)}
        #? (0: True 1: False) -> esses são os outputs para o Radio.
        
        self.janela = sg.Window('Currículo App', layout)

    # Inicia/Fecha a janela
    def Iniciar(self):
        while True:
            evento, valores = self.janela.read()
            print(valores)
            if evento == sg.WINDOW_CLOSED:
                break
            if evento == 'Confirmar':
                print(valores['lingua'])
                lan = self.get_lang(valores)
                imagem = self.treat_image(valores)
                text = self.read_cur(lan, imagem)
                arq = self.save_cur(text)
                sleep(1)
                self.speak_voice(arq)
                break

    # Pega a lingua escolhida pelo usuario
    def get_lang(self, valores):
        if valores['lingua'].lower() == 'english':
            return 'eng'
        elif valores['lingua'].lower() == 'português':
            return 'por'
        elif valores['lingua'].lower() == 'spanish':
            return 'spa'
    
    # Trata a imagem do curriculo
    def treat_image(self, valores):
        imagem = cv2.imread(f"./assets/{valores['cv']}.jpg", 1)
        img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        imgW = imagem.shape[1]
        imgH = imagem.shape[0]
        if valores['cv'] == "Curriculo_exemplo":
            filtro = cv2.bilateralFilter(img_gray, 43, 45, 200)
            ret, mask = cv2.threshold(filtro, 197, 255, cv2.THRESH_BINARY)
        else: 
            ret, mask = cv2.threshold(img_gray, 56, 255, cv2.THRESH_BINARY)
        mask2 = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 45, 35)
        mask3 = cv2.adaptiveThreshold(mask2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 45, 45)
        print(imagem.shape)
        print(ret)
        proporcao = float(imgH/imgW)
        new_Width = 620
        new_Height = int(new_Width*proporcao)
        new_Image =  cv2.resize(mask3, (new_Width, new_Height), interpolation=cv2.INTER_AREA)
        if valores[0] == True:
            cv2.imshow('Curriculo', new_Image)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return mask3

    # Identifica palavras na imagem tratada
    def read_cur(self, lan, imagem):            
        caminho = r"C:\Program Files\Tesseract-OCR"
        pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"
        config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(imagem, lang=lan, config=config) #
        
        return texto

    # Salva o que achou em um arquivo .txt
    def save_cur(self, text):
        with open('curriculo.txt', 'a', newline='') as arquivo:
                arquivo.write(text)

                print('Currículo salvo!')

        return 'curriculo.txt'

    # Pega a primeira linha do arquivo .txt transforma em um arquivo .mp3 e executa o arquivo .mp3
    def speak_voice(self, arq):
        with open(arq, 'r') as arquivo:
            for linha in arquivo:
                curriculo = gtts.gTTS(linha, lang='pt-br')
                curriculo.save('curriculo.mp3')
                playsound('curriculo.mp3')

iot = IotAm()
iot.Iniciar()

