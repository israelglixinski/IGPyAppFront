
#####* ARQUIVO RESPONSÁVEL PELO FRONT END E INTERAÇÃO COM O USUÁRIO
#####* 
#####* ESTE ARQUIVO É CHAMADO PELO ARQUIVO:
#####*      - main.py       >>> Ponto de partida para a execução do softer
#####* 
#####* 
#####* 
#####* ESTE ARQUIVO CHAMA OS ARQUIVOS:
#####*      - config.py     >>> Informações de cofigurações e conexões de banco de dados
#####* 
#####* 
#####* 



from os import remove, makedirs #* MANIPULA SISTEMA OPERACIONAL EM BACK-GROUND
from datetime import datetime   #* MANIPULAÇÃO DE DATA E HORA
from threading import Thread    #* EXECUÇÃO DE THREADS - MULTIPLAS EXECUÇÕES SIMUTANEAS
import customtkinter            #* CRIADOR DE JANELAS PERSONALIZADAS
import tkinter                  #* CRIADOR DE JANELAS
import config                   #* INFORMAÇÕES DE CONFIGURAÇÃO



class front:
    '''Classe principal para criação e gerenciamento da tela'''
    
    def __init__(self):
        '''Inicializador'''

        self.prepare_files()                                                                    #* PREPARA O ARQUIVO QUE O BACKEND COLOCARÁ AS MENSAGENS

        self.cont_linhas = 1                                                                    #* CONTADOR DE LINHAS DO ARQUIVO DE COMUNICAÇÃO COM O BACKEND
        self.app_win     = customtkinter.CTk()                                                  #* INSTANCIAÇÃO DA JANELA
        self.config_get_defnition()                                                             #* DEFINE AS CONFIGURAÇÕES DO FRONT END                                                                   
        self.app_win.geometry("800x600")                                                        #* TAMANHO DA JANELA
        self.app_win.title(F'{config.softer_name} {config.softer_version}')                     #* TITULO DA JANELA
        self.app_win.iconbitmap('icon.ico')                                                     #* DEFINE O ICONE DA JANELA

        self.top()                                                                              #* CRIA A PARTE DE CIMA DA JANELA

        ##### * CRIA MAIS UM FRAME SOMENTE PARA A ORGANIZAÇÃO DA TELA
        ##### * NESTE FRAME QUE FICARÃO OS ELEMENTOS DAS FUNÇÕES "LEFT" E "RIGHT"
        self.frame_midle = customtkinter.CTkFrame(master=self.app_win)
        self.frame_midle.pack(padx=5, pady=5, fill='both', expand=True, side=tkinter.TOP)

        # self.left()                                                                           #* CRIA A PARTE ESQUERDA DA JANELA
        self.right()                                                                            #* CRIA A PARTE DIREITA DA JANELA
        self.down()                                                                             #* CRIA A PARTE DE BAIXO DA JANELA
        
        Thread(target=self.periodic_call).start()                                               #* VERIFICADOR CONTINUO DE MENSAGENS NA MEMÓRIA E NO ARQUIVO 
        self.app_win.mainloop()                                                                 #* INICIALIZA A JANELA
        pass

    ##### * ########################################################################################
    ##### * ########################################################################################
    ##### * FUNÇÕES BACKEND DO GUI
    ##### * ########################################################################################
    ##### * ########################################################################################
    
    def prepare_files(self):
        """Faz a preparação dos arquivos e pastas que serão usados pelo programa"""

        try:    makedirs(f'{config.dir_softer}')                                                #* SE CERTIFICA QUE REALMENTE VAI EXISTIR A PASTA DO SOFTER
        except: pass                                                                            #* CASO JÁ EXISTA SOMENTE SEGUE ADIANTE        
        
        try:    remove(config.path_comunication)                                                #* REMOVE O ARQUIVO DE COMUNICAÇÃO ANTERIOR CASO EXISTA
        except: pass                                                                            #* CASO NÃO EXISTA APENAS SEGUE ADIANTE
        with open(config.path_comunication,'a') as arquivo: arquivo.write('...')                #* CRIA NOAMENTE O ARQUIVO DE COMUNICAÇÃO COM 1 LINHA

    def periodic_call(self):
        '''
        * Responsavel pela busca de mensagens através do arquivo de comunicação.
        * Já executa os procedimentos determinado para cada tipo de mensagem específico
        * Função recursiva que chama a si mesmo em um loop semi-perpétuo
        '''
        arquivo = open(config.path_comunication,'r')                                            #* ABRE O ARQUIVO DE COMUNICAÇÃO COM O BACKEND        
        leitura_total = arquivo.readlines()                                                     #* JOGA TODAS AS LINHAS EM UMA LISTA
        new_cont_linhas = len(leitura_total)                                                    #* CONTAGEM TOTAL DE LINHAS DO ARQUIVO
        if new_cont_linhas != self.cont_linhas:                                                 #* SE A NOVA CONTAGEM DAS LINHAS DIFERIR DA ANTERIOR
            novas_linhas = leitura_total[self.cont_linhas:]                                     #* PEGA AS NOVAS LINHAS ADICIONADA AO ARQUIVO
            for linha in novas_linhas:                                                          #* E PARA CADA LINHA NOVA
                try:                                                                            #* VERIFICA SE OS SEPARADORES VIERAM CORRETOS
                    itens_linha     = linha.split('*%@%*')                                      #* FAZ O SPLIT NO SEPARADOR
                    mark_dtm        = itens_linha[0]                                            #* MARCADOR DE DATA E HORA
                    texto           = itens_linha[1]                                            #* TEXTO DA MENSAGEM ENVIADA
                    vida            = itens_linha[2]                                            #* TEMPO DE VIDA DA MENSAGEM
                    cor             = itens_linha[3]                                            #* COR DA MENSAGEM
                    comando         = itens_linha[4]                                            #* COMANDO PARA SER EXECUTADO NO FRONT
                    if texto != '':                                                             #* CASO VENHA ALGO NO CAMPO DE TEXTO
                        ##### *  CASO VENHA ALGO NO CAMPO DE COR, INSERE NA CAIXA DE TEXTO DA TELA COM A COR
                        if cor != '':   self.feed_back_box.insert(tkinter.END,f'{mark_dtm} - {texto}\n',cor)
                        #* CASO NÃO VENHA NADA NO CAMPO DE COR, APENAS INSERE O TEXTO NA CAIXA DE TEXTO
                        else:           self.feed_back_box.insert(tkinter.END,f'{mark_dtm} - {texto}\n')
                        self.feed_back_box.see("end")                                           #* COLOCANDO O FOCO PARA O FINAL
                    if comando != '':                                                           #* CASO VENHA ALGUM COMANDO NA MENSAGEM
                        if comando.find('progress') != -1:                                      #* VERIFICA SE O COMANDO É REFERENTE À BARRA DE PROGRESSO
                            self.set_progress_bar(comando)                                      #* EM CASO POSITIVO EXECUTA A FUNÇÃO RESPONSÁVEL
                        if comando == 'enable':                                                 #* VERIFICA SE O COMANDO É HABILITAR OS ELEMENTOS DA TELA
                            self.enable_front_elements()                                        #* EM CASO POSITIVO EXECUTA A FUNÇÃO RESPONSÁVEL
                        if comando == 'disable':                                                #* VERIFICA SE O COMANDO É DESABILITAR OS ELEMENTOS DA TELA
                            self.disable_front_elements()                                       #* EM CASO POSITIVO EXECUTA A FUNÇÃO RESPONSÁVEL
                except:pass                                                                     #* CASO OS SEPARADORES NÃO ESTEJAM CORRETOS NÃO FAZ NADA
            self.cont_linhas = new_cont_linhas                                                  #* ENTÃO O NOVO NUMERO DE LINHA É SALVO
        arquivo.close()                                                                         #* E POR FIM É FECHADO O ARQUIVO DE COMUNICAÇÃO COM O FEEDBACK

        ##### * REESCREVE O ARQUIVO 'ALIVE' PARA MOSTRAR QUE A MAQUINA DO FRONT-END CONTINUA VIVA
        with open(config.path_alive,'w') as frnt_aliv: frnt_aliv.write(' ')
        ##### * DEFINE A PROXIMA CHAMADA RECURSIVA DA FUNÇÃO
        self.app_win.after(100,self.periodic_call) 
        pass

    def set_progress_bar(self,comando):
        '''Define o valor na progress bar que aparece na tela do front end'''
        comando_clean       = str(comando).replace('progress(','').replace(')','')              #* REMOVE CARACTERES QUE NÃO SERÃO USADOS
        list_info_progress  = comando_clean.split('/')                                          #* DIVIDE OS VALORES EM QUE SERÃO USADOS EM LISTA
        update              = int(list_info_progress[0])                                        #* VALOR ATUAL DO PROGRESSO/ANDAMENTO DO TRABALHO REALIZADO
        total               = int(list_info_progress[1])                                        #* A QUANTIDADE TOTAL DOS ITEM QUE SERÃO TRABALHADOS 
        valor_unitario  = 1/total                                                               #* PREPARAÇÃO DOS VALORES
        valor_atual     = valor_unitario*update                                                 #* PARA CONFIGURAR A BARRA DE PROGRESSO
        self.progressbar_down.set(valor_atual)                                                  #* DEFINDO A CONFIGURAÇÃO NA BARRA DE PROGRESSO
        pass

    def enable_front_elements(self):
        '''Habilita os elementos do front end, para haver interação do usuário'''
        ##### * EXECUTA O COMANDO EM TRY, PARA CASO OCORRA ALGUMA FALHA, AINDA ASSIM
        ##### * É DADO CONTINUIDADE SEM UM COLAPSO TOTAL DO FRONT
        try: self.top_btn_1.configure(state='normal')
        except: pass                                 
        try: self.top_btn_2.configure(state='normal')
        except: pass                                 

    def disable_front_elements(self):
        '''Desabilita os elementos do front end, para não haver interação do usuário'''
        ##### * EXECUTA O COMANDO EM TRY, PARA CASO OCORRA ALGUMA FALHA, AINDA ASSIM
        ##### * É DADO CONTINUIDADE SEM UM COLAPSO TOTAL DO FRONT
        try: self.top_btn_1.configure(state='disabled')
        except: pass
        try: self.top_btn_2.configure(state='disabled')
        except: pass
        pass

    def exec_iniciar(self):
        '''Executa o botão iniciar'''
        self.feed_back_box.insert(tkinter.END,f'...\n')
        pass

    ##### * ########################################################################################
    ##### * ########################################################################################
    ##### * FUNÇÕES E DEFINIÇÕES DAS CONFIGURAÇÕES
    ##### * ########################################################################################
    ##### * ########################################################################################

    def config_get_defnition(self):
        '''
        * Carrega as definições padrão
        * Verifica se já existe um arquivo de configuração
        * Caso exista, atualiza as configurações por ele
        * Caso não exista arquivo de config já o cria
        '''
        ############################################################
        ##### * PARTE DE RECUPERAÇÃO E DEFINIÇÃO DAS CONFIGURAÇÕES
        ############################################################
        self.config_set_defaut()                                                                #* CARREGA AS VARIAVEIS DE CONFIG COM O PADRÃO
        try:                                                                                    #* TENTA LOCALIZAR ARQUIVO DE CONFIGURAÇÃO
            arquivo = open (f'{config.path_config}','r')                                                      
            leitura = (str(arquivo.read()).replace(' ','')).split('\n')                         #* RETINA OS ESPAÇOS EM BRANCO
            for linha in leitura:                                                               #* VERIFICA LINHA À LINHA SE EXISTE ALGUMA CONFIGURAÇÃO
                linha = linha.split('=')                                                        #* SPLITA A LINHA COM '='
                try:                                                                            #* TENTA PEGAR A CHAVE E O VALOR
                    chave = linha[0]                                                            #* CHAVE É O QUE VEM ANTES DO '='
                    valor = linha[1]                                                            #* VALOR É OQUE VEM DEPOIS DO '='
                except:
                    chave = 'erro'                                                              #* CASO NÃO CONSI OBTER A CHAVE E O VALOR
                    valor = 'erro'                                                              #* DEFINE AMBOS COMO 'erro'
                ##### * ABAIXO FICA AS DEFINIÇÕES
                ##### * DAS OPÇÕES DE CONFIGURAÇÕES DESEJADAS   
                if chave == 'win_theme': self.win_theme.set(valor)                              #* DEFINE A COR DO THEMA
                if chave == 'win_color': self.win_color.set(valor)                              #* DEFINE A COR DOS ELEMENTOS 
            arquivo.close()                                                                     #* FECHA ARQUIVO CONFIGURADOR
        except: self.config_save()                                                              #* CASO O ARQUIVO DE CONFIG AINDA NÃO EXISTA, CRIA UM.

        ############################################################
        ##### * PARTE ONTE AS COFIGURAÇÕES DEFINIDAS SÃO APLICADAS
        ############################################################
        customtkinter.set_appearance_mode     (self.win_theme.get())                            #* APLICA AS CONFIGURAÇÃO DO THEMA
        customtkinter.set_default_color_theme (self.win_color.get())                            #* APLICA A COR DOS ELEMENTOS
        pass

    def config_set_defaut(self):
        '''Definições padrão das configurações'''
        self.win_theme = tkinter.StringVar()                                                    #* INSTANCIA A CONFIGURAÇÃO DO TEMA
        self.win_color = tkinter.StringVar()                                                    #* INSTANCIA A CONFIGURAÇÃO DE COR
        self.win_theme.set('Dark')                                                              #* DEFINE A CONFIGURAÇÃO DO TEMA
        self.win_color.set('blue')                                                              #* DEFINE A CONFIGURAÇÃO DA COR

    def config_save(self):
        '''Salva as configurações no arquivo de configuração'''
        arquivo = open (f'{config.path_config}','w')                                            #* ABRE O ARQUIVO DE CONFGURAÇÃO
        print(f'win_theme = {self.win_theme.get()}',file=arquivo)                               #* SALVA A CONFIGURAÇÃO DO TEMA
        print(f'win_color = {self.win_color.get()}',file=arquivo)                               #* SALVA A CONFIGURAÇÃO DA COR
        arquivo.close()                                                                         #* FECHA O ARQUIVO DE CONFIGURAÇÃO
        pass

    def config_window(self):
        '''Cria a janela modal de configurações'''

        self.win_config = customtkinter.CTkToplevel()                                           #* CRIA A JANELA MODAL DE CONFIGURAÇÃO
        self.win_config.geometry("360x160")                                                     #* DEFINE O TAMANHO DA JANELA
        self.win_config.title("Configurações")                                                  #* DEFINE O TITULO DA JANELA
        self.win_config.iconbitmap('icon.ico')                                                  #* DEFINE O ICONE DA JANELA
        self.win_config.protocol("WM_DELETE_WINDOW", self.config_close_window)                  #* DEFINE O PROTOCOLO DE FECHAMENTO DA JANELA

        self.cfg_frame_visual = customtkinter.CTkFrame(master=self.win_config, height=40)       #* CRIA O FRAME QUE RECEBERA OS ELEMENTOS 
        self.cfg_frame_visual.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)               #* E INVOCA O FRAME

        ##### * CRIA OS ELEMENTOS DE CONFIGURAÇÃO DE TEMA
        self.cfg_label_theme = customtkinter.CTkLabel      (master=self.cfg_frame_visual,text='Tema:')
        self.cfg_swtch_darkm = customtkinter.CTkRadioButton(master=self.cfg_frame_visual,text='Escuro' ,variable=self.win_theme, value='Dark' )
        self.cfg_swtch_light = customtkinter.CTkRadioButton(master=self.cfg_frame_visual,text='Claro'  ,variable=self.win_theme, value='Light')
        self.cfg_label_theme.grid(row=0, column=0,pady=10,padx=40, sticky="e")                  #*
        self.cfg_swtch_darkm.grid(row=0, column=1,pady=10,padx= 0, sticky="e")                  #* INVOCA OS ELEMENTOS DE CONFIGURAÇÃO DE TEMA
        self.cfg_swtch_light.grid(row=0, column=2,pady=10,padx= 0, sticky="e")                  #*

        ##### * CRIA OS ELEMENTOS DE CONFIGURAÇÃO DE COR
        self.cfg_label_color  = customtkinter.CTkLabel      (master=self.cfg_frame_visual,text='Cor:')
        self.cfg_swtch_bluec  = customtkinter.CTkRadioButton(master=self.cfg_frame_visual,text='Azul'  ,variable=self.win_color, value='blue' )
        self.cfg_swtch_green  = customtkinter.CTkRadioButton(master=self.cfg_frame_visual,text='Verde' ,variable=self.win_color, value='green')
        self.cfg_label_color .grid(row=1, column=0,pady=10,padx=40, sticky="e")                 #*
        self.cfg_swtch_bluec .grid(row=1, column=1,pady=10,padx= 0, sticky="e")                 #* INVOCA OS ELEMENTOS DE CONFIGURAÇÃO DE COR
        self.cfg_swtch_green .grid(row=1, column=2,pady=10,padx= 0, sticky="e")                 #*

        self.cfg_frame_obsrv = customtkinter.CTkFrame(master=self.win_config, height=40)        #* CRIA O FRAME QUE REBECERÁ A LABEL DE OBS
        self.cfg_frame_obsrv.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)                #* E JÁ INVOCA O FRAME

        ##### * CRIA O LABEL COM A DESCRIÇÃO DA OBSERVAÇÃO E JÁ A INVOCA
        txt_obs = 'OBS: Para alterar a cor dos botões \né necessário reiniciar o programa'
        self.cfg_label_obsrv = customtkinter.CTkLabel      (master=self.cfg_frame_obsrv,text=txt_obs)
        self.cfg_label_obsrv.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)

        self.win_config.grab_set()                                                              #* CONGELA A JANELA PRINCIPAL ATÉ O MODAL SER FECHADO
        pass

    def config_close_window(self):
        '''Protocolo de fechamento da janela modal de configuração'''
        self.config_save()                                                                      #* SALVA AS CONFIGURAÇÕES NO ARQUIVO
        self.config_get_defnition()                                                             #* APLICA AS NOVAS CONFIGURAÇÕES
        self.win_config.destroy()                                                               #* DESTROE A JANELA DO MODAL
        pass

    ##### * ########################################################################################
    ##### * ########################################################################################
    ##### * CONSTRUTORES DOS ELEMENTOS FRONT END
    ##### * ########################################################################################
    ##### * ########################################################################################

    def top(self):
        '''Criação da parte de cima da janela'''

        ##### * CRIA E COLOCA O PRIMEIRO FRAME QUE RECEBERÁ OS ELEMENTOS
        self.frame_top= customtkinter.CTkFrame(master=self.app_win, height=40)
        self.frame_top.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)

        ##### * BOTÃO INICIAR
        self.top_btn_1= customtkinter.CTkButton(master=self.frame_top, text='Iniciar'       ,command=self.exec_iniciar)
        self.top_btn_1.grid(row=0, column=0, pady=(10, 10), padx=20, sticky="n")
        
        ##### * BOTÃO CONFIGURAÇÕES
        self.top_btn_2= customtkinter.CTkButton(master=self.frame_top, text='Configurações' ,command=self.config_window)
        self.top_btn_2.grid(row=0, column=1, pady=(10, 10), padx=20, sticky="n")

    def left(self):
        '''Criação do menu lateral da janela'''

        ##### * CRIA E COLOCA O FRAME RESPONSÃO POR RECEBER OS ELEMENTOS
        self.frame_left = customtkinter.CTkFrame(master=self.frame_midle)
        self.frame_left.pack(padx=5, pady=5, fill='both', side=tkinter.LEFT)

        ##### * CRIA E COLOCA UMA LABEL PARA DESCRIÇÃO
        self.left_labe_l = customtkinter.CTkLabel(self.frame_left, text="Description:")
        self.left_labe_l.pack(padx=5,pady=5)
        
        ##### * CRIA E COLOCA UMA CAIXA DE ENTRADA
        self.left_entry_1 = customtkinter.CTkEntry(master=self.frame_left, placeholder_text="Write Me")
        self.left_entry_1.pack(pady=5, padx=5)

        ##### * CRIA E COLOCA O PRIMEIRO BOTÃO
        self.left_btn_1 = customtkinter.CTkButton(master=self.frame_left,text='Action 1',command=self.exec_left_btn_1)
        self.left_btn_1.pack(padx=5,pady=5)

        ##### * CRIA E COLOCA O SEGUNDO BOTÃO
        self.left_btn_2 = customtkinter.CTkButton(master=self.frame_left,text='Action 2',command=self.exec_left_btn_1)
        self.left_btn_2.pack(padx=5,pady=5)

    def right(self):
        '''Criação da parte esquerda da janela'''

        ##### * CRIAÇÃO E COLOCAÇÃO DO FRAME QUE RECEBERÁ A CAIXA DE TEXTO
        self.frame_right = customtkinter.CTkFrame(master=self.frame_midle)
        self.frame_right.pack(padx=5, pady=5, fill='both', side=tkinter.LEFT, expand=True)

        ##### * CRIAÇÃO E COLOCAÇAO DA CAIXA DE TEXTO NO FRAME
        self.feed_back_box = customtkinter.CTkTextbox(master=self.frame_right)
        self.feed_back_box.pack(fill='both', expand=True)

        self.feed_back_box.tag_config('RED'   ,foreground='#FF0000')
        self.feed_back_box.tag_config('GREEN' ,foreground='#006400')
        self.feed_back_box.tag_config('ORANGE',foreground='#FF8C00')
        self.feed_back_box.tag_config('PURPLE',foreground='#A020F0')
        self.feed_back_box.tag_config('INDIGO',foreground='#4B0082')
        self.feed_back_box.tag_config('BROWN' ,foreground='#8B4513')
        self.feed_back_box.tag_config('TOMATO',foreground='#FF6347')
        self.feed_back_box.tag_config('BLUE'  ,foreground='#4169e1')

    def down(self):
        '''Criação da parte de baixo da janela'''

        ##### * CRIAÇÃO E COLOCAÇÃO DO FRAME QUE REBERÁ A BARRA DE PROGRESSO
        self.frame_down = customtkinter.CTkFrame(master=self.app_win, height=20)
        self.frame_down.pack(padx=5, pady=5, fill='both', side=tkinter.TOP)        
        
        ##### * CRIAÇÃO E COLOCAÇÃO DA BARRA DE PROGRESSO NO FRAME
        self.progressbar_down = customtkinter.CTkProgressBar(self.frame_down)
        self.progressbar_down.pack(fill='both')        
        self.progressbar_down.set(1) #* A BARRA INICIALMENTE É DEFINIDA COMO CHEIA, APENAS POR QUESTÃO DE ESTÉTICA 
        

