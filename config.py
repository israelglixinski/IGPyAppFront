
#####* ARQUIVO RESPONSÁVEL POR ARMAZENAR AS CONFIGURAÇÕES



#####* NOME E VERSÃO DO SOFTER
softer_name         = 'IGPyAppFront'
softer_version      = '1.0.0'



#####* CAMINHO DE PASTAS E NOME DE ARQUIVOS
script_front        = 'main'                                                        #* FRONT END
script_back         = 'robo'                                                        #* BACK END
dir_enterprise      = 'c:/Sistemas/Robos/'                                          #* CAMINHO DA PASTA DA EMPRESA
dir_softer          = f'{dir_enterprise}{softer_name}_{softer_version}'             #* CAMINHO DA PASTA DO SOFTER/VERSÃO
path_comunication   = f'{dir_softer}/front_comunication'                            #* ARQUIVO DE COMUNICAÇÃO LOG_BACK/TELA_FRONT
path_alive          = f'{dir_softer}/front_alive'                                   #* VERIFICADOR SE O FRONT ESTÁ VIVO
path_config         = f'{dir_softer}/front_configs'                                 #* ARQUIVO QUE SALVA AS CONGFIGURAÇÕES DO FRONT


