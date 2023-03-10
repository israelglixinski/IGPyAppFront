
#####* ARQUIVO RESPONSÁVEL PELA COMPILAÇAO DE TODO O SOFTERWARE 
#####* E CRIAÇÃO DE UM ARQUIVO INSTALADOR.EXE
#####* 
#####* 
#####* 
#####* ESTE ARQUIVO NÃO É CHAMADO POR NENHUM OUTRO ARQUIVO
#####* MAS PARA SER REALIZADA UMA PUBLICAÇÃO PELO ARQUIVO "pub_new_ver.py"
#####* É NECESSÁRIO ANTES EXECUTAR ESTE ARQUIVO PARA COMPILAR A VERSÃO 
#####* 
#####* 
#####* 
#####* ESTE ARQUIVO CHAMA O ARQUIVO:
#####*     -config.py          >>> Contem os dados da conexão com os servidores e informações de configuração do robô
#####* 
#####* 
#####* 
#####* ESTE ARQUIVO FAZ INTERAÇÕES COM VÁRIOS OUTROS ARQUIVOS DO REPOSITÓRIO
#####* SEM ESTES ESTAREM SENDO CHAMADO DIRETAMENTE AQUI NO CÓDIGO
#####*     Exemplos:
#####*         - main.py 
#####*         - robo.py
#####*         - base.zip
#####*         - favicon.ico
#####*         - msedgedriver.exe
#####*         - atalho.lnk 
#####* 
#####* 
#####* 
#####* ESTE ARQUIVO FAZ INTERAÇÕES DIRETAS COM PASTAS DENTRO E FORA DESTE REPOSITÓRIO
#####*     Exemplos:
#####*         - /dist/main
#####*         - /dist/robo
#####*         - c:/Sistemas/Robos/
#####*         - Área de Trabalho
#####* 
#####* 
#####* 



import subprocess   #* UTILIZADO PARA E EXECUÇÃO DO SCRIPT QUE CRIA O ATALHO DO PROGRAMA
import tempfile     #* UTILIZADO PARA E EXECUÇÃO DO SCRIPT QUE CRIA O ATALHO DO PROGRAMA
import pathlib      #* UTILIZADO PARA E EXECUÇÃO DO SCRIPT QUE CRIA O ATALHO DO PROGRAMA
import config       #* CONFGURAÇÕES DO ROBÔ E DADOS DE CONEXÃO COM O BANCO
import shutil       #* UTILIZADO PARA COPIAR, RENOMEAR, TRABALHAR COM ARQUIVOS E PASTAS
import os           #* MANIPULADOR DO SISTEMA OPERACIONAL EM BACK-GROUND



# #####* DELETANDO OS ARQUIVOS RESIDUAIS CRIADOS EM COMPILAÇÕES ANTERIORES
current_path                = os.getcwd()                                                #* PEGA CAMINHO ATUAL DO REPOSITORIO
path_main_script            = f'\\dist\\{config.script_front}'                            #* CAMINHO DA PASTA COMPILADA 'MAIN'
path_robo_script            = f'\\dist\\{config.script_back}'                            #* CAMINHO DA PASTA COMPILADA 'ROBO'
cmd_del_main_script         = f'rmdir {current_path}{path_main_script} /s/q'             #* COMANDO PARA DELETE DA PASTA'MAIN'
cmd_del_robo_script         = f'rmdir {current_path}{path_robo_script} /s/q'             #* COMANDO PARA DELETE DA PASTA'ROBO'
cmd_del_baseZip             = f'del base.zip /q'                                         #* COMANDO PARA DELETAR A BASE COMPILADA
cmd_del_shortcut            = f'del {config.softer_name}_{config.softer_version}.lnk /q' #* COMANDO QUE APAGA O ATALHO DO PROGRAMA

os.system(cmd_del_main_script)  #*
os.system(cmd_del_robo_script)  #* EXECUÇÃO DOS COMANDOS PARA DELETAR
os.system(cmd_del_baseZip)      #* CASO OS ARQUIVOS NÃO EXISTAM NÃO TEM PROBLEMA
os.system(cmd_del_shortcut)     #*



