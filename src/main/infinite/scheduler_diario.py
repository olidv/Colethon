"""
   Package infinite
   Module  scheduler_diario.py

   Modulo para agendar as tarefas diarias do Infinite, atraves do agendador
   utilitario do Python (lib schedule).
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import time
import logging

# Libs/Frameworks modules
import schedule

# Own/Project modules
from infinite.conf import app_config
from infinite.util.parallel_task import run_threaded
from infinite.jobs.download_loterias_caixa import DownloadLoteriasCaixa
from infinite.jobs.download_ibovespa_b3 import DownloadIbovespaB3
from infinite.jobs.download_intraday_b3 import DownloadIntradayB3
from infinite.jobs.zip_files_mql5 import ZipFilesMql5
from infinite.jobs.move_files_intranet import MoveFilesIntranet


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# configura as tarefas no scheduler de acordo com as opcoes de execucao do job:
def schedule_job(job_obj):
    # o job sera executado em nova thread:
    schedule.every(job_obj.job_interval).minutes.do(run_threaded, job_obj.run_job, cancel_job) \
                                                .tag(job_obj.job_id)
    logger.info("Agendado job '%s' a cada %d minutos.", job_obj.job_id, job_obj.job_interval)

    logger.debug("Incluindo intervalo de %d segundos entre as execucoes...",
                 app_config.SC_job_delay)
    time.sleep(app_config.SC_job_delay)


# cancela o job fornecido:
def cancel_job(job_id):
    schedule.clear(job_id)
    logger.info("Cancelado job diario: '%s'.", job_id)


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def main():
    logger.info("Iniciando agendamento dos jobs diarios...")

    # Download dos Resultados das Loterias da Caixa:
    schedule_job(DownloadLoteriasCaixa())

    # Download das Cotacoes IntraDay da B3
    schedule_job(DownloadIntradayB3())

    # Download da Carteira Teorica do IBovespa
    schedule_job(DownloadIbovespaB3())

    # Compactar arquivos CSV nos terminais MT5
    schedule_job(ZipFilesMql5())

    # Copiar/mover arquivos para outra estacao
    schedule_job(MoveFilesIntranet())

    # --- Monitoramento do Scheduler -----------------------------------------

    # mantem valores em variaveis locais para melhor performance:
    time_wait = app_config.SC_time_wait
    loop_on = app_config.SC_loop_on

    # mantem o script em execucao permanente enquanto os jobs estiverem agendados...
    idles = schedule.idle_seconds()  # sera usado para verificar se ha jobs pendentes.
    # se nao for desejado continuar executando, valor de loop_on deve ser False (no).
    while loop_on or (idles is not None):  # tem mais jobs?
        # se estiver em 'loop-continuo' aguarda determinado tempo se nao tiver mais jobs
        if loop_on and (idles is None):
            idles = time_wait

        # aguarda determinado tempo (em segundos) ate a proxima execucao:
        if (idles is not None) and (idles > 1):
            logger.info("Vai aguardar %d segundos ate a proxima execucao...", idles)
            # apenas esta thread do scheduler diario sera interrompida:
            time.sleep(idles - 1)  # deixa 1 segundo de margem pois o time.sleep() nao eh exato.

        # executa os jobs pendentes:
        schedule.run_pending()

        # atualiza variavel de controle:
        idles = schedule.idle_seconds()

    # finalizados todos os jobs, informa que o processamento foi ok:
    logger.info("Finalizados todos os jobs diarios.")
    return 0

# ----------------------------------------------------------------------------
