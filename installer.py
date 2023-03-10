
##### * ARQUIVO RESPOSÁVEL POR FAZER A INSTALAÇÃO DO SOFTER NA MAQUINA DO USUÁRIO
##### * 
##### * 
##### * 
##### * ESTE ARQUIVO NÃO É CHAMADO POR OUTROS ARQUIVOS
##### * 
##### * 
##### * 
##### * ESTE ARQUIVO CHAMA OS SEGUINTE ARQUIVO:
##### *         - config.py     >>> Variaveis de configuração e informações de banco de dados
##### * 
##### * 
##### * 
##### * ESTE ARQUIVO UTILIZA UM ARQUIVO COM O NOME 'base.zip' 
##### * QUE É CRIADO AO EXECUTAR O ARQUIVO "compiler.py"
##### * 
##### * 
##### * 



from pkg_resources import resource_filename     #* PARA IMBUTIR UM ARQUIVO NA COMPILAÇÃO DO SCRIPT
from datetime import datetime                   #* GERENCIAMENTO DE DATAS
from threading import Thread                    #* GERENCIAMENTOS DE THREADS (MULTI EXECUÇÃO SUMITANEAS)
from time import sleep                          #* TEMPORIZADOR
import customtkinter                            #* BIBLIOTECA DE TELAS PERSONALIZADAS
import subprocess                               #* PARA EXECUÇÃO DE SUBPROCESSOS
import tkinter                                  #* BIBLIOTECAS DE TELA
import psutil                                   #* PARA PEGAR OS PID'S FILHOS
import shutil                                   #* PARA COPIAR/GERENCIAR ARQUIVOS E PASTAS
import config                                   #* OBTER VARIAVEIS DE CONFIGURAÇÃO
import os                                       #* MANIPULAR SISTEMA OPERACIONAL EM BACK-GROUND



##### * CERTIFICA QUE A PASTA PRINCIPAL DE SOFTERS VAI REALMENTE ESTAR CRIADA
try:    os.makedirs(f'{config.enterprise_dir}')
except: pass



##############################################################################
##### * DEFINIÇÃO DAS FUNÇÕES
##############################################################################

##### * DEFINE UMA LISTA LIMPA PARA OS PID'S FILHOS
lista_pids_filhos = []                                                      

def get_pids():
    '''Captura os PID's filhos'''
    global lista_pids_filhos                                        #* DEFINE A LISTA COMO GLOBAL
    pid_principal = os.getpid()                                     #* PEGA O PID PRINCIPAL
    cadeia_de_processos = psutil.Process(pid_principal)             #* PEGA A CADEIA DE PROCESSOS FILHOS
    for processo in cadeia_de_processos.children(recursive=True):   #* PARA CADA PROCESSO NA CADEIA DE PROCESSOS
        if processo.pid not in lista_pids_filhos:                   #* CASO O PID DO PROCESSO AINDA NÃO ESTEJA NA LISTA
            lista_pids_filhos.append(processo.pid)                  #* É ADICIONADO

def reinicializar():
    '''Função que mata todos os processos filhos'''
    global lista_pids_filhos                                        #* DEFINE A LISTA DE PIDS COMO GLOBAL
    cont_pid = 0                                                    #* DEFINE O CONTADOR DE PID COM O INICIO EM 0
    total_pid = len(lista_pids_filhos)                              #* PEGA O TOTAL DE PIDS QUE TEMOS NA LISTA
    for pid in lista_pids_filhos:                                   #* PARA CARA PID NA LISTA DE PIDS FILHOS
        if cont_pid != total_pid:                                   #* SE O CONTADOR DE PID FOR DIFERENTE DO NUMERO TOTAL DE PIDS
            os.system(f'taskkill /pid {str(pid)} /F')               #* MATA O PID
        cont_pid+=1                                                 #* ADICIONA UM NUMERO AO CONTADOR DE PIDS
    lista_pids_filhos   = []                                        #* LIMPA A LISTA DE PID'S FILHOS               

