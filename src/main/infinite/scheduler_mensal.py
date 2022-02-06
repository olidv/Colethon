"""
   Package infinite
   Module  scheduler_mensal.py

   Modulo para agendar as tarefas mensais do Infinite, atraves do agendador
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
# from infinite.util.parallel_task import run_threaded


# ----------------------------------------------------------------------------
# VARIAVEIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES
# ----------------------------------------------------------------------------

# cancela o job fornecido:
def cancel_job(job_id):
    schedule.clear(job_id)
    logger.info("Cancelado mensal: '%s'.", job_id)


# entry-point de execucao para tarefas mensais:
def main():
    logger.info("Iniciando agendamento dos jobs mensais...")

    # mantem valores em variaveis locais para melhor performance:
    job_delay = app_config.SC_job_delay
    time_wait = app_config.SC_time_wait
    loop_on = app_config.SC_loop_on

    # --- Job Mensal ---------------------------------------------------------

    logger.debug("Incluindo intervalo de %d segundos entre as execucoes...", job_delay)
    time.sleep(job_delay)

    # --- Monitoramento do Scheduler -----------------------------------------

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
    logger.info("Finalizados todos os jobs mensais.")
    return 0

# ----------------------------------------------------------------------------
