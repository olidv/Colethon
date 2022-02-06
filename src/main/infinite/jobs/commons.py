"""
   Package infinite.jobs
   Module  commons.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import socket
import logging

# Libs/Frameworks modules
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Own/Project modules


# ----------------------------------------------------------------------------
# VARIAVEIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES
# ----------------------------------------------------------------------------

# verifica se o computador possui conexao com a internet e o site fornecido esta ok:
def web_online(uri_site: str, uri_port: int) -> bool:
    logger.debug("Verificando conexao com internet acessando website '%s:%d'.", uri_site, uri_port)
    try:
        # tenta conectar com o site via socket e verifica se vai disparar exception:
        sock = socket.create_connection((uri_site, uri_port))
        if sock is not None:
            sock.close()
        return True

    # qualquer erro significa que nao pode acessar o web site...
    except OSError as err:
        logger.critical("Nao foi possivel acessar o site '%s:%d'. ERRO: %s",
                        uri_site, uri_port, repr(err))
    return False


# realiza o download de arquivo a partir de URL fornecida:
def download_file(url_download: str, file_name: str) -> bool:
    logger.debug("Iniciando acesso a URL '%s' para baixar arquivo '%s'.", url_download, file_name)

    # utiliza library requests:
    try:
        res = requests.get(url_download, allow_redirects=True)
        logger.debug("Retornou Status-Code '%s' apos acessar URL '%s'.",
                     res.status_code, url_download)

        res.raise_for_status()  # vai disparar exception se ocorreu algum erro...
        if res.status_code != requests.codes.ok:  # verificacao adicional p/ seguranca.
            return False

        # salva o conteudo do download em arquivo local:
        logger.debug("Baixando e salvando arquivo '%s'...", file_name)
        with open(file_name, 'wb') as output:  # considera o arquivo como binario.
            output.write(res.content)

        logger.info("Download do arquivo '%s' finalizado com sucesso.", file_name)

    except Exception as ex:
        logger.error("Nao foi possivel efetuar download da URL '%s'. ERRO: %s",
                     url_download, repr(ex))
        return False

    # se chegou aqui, entao o download foi efetuado com sucesso:
    return True


# abre o navegador Chrome e configura as opcoes para download automatico e direto:
def open_webdriver_chrome(download_directory: str,
                          timeout_download: int) -> webdriver.Chrome:
    # utiliza as preferencias especificas do Chrome para nao abrir dialogo de download:
    options = Options()
    options.add_argument('--headless')  # nao exibe a janela do browser
    options.add_argument('window-size=500,500')  # para o caso da janela aparecer...

    options.add_experimental_option("prefs", {  # evita dialogo para salvar arquivo...
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # vai abrir o navegador do Chrome escondido do usuario:
    logger.debug("Iniciando WebDriver do Chrome com Options:\n%s\n%s",
                 options.arguments, options.experimental_options)
    browser = None
    try:
        browser = webdriver.Chrome(chrome_options=options)

        # apos ativar o driver do chrome, configura sua execucao:
        browser.minimize_window()  # melhor minimizar...
        browser.implicitly_wait(timeout_download)  # timeout para aguardar o site carregar.
        logger.info("WebDriver do Chrome inicializado com sucesso.")

    except WebDriverException as ex:
        # o WebDriver do Chrome pode nao estar instalado ou presente no PATH:
        logger.error("Erro ao tentar inicializar o WebDriver do Chrome:\n  %s", repr(ex))

    return browser

# ----------------------------------------------------------------------------
