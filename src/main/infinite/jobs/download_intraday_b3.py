"""
   Package infinite.jobs
   Module  download_intraday_b3.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import logging
from datetime import date, timedelta

# Libs/Frameworks modules

# Own/Project modules
from infinite.jobs.abstract_job import AbstractJob
from infinite.conf import app_config
from infinite.jobs import commons
from infinite.util import feriado


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# gera o nome do arquivo de controle para indicar status do job:
def arquivo_controle(data: date) -> str:
    # aplica a mascara na data fornecida, configurada no INI,
    ctrl_file_name = data.strftime(app_config.IB_ctrl_file_mask)

    # e identifica o path onde sera salvo:
    ctrl_file_name = os.path.join(app_config.RT_tmp_path, ctrl_file_name)

    return ctrl_file_name


# efetua o download do arquivo ZIP a partir da URL configurada pra este job:
def download_cotacoes_intraday(data: date) -> bool:
    logger.debug("Vai acessar URL da B3 p/ download de Cotacoes Intraday na data '%s'.", data)

    url_cotacoes_intraday = app_config.IB_url_cotacoes_intraday
    intraday_url_mask = app_config.IB_intraday_url_mask
    intraday_zip_mask = app_config.IB_intraday_zip_mask

    # gera a url para o arquivo ZIP na data especifica:
    url_download_zip = url_cotacoes_intraday + data.strftime(intraday_url_mask)

    # gera o nome do arquivo ZIP a ser salvo apos download:
    intraday_zip_name = os.path.join(app_config.RT_www_path,
                                     data.strftime(intraday_zip_mask))

    # se nao conseguir fazer download do arquivo ZIP:
    if commons.download_file(url_download_zip, intraday_zip_name):
        logger.info("Download da URL '%s' efetuado com sucesso.", url_download_zip)
        return True
    else:
        logger.error("Nao foi possivel efetuar download a partir da URL '%s'.", url_download_zip)
        return False


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class DownloadIntradayB3(AbstractJob):
    """
    Implementacao de job para download das Cotacoes IntraDay da B3.
    """

    # --- PROPRIEDADES -----------------------------------------------------

    @property
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Infinite, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "INTRADAY_B3"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.IB_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        logger.info("Iniciando job '%s' para download das Cotacoes IntraDay da B3.", self.job_id)

        # o processamento eh feito conforme a data atual:
        hoje = date.today()
        logger.debug("Processando downloads para a data '%s'", hoje)

        # gera o nome do arquivo de controle para a data de hoje.
        ctrl_file_job = arquivo_controle(hoje)
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

        # verifica se o computador esta conectado a internet e se o site da B3 esta ok.
        uri_site = app_config.B3_uri_site
        uri_port = app_config.B3_uri_port
        if commons.web_online(uri_site, uri_port):
            logger.info("Conexao com Internet testada e funcionando OK.")
        else:
            # se esta sem acesso, interrompe e tenta novamente na proxima execucao.
            logger.error("Sem conexao com internet ou acesso ao site da B3.")
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # se tudo ok ate aqui, procede aos downloads de 2 dias anteriores:
        yesterday = hoje  # a partir da data atual ira retroceder 2 dias uteis anteriores...
        for _ in (1, 2):
            yesterday -= timedelta(1)  # a cada iteracao, subtrai 1 dia
            # se esse dia for feriado ou fim de semana, entao segue subtraindo:
            while not feriado.is_dia_util_bolsa(yesterday):  # ate encontrar dia util
                yesterday -= timedelta(1)

            # tenta fazer o download do arquivo ZIP conforme URL pra este job:
            if not download_cotacoes_intraday(yesterday):
                # interrompe e tenta novamente na proxima execucao...
                return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        logger.info("Finalizado job '%s' para download das Cotacoes IntraDay da B3.", self.job_id)
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
