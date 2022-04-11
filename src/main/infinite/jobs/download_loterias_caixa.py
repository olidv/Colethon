"""
   Package infinite.jobs
   Module  download_loterias_caixa.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import logging
import time
from datetime import date

# Libs/Frameworks modules
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

# Own/Project modules
from infinite.jobs.abstract_job import AbstractJob
from infinite.conf import app_config
from infinite.jobs import commons


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
    ctrl_file_name = data.strftime(app_config.LC_ctrl_file_mask)

    # e identifica o path onde sera salvo:
    ctrl_file_name = os.path.join(app_config.RT_tmp_path, ctrl_file_name)

    return ctrl_file_name


# efetua o download do arquivo de resultados da loteria a partir da URL configurada pra este job:
def download_resultados_loteria(browser: webdriver.Chrome, name: str, link: str,
                                xpath: str) -> bool:
    try:
        # acessa link desta Loteria da Caixa com selenium e simula download com click.
        browser.get(link)
        logger.debug("A pagina da Loteria '%s' foi carregada com sucesso.", name)

        # localiza o elemento HTML do tipo <a href> para simular click:
        el_a = browser.find_element(By.XPATH, xpath)
        logger.debug("Elemento HTML encontrado: %s", el_a)

        # clica no <a> para abertura da pagina de resultados, para salvar em disco.
        el_a.click()
        logger.debug("Efetuado click na pagina para download da Loteria '%s'.", name)

        # timeout para o browser aguardar o carregamento da pagina de resultados.
        # browser.implicitly_wait(app_config.LC_timeout_download)
        time.sleep(app_config.LC_timeout_download)

        if len(browser.window_handles) > 1:
            logger.debug("Ativando segunda aba do browser para download da Loteria.")
            window_after = browser.window_handles[1]
            browser.switch_to.window(window_name=window_after)

        # gera o nome do arquivo HTM a ser salvo apos download dos resultados:
        loteria_htm_name = app_config.LC_loteria_htm_name
        loteria_htm_name = loteria_htm_name.format(name)
        loteria_htm_path = os.path.join(app_config.RT_www_path, loteria_htm_name)

        # obtem o HTML diretamente da pagina de resultados aberta e salva em arquivo:
        logger.debug("Iniciando download de resultados da Loteria '%s' apos click na pagina.", name)
        with open(loteria_htm_path, "w", encoding="utf-8") as file_htm:
            file_htm.write(browser.page_source)

        logger.debug("Finalizado download dos resultados da Loteria '%s' no arquivo '%s'.",
                     name, loteria_htm_name)
        return True

    # captura as excecoes InvalidArgumentException, NoSuchElementException,
    #                     InvalidSelectorException
    except WebDriverException as ex:
        # se o site esta fora do ar ou o HTML foi alterado, interrompe e tenta depois:
        logger.error("Erro no download da Loteria '%s' no site da Caixa:\n  %s",
                     name, repr(ex))
        return False

    # ao final, fecha navegador e encerra o webdriver...
    finally:
        browser.quit()


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class DownloadLoteriasCaixa(AbstractJob):
    """
    Implementacao de job para download dos resultados das loterias da Caixa EF.
    """

    # --- PROPRIEDADES -----------------------------------------------------

    @property
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Infinite, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "LOTERIA_CAIXA"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.LC_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        logger.info("Iniciando job '%s' para download dos resultados das loterias da Caixa EF.",
                    self.job_id)

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

        # identifica as loterias da Caixa a serem processadas:
        caixa_loterias_url = app_config.LC_caixa_loterias_url
        if len(caixa_loterias_url) == 0:
            logger.error("Nao ha loterias da Caixa configuradas em INI para processamento.")
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.

        # verifica se o computador esta conectado a internet e se o site da Caixa esta ok.
        uri_site = app_config.LC_uri_site
        uri_port = app_config.LC_uri_port
        if commons.web_online(uri_site, uri_port):
            logger.info("Conexao com Internet testada e funcionando OK.")
        else:
            # se esta sem acesso, interrompe e tenta novamente na proxima execucao.
            logger.error("Sem conexao com internet ou acesso ao site da Caixa EF.")
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # percorre lista de loterias para processar cada download.
        for name, link, xpath in caixa_loterias_url:
            # inicia navegador para download com selenium:
            browser = commons.open_webdriver_chrome(app_config.RT_www_path,
                                                    app_config.LC_timeout_download)
            if browser is None:  # se nao ativou o WebDriver nao tem como prosseguir...
                # pode cancelar o job porque nao sera mais executado.
                logger.error("O job '%s' nao pode prosseguir sem o WebDriver do Chrome.",
                             self.job_id)
                if callback_func is not None:
                    callback_func(self.job_id)
                return  # ao cancelar o job, nao sera mais executado novamente.

            # acessa site da Caixa com selenium e baixa os resultados de cada loteria.
            logger.info("Iniciando download da loteria '%s' a partir do site '%s'...", name, link)
            if download_resultados_loteria(browser, name, link, xpath):
                logger.info("Download dos resultados da Loteria '%s' efetuado com sucesso.", name)
            else:
                logger.error("Erro ao executar download dos resultados da Loteria '%s'.", name)

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        logger.info("Finalizado job '%s' para download dos resultados das loterias da Caixa EF.",
                    self.job_id)
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
