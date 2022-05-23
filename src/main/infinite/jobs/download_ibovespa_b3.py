"""
   Package infinite.jobs
   Module  download_ibovespa_b3.py

   Realiza o download do arquivo texto da B3 contendo os ativos que compoem o IBOVESPA
   e monta arquivo com relacao de ativos a serem processados para coleta de cotacoes:
   C:/Users/<user>/AppData/Roaming/MetaQuotes/Terminal/Common/Files/b3_ibov.txt
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import glob
import shutil
import logging
import time
from datetime import date, datetime

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
    ctrl_file_name = data.strftime(app_config.CI_ctrl_file_mask)

    # e identifica o path onde sera salvo:
    ctrl_file_name = os.path.join(app_config.RT_tmp_path, ctrl_file_name)

    return ctrl_file_name


# efetua o download do arquivo CSV simulando click() na pagina HTML:
def download_ibov_csv(browser: webdriver.Chrome) -> None:
    logger.debug("Vai simular click na pagina para download da Carteira do IBovespa...")

    # acessa site da B3 com selenium e simula download com click.
    url_carteira_ibov = app_config.CI_url_carteira_ibov
    browser.get(url_carteira_ibov)
    logger.debug(f"A pagina da Carteira do IBovespa (B3) foi carregada com sucesso.")

    # timeout para o browser aguardar o carregamento da pagina inteira.
    time.sleep(app_config.B3_timeout_loadpage)

    # localiza o elemento HTML do tipo <a href> para simular click:
    xpath_a_click = app_config.CI_xpath_a_click
    el_a = browser.find_element(By.XPATH, xpath_a_click)
    logger.debug("Elemento HTML encontrado: %s", el_a)

    # clica no <a> para download e salva arquivo CSV para leitura e processamento.
    logger.debug("Iniciando download da Carteira do IBovespa apos click na pagina...")
    el_a.click()

    # timeout para o browser aguardar o carregamento da pagina para download.
    time.sleep(app_config.B3_timeout_download)
    logger.debug("Finalizado download da Carteira do IBovespa.")


# Efetua a leitura e parsing do arquivo CSV contendo a carteira do IBOV:
def parse_ibov_csv(www_ibov_csv: str) -> list[str]:
    logger.debug("Lendo arquivo CSV '%s' da Carteira do IBovespa...", www_ibov_csv)

    # le arquivo CSV e obtem relacao de ativos que compoem o ibovespa no dia corrente.
    carteira_ibov: list[str]
    with open(www_ibov_csv, "rt") as csv:
        lines = csv.readlines()
        # faz o parsing do arquivo para extrair apenas o nome dos ativos da carteira.
        carteira_ibov = [line.split(';')[0] for line in lines[2:-2]]

    # ordena os ativos principais
    carteira_ibov.sort()

    return carteira_ibov


# Salva a carteira IBOVESP em arquivo texto dentro do terminal MT5:
def salva_ibov_txt(carteira_ibov: list[str]) -> bool:
    # salva arquivo b3_ibov.txt com ativos e derivativos primeiro na pasta temporaria:
    tmp_ibov_txt = os.path.join(app_config.RT_tmp_path, app_config.CI_ibov_txt_name)
    logger.debug("Salvando arquivo TXT '%s' com %d ativos da Carteira do IBovespa...",
                 tmp_ibov_txt, len(carteira_ibov))

    with open(tmp_ibov_txt, "wt") as txt:
        txt.write('\n'.join(carteira_ibov))

    # entao move arquivo TXT para MetaQuotes\Terminal\Common\Files\
    mt5_ibov_txt = os.path.join(app_config.RT_mt5_terminal_commons, app_config.CI_ibov_txt_name)
    logger.debug("Arquivo TXT '%s' sera movido para pasta do terminal do MT5 '%s'.",
                 app_config.CI_ibov_txt_name, app_config.RT_mt5_terminal_commons)

    shutil.move(tmp_ibov_txt, mt5_ibov_txt)
    logger.info("Arquivo TXT foi movido para pasta do terminal do MT5: '%s'.", mt5_ibov_txt)
    return True  # operacao concluida com sucesso.


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class DownloadIbovespaB3(AbstractJob):
    """
    Implementacao de job para efetuar o download e processamento da Carteira Teorica do IBovespa.
    """

    # --- PROPRIEDADES -----------------------------------------------------

    @property
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Infinite, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "CARTEIRA_IBOVESPA"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.CI_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Efetua o download e processamento da Carteira Teorica do IBovespa.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        _startTime: datetime = datetime.now()
        logger.info("Iniciando job '%s' para download da Carteira Teorica do IBovespa.",
                    self.job_id)

        # o processamento eh feito conforme a data atual:
        hoje = date.today()
        logger.debug("Processando download para a data '%s'", hoje)

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

        # se tudo ok ate aqui, inicia navegador para download com selenium:
        browser = commons.open_webdriver_chrome(app_config.RT_www_path,
                                                app_config.B3_timeout_download)
        if browser is None:  # se nao ativou o WebDriver nao tem como prosseguir...
            # pode cancelar o job porque nao sera mais executado.
            logger.error("O job '%s' nao pode prosseguir sem o WebDriver do Chrome.", self.job_id)
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.

        try:
            # acessa site da B3 com selenium e simula download com click.
            download_ibov_csv(browser)

            logger.info("Download da Carteira Teorica do IBovespa efetuado com sucesso.")

        # captura as excecoes InvalidArgumentException, NoSuchElementException,
        #                     InvalidSelectorException
        except WebDriverException as ex:
            # se o site esta fora do ar ou o HTML foi alterado, interrompe e tenta depois:
            logger.error("Erro ao tentar localizar botao de download no site da B3:\n  %s",
                         repr(ex))
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # ao final, fecha navegador e encerra o webdriver...
        finally:
            browser.quit()

        # mask usada para localizar todos os arquivos CSV ja baixados em \www:
        ibov_csv_mask = app_config.CI_ibov_csv_mask
        mask_www_ibov = os.path.join(app_config.RT_www_path, ibov_csv_mask)

        # para ter certeza, confirma se o arquivo CSV foi baixado sem problemas:
        www_contents = glob.glob(mask_www_ibov)
        len_contents = len(www_contents)
        if len_contents > 0:
            logger.debug("Encontrado(s) %d arquivo(s) CSV em '%s'.",
                         len_contents, app_config.RT_www_path)
        else:
            logger.error("Nenhum arquivo 'IBOVDia_??-??-??.csv' foi encontrado em '%s'",
                         app_config.RT_www_path)
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # dos arquivos CSV encontrados, identifica o mais recente (fez download agora):
        www_ibov_csv = max(www_contents, key=os.path.getctime)

        # se tudo ok ate aqui, inicia processamento do arquivo CSV presente em \www
        logger.debug("Sera utilizado para processamento o arquivo CSV mais recente '%s'",
                     www_ibov_csv)

        # le arquivo CSV e obtem relacao de ativos que compoem o ibovespa no dia corrente.
        carteira_ibov: list[str] = parse_ibov_csv(www_ibov_csv)

        # contabiliza o numero de ativos lidos do CSV e efetua validacao (bom senso):
        len_carteira_ibov = len(carteira_ibov)
        if len_carteira_ibov > 10:  # razoavel ter ao menos 10 ativos na carteira IBOVESPA
            logger.debug("Foram lidos %d ativos a partir do arquivo '%s'",
                         len_carteira_ibov, www_ibov_csv)
        elif len_carteira_ibov > 0:
            logger.error("Poucos ativos foram encontrados no arquivo '%s'", www_ibov_csv)
            return  # ao sair do job, sem cancelar, permite executar novamente depois.
        else:
            logger.error("Nenhum ativo foi encontrado no arquivo '%s'", www_ibov_csv)
            return  # ao sair do job, sem cancelar, permite executar novamente depois.

        # obtem os derivativos adicionais do arquivo INI da aplicacao.
        derivativos = app_config.CI_derivativos
        logger.debug("Vai adicionar os derivativos  %s  na relacao de ativos...", derivativos)
        carteira_ibov.extend(derivativos)

        # Salva a carteira IBOVESP em arquivo texto dentro do terminal MT5:
        salva_ibov_txt(carteira_ibov)

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        _totalTime = datetime.now() - _startTime
        logger.info(f"Finalizado job '{self.job_id}' para download da carteira do IBOVESPA. "
                    f"Tempo gasto: {_totalTime}")
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
