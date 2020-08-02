import PySimpleGUI as sg
import s3fs
import numpy as np
import datetime
import os
import shutil

class TelaPython:
    def __init__(self):
        # Layout
        layout = [
            [sg.Text('Hora inicio', size=(5, 0)), sg.Input(size=(15, 0), key='horai')],
            [sg.Text('Hora fim', size=(5, 0)), sg.Input(size=(15, 0), key='horaf')],
            [sg.Text('Ano',  size=(5, 0)), sg.Input(size=(15, 0), key='ano')],
            [sg.Text('Mes',  size=(5, 0)), sg.Input(size=(15, 0), key='mes')],
            [sg.Text('Dia',  size=(5, 0)), sg.Input(size=(15, 0), key='dia')],
            [sg.Button('Ok'), sg.Button('Cancelar')],


        ]
        # Janela
        while True:
            janela = sg.Window("Extrator de dados").layout(layout)
            # Extrair dados da tela
            self.button, self.values = janela.Read()
            try:
                if self.button == sg.WIN_CLOSED or self.button == 'Cancelar':  # if user closes window or clicks cancel
                    break
                hora_s = int(self.values['horai'])
                hora_f = int(self.values['horaf'])
                hour = range(hora_s, hora_f, 1)
                year = int(self.values['ano'])
                month = int(self.values['mes'])
                day = int(self.values['dia'])
                if hora_s > 24 or hora_f > 24 or hora_s > hora_f:
                    raise ValueError
                if year < 2010 or year > 2020:
                    raise ValueError
                if month > 12:
                    raise ValueError
                if day > 31:
                    raise ValueError

                today = datetime.datetime(year, month, day, 00, 00)
                day_in_year = (today - datetime.datetime(year, 1, 1)).days + 1
                print(day_in_year)

            except ValueError:
                # O usuário digitou de forma errada os dados, permanece no loop
                print("O valor digitado está incorreto, por favor tente novamente.")


            else:
                # O usuário digitou de forma correta as datas e horas, sendo assim sai do loop
                break
        janela.Close()

        # hour = 00
        # Use the anonymous credentials to access public data
        fs = s3fs.S3FileSystem(anon=True)

        # List contents of GOES-16 bucket.
        fs.ls('s3://noaa-goes16/')

        for t in hour:

            print(t)
            if t < 10:

                files = np.array(fs.ls('noaa-goes16/GLM-L2-LCFA/{0}/{1:03d}/{2:02d}/'.format(year, day_in_year, t)))

                print(files)
                length = len(files)  # Getting the number of .nc files
                print(length)
                for i in range(0, length):
                    fs.get(files[i],
                            files[i].split('/')[-1])  # Writting all those .nc files in the directory of your script

                print('End of minus 10')
            else:
                files = np.array(fs.ls('noaa-goes16/GLM-L2-LCFA/{0}/{1:03d}/{2:02d}/'.format(year, day_in_year, t)))
                print(files)
                length = len(files)  # Getting the number of .nc files
                print(length)
                for i in range(0, length):
                    fs.get(files[i],
                            files[i].split('/')[-1])  # Writting all those .nc files in the directory of your script

                print('End over 10')

        self.criarPasta('C:\\Projct\\{0:02d}-{1:02d}-{2} T {3}h00m # {4}h00m'.format(day, month, year, hora_s, hora_f))
        self.mover('C:\\Projct\\{0:02d}-{1:02d}-{2} T {3}h00m # {4}h00m'.format(day, month, year, hora_s, hora_f))
        # self.size('C:\\goes16\\{0:02d}-{1:02d}-{2} T {3}h00m # {4}h00m'.format(self.values['dia'], self.values['mes'], self.values['ano'], self.values['horai'], self.values['horaf']))  # Duas barras fazem diferença


    def Iniciar(self):
        horainicio = self.values['horai']
        horafim = self.values['horaf']
        ano = self.values['ano']
        mes = self.values['mes']
        dia = self.values['dia']
        print(f'hora de inicio: {horainicio}-{horafim}')
        print(f'hora de inicio: {ano}')
        print(f'hora de inicio: {mes}')
        print(f'hora de inicio: {dia}')


    #
    # Cria uma pasta com a data informada
    #
    def criarPasta(self, data):
        try:
            if not os.path.exists(data):
                os.makedirs(data)
        except OSError:
            print("Erro ao criar o diretório, " + data)


    #
    # Move os arquivos baixados para uma pasta
    #
    def mover(self, data):
        caminho_fonte = os.getcwd()
        caminho_destino = data
        lista_arquivos_fonte = os.listdir(caminho_fonte)

        for file in lista_arquivos_fonte:
            if file.endswith('.nc'):
                shutil.move(os.path.join(caminho_fonte, file), os.path.join(caminho_destino, file))

    #
    # Mostra o tamanho total do arquivo
    #

    #def size(self, data):
        # Inicializa a variável que vai armazenar o tamanho total da pasta
    #    tamanho_total = 0

    #    # Usando o método walk() para navegar entre os diretórios
    #    for dirpath, dirnames, filenames in os.walk(data):
    #        for i in filenames:
    #            # O .join é para concatenação de todos componentes da pasta
    #            f = os.path.join(dirpath, i)
    #            # Usar o getsize para pegar o tamanho em bytes e ir salvando o valor acumulado

     #           tamanho_total += os.path.getsize(f)
     #   return tamanho_total

    #print('{0:0.5f} GB'.format(size() / 1073741824))


tela = TelaPython()
tela.Iniciar()
tela.criarPasta()
tela.mover()


