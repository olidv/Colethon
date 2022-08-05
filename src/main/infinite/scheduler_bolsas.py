"""
   Package infinite
   Module  scheduler_bolsas.py

   Modulo para agendar as tarefas relativas a bolsas de valores,
   atraves do agendador utilitario do Python (lib schedule).
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import time
import logging
from queue import Queue

# Libs/Frameworks modules
import schedule

# Own/Project modules
from infinite.conf import app_config
from infinite.util.parallel_task import run_threaded
from infinite.jobs.bolsa.download_ibovespa_b3 import DownloadIbovespaB3
from infinite.jobs.bolsa.download_intraday_b3 import DownloadIntradayB3
from infinite.jobs.caixa.download_loterias_caixa import DownloadLoteriasCaixa
from infinite.jobs.infra.zip_files_mql5 import ZipFilesMql5
from infinite.jobs.infra.move_files_intranet import MoveFilesIntranet


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# pilha para armazenar os jobs a serem agendados/executados sequencialmente,
# em ordem FIFO (First In, First Out), pois Python nao eh multi-thread na real.
queue_jobs = Queue(maxsize=10)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# verificar se ainda ha jobs pendentes a serem executados:
def has_pending_jobs():
    return (not queue_jobs.empty()) or (schedule.idle_seconds() is not None)


# configura as tarefas no scheduler de acordo com as opcoes de execucao do job:
def schedule_job(job_obj):
    # o job sera executado em nova thread:
    schedule.every(job_obj.job_interval).minutes.do(run_threaded, job_obj.run_job, cancel_job) \
                                                .tag(job_obj.job_id)
    logger.info(f"Agendado job '{job_obj.job_id}' a cada {job_obj.job_interval} minutos.")


# cancela o job fornecido:
def cancel_job(job_id):
    schedule.clear(job_id)
    logger.info(f"Cancelado job agendado: '{job_id}'.")


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas agendadas:
def main():
    logger.info("Iniciando agendamento dos jobs relativos a Bolsas de Valores...")

    # --- Agenamento dos Jobs em Fila ----------------------------------------

    # Download da Carteira Teorica do IBovespa
    queue_jobs.put(DownloadIbovespaB3())

    # Download das Cotacoes IntraDay da B3
    queue_jobs.put(DownloadIntradayB3())

    # Download dos Resultados das Loterias da Caixa:
    queue_jobs.put(DownloadLoteriasCaixa())

    # Compactar arquivos CSV nos terminais MT5
    queue_jobs.put(ZipFilesMql5())

    # Copiar/mover arquivos para outra estacao
    queue_jobs.put(MoveFilesIntranet())

    # --- Monitoramento do Scheduler -----------------------------------------

    # mantem valores em variaveis locais para melhor performance:
    time_wait = app_config.SC_time_wait
    # se nao for desejado continuar executando, valor de loop_on deve ser False (no).
    loop_on = app_config.SC_loop_on

    # mantem o script em execucao permanente enquanto os jobs estiverem agendados...
    while loop_on or has_pending_jobs():  # tem mais jobs?
        # atualiza variavel de controle para verificar se ainda ha jobs agendados:
        idles = schedule.idle_seconds()
        if idles is None:
            # se finalizou o ultimo job agendado, verifica se ainda ha job enfileirado:
            if not queue_jobs.empty():
                # se ha job enfileirado, entao agenda proximo job:
                schedule_job(queue_jobs.get())
                # atualiza idles com tempo ate a execucao do job recem agendado:
                idles = schedule.idle_seconds()
            elif loop_on:  # se estiver em 'loop-continuo':
                # aguarda determinado tempo (configurado) se nao tiver mais jobs:
                idles = time_wait

        # aguarda determinado tempo (em segundos) ate a proxima execucao:
        if idles is not None and idles > 0:  # pode ser negativo, por isso o segundo teste
            logger.info(f"Vai aguardar {idles} segundos ate a proxima execucao...")
            # apenas esta thread do scheduler diario sera interrompida:
            time.sleep(idles)

        # executa os jobs pendentes:
        schedule.run_pending()

    # finalizados todos os jobs, informa que o processamento foi ok:
    logger.info("Finalizados todos os jobs relativos a Bolsas de Valores.")
    return 0

# ----------------------------------------------------------------------------
