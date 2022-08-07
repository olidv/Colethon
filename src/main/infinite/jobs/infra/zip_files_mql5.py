"""
   Package infinite.jobs
   Module  zip_files_mql5.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import glob
import zipfile
import logging
from datetime import date, datetime

# Libs/Frameworks modules
import send2trash

# Own/Project modules
from infinite.conf import app_config
from infinite.util.eve import *
from infinite.jobs import commons
from infinite.jobs.abstract_job import AbstractJob


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# relaciona os arquivos CSV presentes na pasta do terminal corrente:
def list_files_contents() -> list[str]:
    # mask usada para localizar todos os arquivos CSV em cada terminal:
    mask_files_csv = app_config.RT_files_csv_mask

    # verifica se ha arquivos CSV a serem compactados na pasta do terminal:
    files_contents = glob.glob(mask_files_csv)
    len_contents = len(files_contents)
    if len(files_contents) > 0:
        logger.debug("Pasta 'Terminal_Files' possui %d arquivos '%s'...",
                     len_contents, mask_files_csv)
    else:
        logger.debug("Nenhum arquivo '%s' foi encontrado na pasta 'Terminal_Files'.",
                     mask_files_csv)

    return files_contents


# relaciona os arquivos CSV presentes na pasta do terminal para uma data:
def list_files_date_contents(date_file_csv: date) -> list[str]:
    # monta mascara para identificar outros arquivos da mesma data:
    mask_files_date_csv = date_file_csv.strftime("%Y.%m.%d_*.csv")

    # verifica se ha arquivos CSV na pasta do  terminal para a data fornecida:
    files_date_contents = glob.glob(mask_files_date_csv)
    len_date_contents = len(files_date_contents)
    if len_date_contents > 0:
        logger.debug("Encontrados %d arquivos '%s' para processamento em 'Terminal_Files'.",
                     len_date_contents, mask_files_date_csv)
    else:
        logger.debug("Nenhum arquivo '%s' encontrado para processamento na pasta 'Terminal_Files'.",
                     mask_files_date_csv)

    return files_date_contents


# compacta a relacao de arquivos encontrados, na propria pasta do terminal:
def compacta_files_csv(files_date_contents: list[str], date_file_csv: date) -> None:
    # utiliza a data corrente para gerar o nome do arquivo ZIP:
    name_file_zip = date_file_csv.strftime("Files_%Y-%m-%d.zip")

    # esta operacao eh realizada no proprio diretorio da pasta de terminal:
    logger.debug("Compactando arquivos CSV em pacote '%s' na pasta 'Terminal_Files'...",
                 name_file_zip)
    with zipfile.ZipFile(name_file_zip, 'w') as zip_file:
        for csv in files_date_contents:
            zip_file.write(csv, compress_type=zipfile.ZIP_DEFLATED)

    # apos compactar os arquivos, elimina-os da pasta, movendo para lixeira:
    logger.debug("Movendo para lixeira os arquivos '%s' na pasta 'Terminal_Files'...",
                 date_file_csv.strftime("%Y.%m.%d_*.csv"))
    for csv in files_date_contents:
        send2trash.send2trash(csv)


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class ZipFilesMql5(AbstractJob):
    """
    Implementacao de job para compactar arquivos CSV nos terminais MT5.
    """

    # --- PROPRIEDADES -----------------------------------------------------

    @property
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Infinite, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "ZIP_MQL5"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.ZM_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        _startWatch = startwatch()
        logger.info("Iniciando job '%s' para compactar arquivos CSV nos terminais MT5.",
                    self.job_id)

        # o processamento eh feito conforme a data atual:
        hoje = date.today()
        logger.debug("Processando compactacao de arquivos para a data '%s'", hoje)

        # gera o nome do arquivo de controle para a data de hoje.
        ctrl_file_job = commons.arquivo_controle(app_config.ZM_ctrl_file_mask)
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

        # identifica os terminais MT5 instalados na estacao:
        mt5_instances_id = app_config.RT_mt5_instances_id
        if len(mt5_instances_id) == 0:
            logger.error("Nao ha terminais MT5 configurados em INI para processamento.")
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.

        # percorre lista de terminais para processar cada pasta <MQL5\Files>.
        for idt, cia in mt5_instances_id:
            # eh necessario fazer replace com o id do terminal em cada instancia:
            terminal_files = app_config.RT_mt5_terminal_mql5_files.replace('%id', idt)
            logger.info(
                "Iniciando processamento dos arquivos CSV na pasta '%s' da corretora '%s'...",
                terminal_files, cia.upper())

            # modifica o diretorio corrente (da thread) para a pasta do terminal:
            os.chdir(terminal_files)  # evita o caminho completo no ZIP...

            # verifica se ha arquivos CSV a serem compactados na pasta do terminal:
            files_contents = list_files_contents()
            len_files_contents = len(files_contents)
            if len_files_contents == 0:  # se nao tiver arquivos CSV, entao ignora...
                continue  # prossegue para a proxima pasta de terminal MT5...

            # efetua loop para cada conjunto de arquivos com data determinada:
            while len_files_contents > 0:
                # identifica o primeiro arquivo CSV da lista para compactar pela data:
                first_file_csv = None
                date_file_csv = None

                # se o arquivo CSV foi criado hoje, deve ser ignorado (em uso):
                logger.debug("Busca arquivos CSV mais antigos na pasta 'Terminal_Files'.")
                for csv in files_contents:
                    # soh por garantia, pega soh o nome, sem o path completo.
                    csv = os.path.basename(csv)

                    # extrai a data do arquivo para verificar se nao eh o dia de hoje:
                    date_file_csv = datetime.strptime(csv[:10], "%Y.%m.%d").date()
                    if date_file_csv != hoje:  # pode ser qualquer arquivo mais antigo.
                        first_file_csv = csv
                        break

                # se apos o loop nao encontrou nenhum arquivo CSV mais antigo:
                if first_file_csv is None:
                    logger.debug("Nenhum arquivo CSV mais antigo na pasta 'Terminal_Files'.")
                    break  # ignora esta pasta de terminal e vai para proxima:

                # neste ponto, encontrou arquivo CSV mais antigo, para compactar:
                logger.debug("Compactando arquivos CSV que possuem a mesma data de '%s'...",
                             first_file_csv)

                # obtem arquivos CSV presentes na pasta do terminal para a data corrente:
                files_date_contents = list_files_date_contents(date_file_csv)
                # verifica se ha mais arquivos com a mesma data:
                if len(files_date_contents) == 0:  # testa soh por garantia.
                    break  # prossegue para a proxima pasta de terminal MT5...

                # compacta a relacao de arquivos encontrados, na propria pasta do terminal:
                compacta_files_csv(files_date_contents, date_file_csv)

                # verifica se ainda ha mais arquivos CSV na pasta do terminal:
                files_contents = list_files_contents()
                len_files_contents = len(files_contents)

            logger.info("Finalizou processamento da pasta 'Terminal_Files'...")

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Finalizado job '{self.job_id}' para compactar arquivos CSV nos "
                    f"terminais MT5. Tempo gasto: {_stopWatch}")
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
