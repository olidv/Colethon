"""
   Package colethon
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
# Own/Project modules
from colethon.conf import app_config
from colethon.jobs.bolsa.download_ibovespa_b3 import DownloadIbovespaB3
from colethon.jobs.bolsa.download_intraday_b3 import DownloadIntradayB3
from colethon.jobs.caixa.download_loterias_caixa import DownloadLoteriasCaixa
from colethon.jobs.caixa.compute_sorteios_loterias import ComputeSorteiosLoterias
from colethon.jobs.infra.zip_files_mql5 import ZipFilesMql5
from colethon.jobs.infra.move_files_intranet import MoveFilesIntranet


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# pilha para armazenar os jobs a serem agendados/executados sequencialmente,
# em ordem FIFO (First In, First Out), pois Python nao eh multi-thread na real.
queue_jobs = Queue(maxsize=10)


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas agendadas:
def main():
    logger.info("Iniciando agendamento dos jobs relativos a Bolsas de Valores...")

    # --- Agendamento dos Jobs em Fila ---------------------------------------

    # Download da Carteira Teorica do IBovespa
    queue_jobs.put(DownloadIbovespaB3())

    # Download das Cotacoes IntraDay da B3
    queue_jobs.put(DownloadIntradayB3())

    # Download dos Resultados das Loterias da Caixa:
    queue_jobs.put(DownloadLoteriasCaixa())

    # Processamento dos sorteios das das Loterias:
    queue_jobs.put(ComputeSorteiosLoterias())

    # Compactar arquivos CSV nos terminais MT5
    queue_jobs.put(ZipFilesMql5())

    # Copiar/mover arquivos para outra estacao
    queue_jobs.put(MoveFilesIntranet())

    # --- Monitoramento das Execucoes ----------------------------------------

    # mantem parametros em variaveis locais para melhor performance:
    loop_wait = app_config.SC_time_wait

    # mantem o script em execucao permanente enquanto houver jobs enfileirados...
    while not queue_jobs.empty():  # tem mais jobs?
        # obtem o proximo job e dispara sua execucao:
        job_obj = queue_jobs.get()  # Fila do tipo FIFO: First In (put), First Out (get)
        job_idle_seconds = job_obj.job_interval  # cada job tem seu tempo de espera especifico

        # executa o job em loop infinito, para o caso de ocorrer algum erro momentaneo
        while True:
            try:
                ret_ok = job_obj.run_job()  # por enquanto, nao utiliza callbacks
            except:
                ret_ok = False
            # se o processamento foi realizado com sucesso, segue para proximo job:
            if ret_ok:
                break
            else:
                # aguarda um tempo antes de executar novamente
                time.sleep(job_idle_seconds)

        # aguarda periodo de tempo padrao, antes de executar proximo job:
        time.sleep(loop_wait)

    # finalizados todos os jobs, informa que o processamento foi ok:
    logger.info("Finalizados todos os jobs relativos a Bolsas de Valores.")
    return 0

# ----------------------------------------------------------------------------
