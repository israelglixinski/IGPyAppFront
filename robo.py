
##### * ARQUIVO DE EXEMPLO PARA COMUNICAÇÃO E MANIPULAÇÃO DO FRONT END 



from datetime import datetime       #* MANIPULADOR DE DATA E HORA
from time import sleep              #* TEMPORIZADOR
import config                       #* VARIÁVEIS DE CONFIGURAÇÃO



def registrando(texto='',vida='SEMANA',cor='',comando=''):
    """
    * Faz o registro de mensagens para o frontend através de um arquivo de comunicação
    * Através da mensagem é possivel enviar diversas informações inclusive comandos
    * Salva um log de backup das ações para registro
    # args:
        * texto     = texto que deseja que seja exibido na tela do frontend
        * vida      = tempo que se deseja que o log seja mantido no banco de dados
        * cor       = cor na qual será exibida a mensagem
        * comando   = para poder manipular o frontend 
    """
    mark_dtm_txt = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))                            #* MARCADOR DE DATA E HORA PARA A MENSAGEM
    mark_dtm_log = str(datetime.now().strftime('%Y%m%d'))                                       #* MARCADOR DE DATA E HORA PARA O LOG
    mensagem = f'{mark_dtm_txt}*%@%*{texto}*%@%*{vida}*%@%*{cor}*%@%*{comando}'                 #* CONTROE O FORMATO QUE FICARÁ A MENSAGEM
    ##### * SALVA A MENSAGEM NO ARQUIVO DE COMUNICAÇÃO COM O FRONT END
    with open(config.path_comunication,'a') as file_comunic: file_comunic.write(f'\n{mensagem}') 
    ##### * SALVA A MENSAGEM EM UM ARQUIVO DE LOG PARA REGISTRO DE AÇÕES
    with open(f'{config.dir_softer}/log_{mark_dtm_log}.txt','a') as file_log: file_log.write(f'\n{mensagem}')
    pass



##### * ABAIXO SEGUE UM EXEMPLO DE ROTINA QUE FAZ COMUNICAÇÃO COM O FRONT END
total = 10                                                                                      #* QUANTIDADE TOTAL DE AÇÕES QUE SERÃO REALIZADAS
for i in range(total):                                                                          #* LAÇO DE EXECUÇÃO DA ROTINA
    i = i+1                                                                                     #* ITEM ATUAL SENDO TRABALHADO
    registrando(i,comando=f'progress({i}/{total})')                                             #* REGISTRO NO FRONT END JUNTO COM A BARRA DE PROGRESSO
    
    ##### * TESTE DE BLOQUEIO DE TELA
    if i == 2:  registrando(comando='disable')

    ##### * TESTE DE ENVIO DE MENSAGEM COM COR
    if i == 3:  registrando('VERMELHO',cor='RED')
    
    ##### * TESTE DE DESBLOQUEIO DE TELA
    if i == 7:  registrando(comando='enable')
    
    
    sleep(1)                                                                                    #* TEMPORIZADOR





