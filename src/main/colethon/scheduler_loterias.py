"""
   Package colethon
   Module  scheduler_loterias.py

   Modulo para agendar as tarefas relativas a loterias da caixa,
   atraves do agendador utilitario do Python (lib schedule).
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
from colethon.conf import app_config
from colethon.util.parallel_task import run_threaded


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas agendadas:
def main():
    logger.info("Iniciando agendamento dos jobs relativos a Loterias da Caixa...")

    # --- Monitoramento do Scheduler -----------------------------------------

    # mantem valores em variaveis locais para melhor performance:
    time_wait = app_config.SC_time_wait

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
    logger.info("Finalizados todos os jobs relativos a Loterias da Caixa.")
    return 0

# ----------------------------------------------------------------------------
