"""
   Package colethon.jobs
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
from datetime import date, timedelta

# Libs/Frameworks modules
# Own/Project modules
from colethon.conf import app_config
from colethon.util.eve import *
from colethon.jobs import commons
from colethon.jobs.abstract_job import AbstractJob


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

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
        logger.error("Nao foi possivel mover arquivos '%s' em '%s' para '%s'. ERRO: %s",
                     mask_files, src_path, dst_path, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel mover arquivos '%s' em '%s' para '%s'. ERRO: %s",
                     mask_files, src_path, dst_path, repr(ex))


# realiza exclusao de arquivo temporario de flag, indicando inicio de processamento do Colethon:
def delete_temp_flag(src_path: str) -> None:
    temp_safe_del = os.path.join(src_path, app_config.MI_temp_safe_del)
    # apaga o arquivo temporario anterior que indica final de processamento do job, se existir:
    if os.path.isfile(temp_safe_del):
        os.remove(temp_safe_del)


# realiza criacao do arquivo temporario de flag, indicando final de processamento do Colethon:
def create_temp_flag(src_path: str) -> None:
    temp_safe_del = os.path.join(src_path, app_config.MI_temp_safe_del)
    # nao precisa criar se ja existir o arquivo:
    if not os.path.exists(temp_safe_del):  # apenas para evitar excecoes eventuais.
        open(temp_safe_del, 'a').close()


# realiza limpeza da pasta de logs, apagando os arquivos mais antigos (do corte pra tras):
def delete_old_logs(src_path: str, mask_files: str, cut_off: int, mask_date: str) -> None:
    try:
        # identifica a data de corte - o processamento eh feito conforme a data atual:
        date_cutoff = date.today() - timedelta(days=cut_off)
        logger.info("Vai apagar todos os arquivos de log em '%s' anteriores a '%s'.",
                    src_path, date_cutoff)

        # busca todos os arquivos de log na pasta de origem, a serem considerados para exclusao:
        dir_contents, len_dir_contents = get_dir_contents(src_path, mask_files)

        # assegura que existam arquivos de log a serem deletados:
        if len_dir_contents == 0:
            # se a pasta estiver vazia, entao nada a fazer aqui.
            logger.info("Nenhum arquivo de log encontrado em '%s' para exclusao.", src_path)
            return

        # percorre a lista de arquivos de log encontrados e verifica se deve excluir:
        del_count = 0
        for log_file in dir_contents:
            # extrai a data do arquivo para verificar se eh anterior ao corte:
            date_log_file = commons.extract_date_file(os.path.basename(log_file), mask_date)
            if date_log_file is not None and date_log_file < date_cutoff:
                # apaga este arquivo mais antigo:
                commons.delete_file(log_file)
                del_count += 1

        if del_count == 0:
            logger.info("Nenhum arquivo de log encontrado em '%s' para exclusao.", src_path)
        elif del_count == 1:
            logger.info("Excluido apenas 1 arquivo de log em '%s'.", src_path)
        else:
            logger.info("Foram excluidos '%d' arquivos de log em '%s'.", del_count, src_path)

    # qualquer erro aborta a operacao e ignora por hoje...
    except OSError as err:
        logger.error("Nao foi possivel apagar arquivos de log em '%s'. ERRO: %s",
                     src_path, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel apagar arquivos de log em '%s'. ERRO: %s",
                     src_path, repr(ex))


# realiza limpeza da pasta temp, apagando os arquivos de controle mais antigos (do corte pra tras):
def delete_old_ctrl(src_path: str, mask_files: str, cut_off: int, mask_date: str) -> None:
    try:
        # identifica a data de corte - o processamento eh feito conforme a data atual:
        date_cutoff = date.today() - timedelta(days=cut_off)
        logger.info("Vai apagar todos os arquivos de controle em '%s' anteriores a '%s'.",
                    src_path, date_cutoff)

        # busca todos os arquivos de controle na pasta temp, a serem considerados para exclusao:
        dir_contents, len_dir_contents = get_dir_contents(src_path, mask_files)

        # assegura que existam arquivos de controle a serem deletados:
        if len_dir_contents == 0:
            # se a pasta estiver vazia, entao nada a fazer aqui.
            logger.info("Nenhum arquivo de controle encontrado em '%s' para exclusao.", src_path)
            return

        # percorre a lista de arquivos de controle encontrados e verifica se deve excluir:
        del_count = 0
        for ctrl_file in dir_contents:
            # extrai a data do arquivo para verificar se eh anterior ao corte:
            ctrl_file_name = os.path.basename(ctrl_file)
            date_log_file = commons.extract_date(ctrl_file_name[1:11], mask_date)
            if date_log_file is not None and date_log_file < date_cutoff:
                # apaga este arquivo mais antigo:
                commons.delete_file(ctrl_file)
                del_count += 1

        if del_count == 0:
            logger.info("Nenhum arquivo de controle encontrado em '%s' para exclusao.", src_path)
        elif del_count == 1:
            logger.info("Excluido apenas 1 arquivo de controle em '%s'.", src_path)
        else:
            logger.info("Foram excluidos '%d' arquivos de controle em '%s'.", del_count, src_path)

    # qualquer erro aborta a operacao e ignora por hoje...
    except OSError as err:
        logger.error("Nao foi possivel apagar arquivos de log em '%s'. ERRO: %s",
                     src_path, repr(err))
    except Exception as ex:
        logger.error("Nao foi possivel apagar arquivos de log em '%s'. ERRO: %s",
                     src_path, repr(ex))


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class MoveFilesIntranet(AbstractJob):
    """
    Implementacao de job para copiar/mover arquivos para outra estacao.
    """

    # --- PROPRIEDADES -----------------------------------------------------

    @property
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Colethon, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "MOVE_INTRANET"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.MI_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        _startWatch = startwatch()
        logger.info("Iniciando job '%s' para copiar/mover arquivos para outra estacao.",
                    self.job_id)

        # o processamento eh feito conforme a data atual:
        hoje = date.today()
        logger.debug("Processando copia/transferencia de arquivos para a data '%s'", hoje)

        # gera o nome do arquivo de controle para a data de hoje.
        ctrl_file_job = commons.arquivo_controle(app_config.MI_ctrl_file_mask)
        logger.debug("Arquivo de controle a ser verificado hoje: %s", ctrl_file_job)

        # se ja existe arquivo de controle para hoje, entao o processamento foi feito antes.
        if os.path.exists(ctrl_file_job):
            # pode cancelar o job porque nao sera mais necessario por hoje.
            logger.warning("O job '%s' ja foi concluido hoje mais cedo e sera cancelado.",
                           self.job_id)
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.
        else:
            logger.info("Arquivo de controle nao foi localizado. Job ira prosseguir.")

        # apaga os arquivos temporarios anteriores que indicam final de processamento do job:
        delete_temp_flag(app_config.MI_local_folder + app_config.MI_lothon_data)
        delete_temp_flag(app_config.MI_local_folder + app_config.MI_quanthon_data)
        delete_temp_flag(app_config.MI_shared_folder + app_config.MI_lothon_data)
        delete_temp_flag(app_config.MI_shared_folder + app_config.MI_quanthon_data)

        # verifica se o computador esta conectado na rede interna e esta ok para copias:
        if intranet_online(app_config.MI_shared_folder):
            logger.info("Conexao com rede interna (Intranet) testada e funcionando OK.")
        else:
            # se esta sem acesso, interrompe e tenta novamente na proxima execucao.
            logger.error("Sem conexao com rede interna (Intranet).")
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # --- Copia/Transferencia de arquivos dos terminais MT5 -------------------------------

        # identifica os terminais MT5 instalados na estacao:
        mt5_instances_id = app_config.RT_mt5_instances_id
        if len(mt5_instances_id) == 0:
            logger.error("Nao ha terminais MT5 configurados em INI para processamento.")
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.

        # percorre lista de terminais para processar cada pasta <MQL5\Files>.
        for idt, cia in mt5_instances_id:
            logger.info("Iniciando copia dos arquivos no terminal '%s' da corretora '%s'...",
                        idt, cia.upper())

            # arquivos de origem: faz replace com o id do terminal em cada instancia:
            terminal_mql5_files = app_config.RT_mt5_terminal_mql5_files.replace('%id', idt)

            # arquivos de destino: faz replace com o nome da corretora em cada instancia:
            quanthon_mql5_files = app_config.MI_quanthon_data_mtrader5.replace('%id', cia)

            # realiza copia/mocao de arquivos em cada pasta da origem para o respectivo destino:
            copy_source_destiny(terminal_mql5_files,
                                app_config.MI_local_folder + quanthon_mql5_files,
                                app_config.RT_files_zip_mask)

            move_source_destiny(terminal_mql5_files,
                                app_config.MI_shared_folder + quanthon_mql5_files,
                                app_config.RT_files_zip_mask)
            logger.debug("Finalizou copia/mocao dos arquivos no terminal '%s' da corretora '%s'.",
                         idt, cia.upper())

        # --- Copia/Transferencia dos arquivos baixados e gerados pelo Colethon ---------------

        # arquivos de loterias da Caixa, contendo os resultados e jogos processados:
        copy_source_destiny(app_config.RT_www_path,
                            app_config.MI_local_folder + app_config.MI_lothon_data_caixa,
                            app_config.LC_loterias_htm_mask)
        copy_source_destiny(app_config.RT_www_path,
                            app_config.MI_local_folder + app_config.MI_lothon_data_cache,
                            app_config.MI_sorteios_csv_mask)
        copy_source_destiny(app_config.RT_www_path,
                            app_config.MI_local_folder + app_config.MI_lothon_data_cache,
                            app_config.MI_jogos_csv_mask)

        move_source_destiny(app_config.RT_www_path,
                            app_config.MI_shared_folder + app_config.MI_lothon_data_caixa,
                            app_config.LC_loterias_htm_mask)
        move_source_destiny(app_config.RT_www_path,
                            app_config.MI_shared_folder + app_config.MI_lothon_data_cache,
                            app_config.MI_sorteios_csv_mask)
        move_source_destiny(app_config.RT_www_path,
                            app_config.MI_shared_folder + app_config.MI_lothon_data_cache,
                            app_config.MI_jogos_csv_mask)

        # arquivos da B3 contendo cotacoes de acoes e ibovespa:
        copy_source_destiny(app_config.RT_www_path,
                            app_config.MI_local_folder + app_config.MI_quanthon_data_ibovespa,
                            app_config.RT_files_csv_mask)
        copy_source_destiny(app_config.RT_www_path,
                            app_config.MI_local_folder + app_config.MI_quanthon_data_cotacoes,
                            app_config.RT_files_zip_mask)

        move_source_destiny(app_config.RT_www_path,
                            app_config.MI_shared_folder + app_config.MI_quanthon_data_ibovespa,
                            app_config.RT_files_csv_mask)
        move_source_destiny(app_config.RT_www_path,
                            app_config.MI_shared_folder + app_config.MI_quanthon_data_cotacoes,
                            app_config.RT_files_zip_mask)
        logger.debug("Finalizou mocao dos arquivos baixados pelo Colethon para outra estacao.")

        # --- Procedimentos finais para encerramento do job -----------------------------------

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # ao final do processamento, cria arquivos temporarios informando o final do job:
        create_temp_flag(app_config.MI_local_folder + app_config.MI_lothon_data)
        create_temp_flag(app_config.MI_local_folder + app_config.MI_quanthon_data)
        create_temp_flag(app_config.MI_shared_folder + app_config.MI_lothon_data)
        create_temp_flag(app_config.MI_shared_folder + app_config.MI_quanthon_data)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Finalizado job '{self.job_id}' para copiar/mover arquivos para outra "
                    f"estacao. Tempo gasto: {_stopWatch}")
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