#####* COMPILA O SCRIPT PRINCIPAL DO SOFTER
#####* JÁ ADICIONA OS ARQUIVOS DA BRIBLIOTECA CUSTONTKINTER NA COMPILAÇÃO
os.system(f"""pyinstaller --add-data "c:\\users\p560564\\appdata\\roaming\\python\\python37\\site-packages\\customtkinter;customtkinter/" --noconfirm --icon=favicon.ico {config.script_front}.py""")



#####* COMPILA O SCRIPT DA MAQUINA DO ROBO
os.system(f"""pyinstaller --icon=favicon.ico --noconfirm {config.script_back}.py""")



#####* COPIA ARQUIVOS ADICIONAIS DA MAQUINA DO ROBO PARA A PASTA COMPILADA DO SCRIPT PRINCIPAL
shutil.copy2(f'favicon.ico'         ,f'./dist/{config.script_front}/')
shutil.copy2(f'msedgedriver.exe'    ,f'./dist/{config.script_front}/')
os.system(f'xcopy dist\{config.script_back} dist\main /e/h/r/y')



#####* CRIA O ATALHADO QUE SERÁ USADO NO INSTALADOR
def create_shortcut(shortcut_path, target, arguments='', working_dir=''):
    shortcut_path = pathlib.Path(shortcut_path)
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)

    def escape_path(path):
        return str(path).replace('\\', '/')

    def escape_str(str_):
        return str(str_).replace('\\', '\\\\').replace('"', '\\"')

    shortcut_path       = escape_path(shortcut_path)
    target              = escape_path(target)
    working_dir         = escape_path(working_dir)
    arguments           = escape_str(arguments)

    js_content = f'''
        var sh = WScript.CreateObject("WScript.Shell");
        var shortcut = sh.CreateShortcut("{shortcut_path}");
        shortcut.TargetPath = "{target}";
        shortcut.Arguments = "{arguments}";
        shortcut.WorkingDirectory = "{working_dir}";
        shortcut.Save();'''

    fd, path = tempfile.mkstemp('.js')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(js_content)
        subprocess.run([R'wscript.exe', path])
    finally:
        os.unlink(path)
create_shortcut(f'{config.softer_name}_{config.softer_version}.lnk',
f'{config.enterprise_dir}{config.softer_name}_{config.softer_version}/{config.softer_name}_{config.softer_version}.exe')



#####* COPIA O ATALHO PARA A PASTA DO SCRIPT PRINCIPAL COMPILADO
shutil.copy2(f'{config.softer_name}_{config.softer_version}.lnk',f'./dist/{config.script_front}/')



#####* RENOMEIA O EXECUTÁVEL PRINCIPAL
try: os.rename(f'./dist/{config.script_front}/{config.script_front}.exe',f'./dist/{config.script_front}/{config.softer_name}_{config.softer_version}.exe')
except: print('Falha ao tentar renomear o executável principal')



#####* COMPACTA A PASTA DO SCRIPT COMPILADO PRINCIPAL, PARA SER USADO NA COMPILAÇÃO DO SCRIPT DO INSTALADOR
shutil.make_archive('base', 'zip', f'./dist/{config.script_front}')



#####* COMPILANDO O INSTALADOR DE SOFTER
#####* JÁ ADICIONANDO À COMPILAÇÃO O ARQUIVO BASE PARA INSTALAÇÃO E A BIBLIOTECA DO CUSTONTKINTER
os.system(f"""pyinstaller --add-data "c:\\users\p560564\\appdata\\roaming\\python\\python37\\site-packages\\customtkinter;customtkinter/" --add-binary="base.zip;." --onefile installer.py""")



#####* RENOMENADO O INSTALADOR
os.rename('./dist/installer.exe',f'./dist/Instalador_{config.softer_name}_{config.softer_version}.exe')



#####* FINALIZADO


