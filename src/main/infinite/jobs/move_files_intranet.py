"""
   Package infinite.jobs
   Module  move_files_intranet.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import glob
import shutil
import time
import logging
from datetime import date

# Libs/Frameworks modules
# Own/Project modules
from infinite.conf import app_config


# ----------------------------------------------------------------------------
# VARIAVEIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES
# ----------------------------------------------------------------------------

# gera o nome do arquivo de controle para indicar status do job:
def arquivo_controle(data: date) -> str:
    # aplica a mascara na data fornecida, configurada no INI,
    ctrl_file_name = data.strftime(app_config.MI_ctrl_file_mask)

    # e identifica o path onde sera salvo:
    ctrl_file_name = os.path.join(app_config.RT_tmp_path, ctrl_file_name)

    return ctrl_file_name


# verifica se o computador esta conectado na rede interna e esta ok para copias:
def intranet_online(dir_shared: str) -> bool:
    logger.debug("Verificando conexao com intranet acessando pasta compartilhada '%s'.", dir_shared)
    try:
        # efetua operacoes na pasta compartilhada para verificar se possui acesso:
        file_intranet_ok = os.path.join(dir_shared, '.move_files_ok')

        # cria um arquivo na pasta compartilhada, lista os arquivos e remove o arquivo...
        open(file_intranet_ok, 'a').close()
        time.sleep(5)  # aguarda 5 segundos para efetivar as permissoes e/ou conexao...
        os.listdir(dir_shared)
        time.sleep(5)  # aguarda 5 segundos para efetivar as permissoes e/ou conexao...
        os.remove(file_intranet_ok)

        return True

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel acessar o diretorio compartilhado '%s'. ERRO: %s",
                     dir_shared, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel acessar o diretorio compartilhado '%s'. ERRO: %s",
                     dir_shared, repr(ex))

    return False


# assegura que existe diretorio destino antes da copia:
def assert_path(path_dir: str) -> bool:
    try:
        # se o diretorio existe, entao nada a fazer aqui...
        if os.path.exists(path_dir):
            logger.debug("O diretorio '%s' ja existe e nao precisa ser criado.", path_dir)
            return True

        # se o path nao existir, entao cria o diretorio neste momento:
        os.makedirs(path_dir)
        logger.debug("O diretorio '%s' nao existia mas foi criado.", path_dir)

        # informa que o path agora existe:
        return True

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel acessar/criar o diretorio compartilhado '%s'. ERRO: %s",
                     path_dir, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel acessar/criar o diretorio compartilhado '%s'. ERRO: %s",
                     path_dir, repr(ex))

    # diretorio nao existe e nao foi possivel criar neste momento...
    return False


# relaciona todos os arquivos em um diretorio:
def get_dir_contents(path_dir: str, mask_files: str) -> (list[str], int):
    try:
        # utiliza mascara generica para abranger todos os arquivos no diretorio:
        source_path_files = os.path.join(path_dir, mask_files)

        dir_contents = glob.glob(source_path_files)
        len_dir_contents = len(dir_contents)
        if len_dir_contents > 0:
            logger.debug("Encontrado(s) %d arquivo(s) em '%s'.", len_dir_contents, path_dir)
        else:
            logger.debug("Nenhum arquivo encontrado em '%s'.", path_dir)

        return dir_contents, len_dir_contents

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel ler o diretorio '%s'. ERRO: %s", path_dir, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel ler o diretorio '%s'. ERRO: %s", path_dir, repr(ex))

    # se nao conseguiu ler o diretorio, retorna 'vazio'...
    return [], 0


# realiza copia de arquivos na pasta de origem para o path destino indicado:
def copy_source_destiny(src_path: str, dst_path: str, mask_files: str) -> None:
    try:
        # busca todos os arquivos na pasta de origem:
        dir_contents, len_dir_contents = get_dir_contents(src_path, mask_files)

        # assegura que existam arquivos na origem e o diretorio destino esteja criado:
        if (len_dir_contents > 0) and assert_path(dst_path):
            # copia cada arquivo na pasta origem para a pasta destino:
            logger.debug("Copiando arquivos em '%s' para '%s'.", src_path, dst_path)
            for src_file in dir_contents:
                dst_file = os.path.join(dst_path, os.path.basename(src_file))
                shutil.copyfile(src_file, dst_file)

            logger.debug("Arquivos em '%s' copiados com sucesso para '%s'.", src_path, dst_path)
        else:
            logger.debug("Nenhum arquivo encontrado em '%s' a ser copiado para '%s'.",
                         src_path, dst_path)

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel copiar arquivos em '%s' para '%s'. ERRO: %s",
                     src_path, dst_path, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel copiar arquivos em '%s' para '%s'. ERRO: %s",
                     src_path, dst_path, repr(ex))


# realiza transferencia de arquivos na pasta de origem para o path destino indicado:
def move_source_destiny(src_path: str, dst_path: str, mask_files: str) -> None:
    try:
        # busca todos os arquivos na pasta de origem:
        dir_contents, len_dir_contents = get_dir_contents(src_path, mask_files)

        # assegura que existam arquivos na origem e o diretorio destino esteja criado:
        if (len_dir_contents > 0) and assert_path(dst_path):
            # move cada arquivo na pasta origem para a pasta destino:
            logger.debug("Movendo arquivos em '%s' para '%s'.", src_path, dst_path)
            for src_file in dir_contents:
                dst_file = os.path.join(dst_path, os.path.basename(src_file))
                shutil.move(src_file, dst_file)

            logger.debug("Arquivos em '%s' movidos com sucesso para '%s'.", src_path, dst_path)
        else:
            logger.debug("Nenhum arquivo encontrado em '%s' a ser movido para '%s'.",
                         src_path, dst_path)

    # qualquer erro significa que ainda nao pode acessar a rede interna...
    except OSError as err:
        logger.error("Nao foi possivel mover arquivos em '%s' para '%s'. ERRO: %s",
                     src_path, dst_path, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel mover arquivos em '%s' para '%s'. ERRO: %s",
                     src_path, dst_path, repr(ex))


# tag de identificacao do job, para agendamento e cancelamento:
def job_id() -> str:
    return "MOVE_INTRANET"


# obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler:
def job_interval() -> int:
    interval = app_config.MI_job_interval
    return interval


# job para copiar/mover arquivos para outra estacao:
def run_job(callback_func=None):
    logger.info("Iniciando job '%s' para copiar/mover arquivos para outra estacao.", job_id())

    # o processamento eh feito conforme a data atual:
    hoje = date.today()
    logger.debug("Processando copia/transferencia de arquivos para a data '%s'", hoje)

    # gera o nome do arquivo de controle para a data de hoje.
    ctrl_file_job = arquivo_controle(hoje)
    logger.debug("Arquivo de controle a ser verificado hoje: %s", ctrl_file_job)

    # se ja existe arquivo de controle para hoje, entao o processamento foi feito antes.
    if os.path.exists(ctrl_file_job):
        # pode cancelar o job porque nao sera mais necessario por hoje.
        logger.warning("O job '%s' ja foi concluido hoje mais cedo e sera cancelado.", job_id())
        if callback_func is not None:
            callback_func(job_id())
        return  # ao cancelar o job, nao sera mais executado novamente.
    else:
        logger.info("Arquivo de controle nao foi localizado. Job ira prosseguir.")

    # verifica se o computador esta conectado na rede interna e esta ok para copias:
    if intranet_online(app_config.MI_shared_folder):
        logger.info("Conexao com rede interna (Intranet) testada e funcionando OK.")
    else:
        # se esta sem acesso, interrompe e tenta novamente na proxima execucao.
        logger.error("Sem conexao com rede interna (Intranet).")
        return  # ao sair do job, sem cancelar, permite executar novamente depois.

    # --- Copia arquivos dos terminais MT5 para outra estacao ----------------------

    # identifica os terminais MT5 instalados na estacao:
    mt5_instances_id = app_config.RT_mt5_instances_id
    if len(mt5_instances_id) == 0:
        logger.error("Nao ha terminais MT5 configurados em INI para processamento.")
        if callback_func is not None:
            callback_func(job_id())
        return  # ao cancelar o job, nao sera mais executado novamente.

    # percorre lista de terminais para processar cada pasta <MQL5\Files>.
    for idt, cia in mt5_instances_id:
        logger.info("Iniciando copia dos arquivos no terminal '%s' da corretora '%s'...",
                    idt, cia.upper())

        # arquivos de origem: faz replace com o id do terminal em cada instancia:
        terminal_logs = app_config.RT_mt5_terminal_logs.replace('%id', idt)
        terminal_mql5_files = app_config.RT_mt5_terminal_mql5_files.replace('%id', idt)
        terminal_mql5_logs = app_config.RT_mt5_terminal_mql5_logs.replace('%id', idt)

        # arquivos de destino: faz replace com o nome da corretora em cada instancia:
        cia_terminal_logs = app_config.MI_cia_terminal_logs.replace('%id', cia)
        cia_mql5_files = app_config.MI_cia_mql5_files.replace('%id', cia)
        cia_mql5_logs = app_config.MI_cia_mql5_logs.replace('%id', cia)

        # realiza copia de arquivos em cada pasta da origem para o respectivo destino:
        copy_source_destiny(terminal_logs, cia_terminal_logs, app_config.RT_files_log_mask)
        move_source_destiny(terminal_mql5_files, cia_mql5_files, app_config.RT_files_zip_mask)
        copy_source_destiny(terminal_mql5_logs, cia_mql5_logs, app_config.RT_files_log_mask)
        logger.debug("Finalizou copia dos arquivos no terminal '%s' da corretora '%s'.",
                     idt, cia.upper())

    # --- Copia arquivos da plataforma MT5 para outra estacao ----------------------

    move_source_destiny(app_config.RT_mt5_platform_crashes, app_config.MI_shared_mt5_crashes,
                        app_config.RT_files_all_mask)
    logger.debug("Finalizou copia dos arquivos de log no MT5 '%s' para outra estacao '%s'.",
                 app_config.RT_mt5_platform_crashes, app_config.MI_shared_mt5_crashes)

    # --- Move arquivos baixados e gerados pelo InFinite para outra estacao ---------------

    move_source_destiny(app_config.RT_www_path, app_config.MI_shared_app_www,
                        app_config.RT_files_all_mask)
    copy_source_destiny(app_config.RT_log_path, app_config.MI_shared_app_logs,
                        app_config.RT_files_all_mask)
    copy_source_destiny(app_config.RT_clock_logs, app_config.MI_shared_app_logs,
                        app_config.RT_files_all_mask)
    logger.debug("Finalizou copia dos arquivos processados pelo InFiniTe para outra estacao.")

    # vai executar este job apenas uma vez, se for finalizado com sucesso:
    logger.info("Finalizado job '%s' para copiar/mover arquivos para outra estacao.", job_id())
    if callback_func is not None:
        callback_func(job_id())

# ----------------------------------------------------------------------------
