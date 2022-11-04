"""
   Package colethon.jobs
   Module  download_loterias_caixa.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import shutil
import time
from datetime import date
import logging

# Libs/Frameworks modules
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

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

# efetua o download do arquivo de resultados da loteria a partir da URL configurada pra este job:
def download_resultados_loteria(browser: webdriver.Chrome, name: str, link: str,
                                download_or_scrap: bool) -> bool:
    try:
        # acessa link desta Loteria da Caixa com selenium:
        browser.get(link)
        logger.debug(f"A pagina da Loteria '{name}' foi carregada com sucesso.")

        # timeout para o browser aguardar o carregamento da pagina inteira.
        time.sleep(app_config.CX_timeout_loadpage)

        # verifica se a loteria tem resultados para download:
        if download_or_scrap:  # True == tem resultados para fazer o download...
            # p/ simular download com click, localiza o elemento HTML do tipo <a href>:
            el_a = browser.find_element(by=By.PARTIAL_LINK_TEXT, value=app_config.LC_text_resultado)
            logger.debug(f"Elemento HTML encontrado: {el_a}")

            # clica no <a> para abertura da pagina de resultados, para salvar em disco.
            el_a.click()
            logger.debug("Efetuado click na pagina para download da Loteria '%s'.", name)

            if len(browser.window_handles) > 1:
                logger.debug("Ativando segunda aba do browser para download da Loteria.")
                window_after = browser.window_handles[1]
                browser.switch_to.window(window_name=window_after)

            # timeout para o browser aguardar o carregamento da pagina para download.
            time.sleep(app_config.CX_timeout_download)

            # gera o nome do arquivo HTM a ser salvo apos download dos resultados:
            loteria_htm_name = app_config.LC_loteria_htm_name
            loteria_htm_name = loteria_htm_name.format(name)
            loteria_htm_path = os.path.join(app_config.RT_www_path, loteria_htm_name)

            # obtem o HTML diretamente da pagina de resultados aberta e salva em arquivo:
            logger.debug("Iniciando download de resultados da Loteria '%s' apos click na pagina.",
                         name)
            with open(loteria_htm_path, "w", encoding="utf-8") as file_htm:
                file_htm.write(browser.page_source)

            # verifica se tudo ok com o arquivo HTM da loteria:
            file_stats = os.stat(loteria_htm_path)
            if file_stats.st_size < 100000:  # se o HTM tiver menos de 100k, nao baixou resultados.
                logger.warning(f"Arquivo HTML da loteria {name} nao baixou resultados.")
                return False  # instrui baixar novamente

        else:  # False == eh preciso fazer scraping para extrair o resultado da pagina:
            logger.debug("Iniciando scraping de resultados da Loteria '%s' em sua pagina.", name)
            # identifica o numero do ultimo concurso e a respectiva data do sorteio:
            el_span = browser.find_element(by=By.XPATH, value=app_config.LC_xpath_concurso)
            logger.debug(f"Titulo da Loteria: Concurso = {el_span.text}")
            titulo_concurso = el_span.text.split(' ')
            if len(titulo_concurso) != 3:  # ocorreu alguma mudanca na pagina...
                logger.warning(f"Arquivo HTML da loteria {name} sofreu mudanças!")
                return False
            id_concurso = int(titulo_concurso[1])

            # identifica as dezenas sorteadas:
            dezenas: tuple = ()  # coloca o nr do concurso com as dezenas
            for li in browser.find_elements(by=By.XPATH, value=app_config.LC_xpath_dezenas):
                dezena = int(li.text)
                dezenas += (dezena,)
            logger.debug(f"Dezenas sorteadas no Concurso #{id_concurso} da Loteria: {dezenas}")

            # gera o nome do arquivo CSV a ser salvo apos scraping dos resultados:
            loteria_htm_name = app_config.JC_sorteios_csv_name.format(name)
            loteria_htm_path = os.path.join(app_config.RT_data_path, loteria_htm_name)

            # carrega os sorteios anteriores e obtem o numero de concursos ja lidos/registrados:
            with open(loteria_htm_path, 'r') as csv:
                nr_concursos = len(csv.readlines())

            # se o concurso recem lido ja estiver sido lido antes, entao ignora:
            if nr_concursos == id_concurso:
                logger.info(f"O concurso #{id_concurso} ja foi lido e salvo em CSV anteriormente.")
            else:
                logger.debug(f"Incluindo concurso #{id_concurso} no arquivo '{loteria_htm_name}'.")
                # ordena as dezenas e transforma em string para salvar em CSV:
                line_dezenas = ','.join([str(n) for n in sorted(dezenas)])
                with open(loteria_htm_path, 'a') as csv:
                    csv.write(line_dezenas + '\n')  # tem q mudar de linha

            # eh preciso copiar esse arquivo CSV para www:
            shutil.copy(loteria_htm_path, app_config.RT_www_path)

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

        :return: Retorna o id do job, unico entre todos os jobs do Colethon, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        return "LOTERIA_CAIXA"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em segundos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em segundos.
        """
        interval = app_config.LC_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> bool | Exception:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.

        :return Retorna True se o processamento foi realizado com sucesso,
        ou False se ocorreu algum erro.
        """
        _startWatch = startwatch()
        logger.info("Iniciando job '%s' para download dos resultados das loterias da Caixa EF.",
                    self.job_id)

        # o processamento eh feito conforme a data atual:
        hoje = date.today()
        logger.debug("Processando downloads para a data '%s'", hoje)

        # gera o nome do arquivo de controle para a data de hoje.
        ctrl_file_job = commons.arquivo_controle(app_config.LC_ctrl_file_mask)
        logger.debug("Arquivo de controle a ser verificado hoje: %s", ctrl_file_job)

        # se ja existe arquivo de controle para hoje, entao o processamento foi feito antes.
        if os.path.exists(ctrl_file_job):
            # pode cancelar o job porque nao sera mais necessario por hoje.
            logger.warning("O job '%s' ja foi concluido hoje mais cedo e sera cancelado.",
                           self.job_id)
            if callback_func is not None:
                callback_func(self.job_id)
            return True  # ao cancelar o job, nao sera mais executado novamente.
        else:
            logger.info("Arquivo de controle nao foi localizado. Job ira prosseguir.")

        # identifica as loterias da Caixa a serem processadas:
        caixa_loterias_url = app_config.LC_caixa_loterias_url
        if len(caixa_loterias_url) == 0:
            logger.error("Nao ha loterias da Caixa configuradas em INI para processamento.")
            if callback_func is not None:
                callback_func(self.job_id)
            return True  # ao cancelar o job, nao sera mais executado novamente.

        # verifica se o computador esta conectado a internet e se o site da Caixa esta ok.
        uri_site = app_config.CX_uri_site
        uri_port = app_config.CX_uri_port
        if commons.web_online(uri_site, uri_port):
            logger.info("Conexao com Internet testada e funcionando OK.")
        else:
            # se esta sem acesso, interrompe e tenta novamente na proxima execucao.
            logger.error("Sem conexao com internet ou acesso ao site da Caixa EF.")
            return False  # ao sair do job, sem cancelar, permite executar novamente depois.

        # percorre lista de loterias para processar cada download.
        for name, link, flag in caixa_loterias_url:
            # ira repetir para cada loteria, ate baixar corretamente os concursos:
            result_ok: bool = False
            while not result_ok:
                # inicia navegador para download com selenium:
                browser = commons.open_webdriver_chrome(app_config.RT_www_path,
                                                        app_config.CX_timeout_download)
                if browser is None:  # se nao ativou o WebDriver nao tem como prosseguir...
                    # pode cancelar o job porque nao sera mais executado.
                    logger.error("O job '%s' nao pode prosseguir sem o WebDriver do Chrome.",
                                 self.job_id)
                    if callback_func is not None:
                        callback_func(self.job_id)
                    return True  # ao cancelar o job, nao sera mais executado novamente.

                # acessa site da Caixa com selenium e baixa os resultados de cada loteria.
                logger.info("Iniciando download da loteria '{name}' a partir do site '{link}'...")
                result_ok = download_resultados_loteria(browser, name, link, to_bool(flag))
                if result_ok:
                    logger.info(f"Download dos resultados da Loteria '{name}' efetuado com "
                                f"sucesso.")
                else:
                    # se alguma das loterias apresentar erro, entao tenta de novo:
                    logger.error(f"Erro ao executar download dos resultados da Loteria '{name}'. "
                                 f"Vai tentar novamente...")

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Finalizado job '{self.job_id}' para download dos resultados das loterias "
                    f"da Caixa EF. Tempo gasto: {_stopWatch}")
        if callback_func is not None:
            callback_func(self.job_id)

        # indica que o processamento foi realizado com sucesso:
        return True

# ----------------------------------------------------------------------------