def registrando(texto):
    '''Mostra o registro desejado na tela da janela e salva a mesma mensagem em um log de texto'''
    dtm = datetime.now().strftime('%Y/%m/%d-%H:%M:%S')              #* CRIA UM MARCADOR DE DATA E HORA
    mensagem = f'{dtm} - {texto}'                                   #* JUNTA O TEXTO COM O MARCADOR DE DATA E HORA
    txtbox.insert(tkinter.END,f'{mensagem}\n')                      #* COLOCA A MENSAGEM NA TELA DA JANELA
    ##### * E POR ULTIMO SALVA A MESMA MENSAGEM EM UM ARQUIVO DE TEXTO PARA LOG
    with open (f'{config.enterprise_dir}LOG_Install_{config.softer_name}_{config.softer_version}.txt','a') as arquivo:
        print(mensagem,file=arquivo)
    pass

def remove_olds():
    '''Remove versões anteriores do softer caso seja desejado'''

    ##### * TENTA APAGAR OS ATALHOS DOS SOFTERS ANTERIORES DA AREA DE TRABALHO
    registrando('Procurando atalhos na área de trabalho para apagar...')
    
    username = str(os.getlogin())                                          #* PEGA O NOME DO USUÁRIO 
    try:    path_desk = str(os.environ['ONEDRIVE'])+'\\Área de Trabalho\\' #* TENTA PEGAR O CAMNHO DO ONEDRIVE
    except: path_desk = f'C:/Users/{username}/Desktop/'                    #* SE NÃO DEFINE A CONFIGURAÇÃO PADRÃO
    path_desk2 = f'C:/Users/{username}/Desktop/'                           #* UMA SEGUNDA CONFIGURAÇÃO POR GARANTIA
                                                                            
    try: os.system(f'del "{path_desk}{config.softer_name}_*.lnk"')         #* TENTA EXCLUSÃO NO PRIMEIRO PATH CONFIGURADO
    except: pass                                                           
                                                                            
    try: os.system(f'del "{path_desk2}{config.softer_name}_*.lnk"')        #* TENTA EXCLUSÃO NO SEGUNDO PATH CONFIGURADO
    except: pass                                                            



    # ##### * INICIO DO PROCESSO DE REMOÇÃO DAS PASTAS DE INSTALAÇÃO DOS SOFTERS ANTERIORES
    # path_enterprise_dir = str(config.enterprise_dir).replace('/','\\')                         # * CAMINHO PRINCIPAL DA PASTA DE SOFTERS
    # resp = subprocess.check_output(f"dir {path_enterprise_dir}", shell=True)                # * COMANDO 'DIR' PARA LISTAR TUDO
    # resp_list = str(resp).split('\\n')                                                      # * SEPARA POR LINHA
    # for item in resp_list:                                                                  
    #     if (                                                                                
    #     item.find   ('<DIR>'    )   != -1)      and (                                       
    #     item.find   ('  .\\r'   )   == -1)      and (                                       # * PARA CADA LINHA:
    #     item.find   ('  ..\\r'  )   == -1)      :                                           # * VERIFICA SE É UMA PASTA
    #         dir_name = item.replace('          ','').split('<DIR>')[1].split('\\r')[0]      # * E SE A PASTA POSSUI O NOME DO SOFTER
    #         if dir_name.find(f'{config.softer_name}_')!=-1:                                                                         
    #             os.system(f'rmdir {path_enterprise_dir}{dir_name} /s/q')                    # * EM CASO POSITIVO DELETA A PASTA        
    pass

def make_enterprise_dir():
    '''Cria a pasta que será realizada feita a instalação'''
    try:    
        os.makedirs(f'{config.enterprise_dir}{config.softer_name}_{config.softer_version}')
        registrando('Criado pasta para a instalação')
        return 'ok'
    except: 
        registrando('Erro ao tentar criar a posta para instalação')
        registrando('Caso o problema persista, entre em contato com o desenvolvedor.')
        return 'erro'

def copy_base():
    '''Copia os arquivos contido no arquivo compactado "base.zip" para a pasta de destino da instalação'''
    base = resource_filename(__name__, 'base.zip')
    shutil.unpack_archive(base, f'{config.enterprise_dir}{config.softer_name}_{config.softer_version}')

def copy_desktop_icon():
    '''Copia o atalho contido na pasta de instalação para a area de trabalho'''
    try:
        username = str(os.getlogin())                                                           #* PEGA O NOME DO USUÁROP

        try:    path_desk = str(os.environ['ONEDRIVE'].replace('\\','/'))+'/Área de Trabalho/'  #* TENTA PEGAR O CAMINHO DO ONEDRIVE
        except: path_desk  = f'C:/Users/{username}/Desktop/'                                    #* SE NÃO, DEFINE O CAMINHO ROTINEIRO

        path_desk2 = f'C:/Users/{username}/Desktop/'                                            #* DEFINE UMA SEGUNDA CONFIGURAÇÃO PARA GARANTIA

        ##### * TENTA COPIAR NO PIMEIRO CAMINHO CASO FALHE TENTA CPIAR PARA O SEGUNDO CAMINHO.
        try:    shutil.copy2(f'{config.enterprise_dir}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.lnk',path_desk )
        except: shutil.copy2(f'{config.enterprise_dir}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.lnk',path_desk2)
    except: registrando('Erro ao tentar criar o Atalho')                                        #* CASO NADA FUNCIONE, RETORNA ERRO NA TELA



##############################################################################
##### * INICIO DO SCRIPT DE INSTALAÇÃO E FRONTEND
##############################################################################

janela = customtkinter.CTk()                                                                    #* INSTANCIA UMA JANELA
janela.title(f'Instalador {config.softer_name}, Versão: {config.softer_version}')               #* DEFINE O TITULO DA JANELA
janela.geometry("700x500")                                                                      #* DEFINE O TAMANHO DA JANELA
txtbox = customtkinter.CTkTextbox(master=janela)                                                #* DEFINE UMA CAIXA DE TEXTO PARA FEEDBACK
txtbox.pack(fill='both',expand=True)                                                            #* COLOCA A CAIXA DE TEXTO NA TELA

def install_script():
    '''Função para a rotina de instalação'''

    registrando(f'Iniciando instalação do softer: {config.softer_name}, Versão: {config.softer_version}')
    registrando(f'Removendo versões anteriores do softer: {config.softer_name}')
    remove_olds()                                                                               #* REMOVE VERSÕES ANTERIORES
    if make_enterprise_dir() == 'ok':                                                              #* TENTA CRIAR A PASTA DE INSTALAÇÃO
        copy_base()                                                                             #* EM CASO POSITIVO COPIA OS ARQUIVOS DE INSTALAÇÃO
    copy_desktop_icon()                                                                         #* COPIA O ATALHO PARA A AREA DE TRABALHO
    registrando('Finalizado a instalação')
    sft_name_vers = f'{config.softer_name}_{config.softer_version}'                             #* DEFINE MAIS UMA VEZ O NOME E VERSÃO DO SOFTER 
    destiny = f'c:/Sistemas/Robos/{sft_name_vers}/{sft_name_vers}.exe'                          #* CAMINHO DO EXECUTÁVEL QUE SERÁ ABERTO NO FINAL DA INSTALAÇÃO
    os.popen(destiny)                                                                           #* ABRE O EXECUTÁVEL NO FINAL DA INSTALAÇÃO 
    registrando('Esta janela já pode ser fechada...')
    sleep(5)
    os.system(f'taskkill /im Instalador_{config.softer_name}_{config.softer_version}.exe /f')   #* O INSTALADOR MATA A SI MESMO PARA COLUIR A INSTALAÇÃO

Thread(target=install_script).start()                                                           #* INICIA A INSTALAÇÃO DENTRO DE UMA THREAD

janela.mainloop()                                                                               #* INVOCA A JANELA CRIADA