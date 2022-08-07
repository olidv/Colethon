"""
   Package infinite.jobs
   Module  compute_sorteios_loterias.py
   ...
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
import glob
import csv
import subprocess
import logging

# Libs/Frameworks modules
from bs4 import BeautifulSoup
from bs4.element import ResultSet

# Own/Project modules
from infinite.util.eve import *
from infinite.conf import app_config
from infinite.jobs import commons
from infinite.jobs.abstract_job import AbstractJob


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# identificacao da tag de cada loteria:
TAGS_LOTERIAS: dict[str: str] = {
    'diadesorte': 'd',
    'duplasena': 'p',
    'lotofacil': 'l',
    'lotomania': 'n',
    'quina': 'q',
    'megasena': 'm',
    'supersete': 's',
    'timemania': 't'
}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# relaciona os arquivos HTM referentes as loterias que foram baixadas do site da Caixa:
def list_files_loterias() -> list[str]:
    # e identifica o path dos arquivos das loterias a serem processados:
    loterias_htm_path = os.path.join(app_config.RT_www_path, app_config.LC_loteria_htm_mask)

    # verifica se ha arquivos D_*.HTM baixados so site da Caixa:
    files_htm_contents = glob.glob(loterias_htm_path)
    len_htm_contents = len(files_htm_contents)
    if len_htm_contents > 0:
        logger.debug("Encontrados %d arquivos de loterias para processamento dos sorteios.",
                     len_htm_contents)
    else:
        logger.debug("Nenhum arquivo '%s' de loteria encontrado para processamento dos sorteios.",
                     app_config.LC_loteria_htm_mask)

    return files_htm_contents


# identifica o id, nome e tag da loteria:
def get_id_loteria(file_loteria: str) -> tuple[str, str, str]:
    # extrai o nome do arquivo para extrair a identificacao da loteria:
    file_name: str = os.path.basename(file_loteria)
    len_file_name: int = len(file_name)

    # o formato do arquivo da loteria eh:   D_??????.HTM
    nome_loteria = file_name[2:len_file_name-4]
    id_loteria = nome_loteria.lower().replace('-', '')
    tag_loteria: str = TAGS_LOTERIAS[id_loteria]  # a partir do id da loteria, identifica sua tag
    return id_loteria, nome_loteria, tag_loteria


# le arquivo de resultados e retorna conteudo HTML:
def ler_arquivo_htm(path_arquivo: str) -> str:
    logger.debug(f"Vai abrir para leitura o arquivo texto '{path_arquivo}'.")
    with open(path_arquivo, "rt", encoding='utf-8') as htm:
        content_htm = htm.read()

    if len(content_htm) == 0:
        logger.warning(f"Este arquivo HTM de resultados esta vazio: '{path_arquivo}'")
    else:
        file_size = os.path.getsize(path_arquivo)
        logger.debug(f"Leitura do arquivo '{path_arquivo}' realizada com sucesso: "
                     f"{formatb(file_size)} bytes lidos.")

    return content_htm


#
def parse_sorteio(id_loteria: str, td: ResultSet, list_sorteios: list[tuple[int, ...]]):
    # a localizacao das bolas sorteadas depende da loteria:
    if id_loteria == 'diadesorte':
        bolas: tuple[int, ...] = (int(td[3].text), int(td[4].text),
                                  int(td[5].text), int(td[6].text),
                                  int(td[7].text), int(td[8].text),
                                  int(td[9].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))

    elif id_loteria == 'duplasena':
        bolas1: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                   int(td[4].text), int(td[5].text),
                                   int(td[6].text), int(td[7].text))
        bolas2: tuple[int, ...] = (int(td[20].text), int(td[21].text),
                                   int(td[22].text), int(td[23].text),
                                   int(td[24].text), int(td[25].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas1)))
        list_sorteios.append(tuple(sorted(bolas2)))

    elif id_loteria == 'lotofacil':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text), int(td[9].text),
                                  int(td[10].text), int(td[11].text),
                                  int(td[12].text), int(td[13].text),
                                  int(td[14].text), int(td[15].text),
                                  int(td[16].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))

    elif id_loteria == 'lotomania':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text), int(td[9].text),
                                  int(td[10].text), int(td[11].text),
                                  int(td[12].text), int(td[13].text),
                                  int(td[14].text), int(td[15].text),
                                  int(td[16].text), int(td[17].text),
                                  int(td[18].text), int(td[19].text),
                                  int(td[20].text), int(td[21].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))

    elif id_loteria == 'megasena':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))

    elif id_loteria == 'quina':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))

    elif id_loteria == 'supersete':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text))
        # aqui nao pode ordenar as bolas:
        list_sorteios.append(bolas)

    elif id_loteria == 'timemania':
        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text))
        # garante a ordenacao das bolas:
        list_sorteios.append(tuple(sorted(bolas)))


# efetua leitura do arquivo da loteria e carrega os sorteios
def load_sorteios_loteria(id_loteria: str, nome_loteria: str,
                          file_loteria: str) -> list[tuple[int, ...]]:
    # efetua leitura dos resultados da loteria, verificando se o arquivo existe na pasta 'data'.
    logger.info(f"Iniciando a carga dos concursos da loteria '{nome_loteria}' / '{id_loteria}.")
    content_htm = ler_arquivo_htm(file_loteria)
    # logger.debug(f"content_htm = {content_htm}")
    if content_htm is None or len(content_htm) == 0:
        logger.error(f"Nao foi possivel carregar os resultados da loteria '{nome_loteria}'.")
        return []
    else:
        logger.info(f"Foram lidos {formatb(len(content_htm))} caracteres do arquivo de "
                    f"resultados da loteria '{nome_loteria}'.")

    # carrega no BeautifulSoup o HTML contendo uma <TABLE> de resultados:
    logger.debug(f"Vai efetuar o parsing do conteudo HTML de resultados da "
                 f"loteria '{nome_loteria}'.")
    soup = BeautifulSoup(content_htm, 'html.parser')
    # logger.debug(f"soup.prettify() = {soup.prettify()}")

    # pesquisa o elemento <TABLE> contendo a relacao de resultados / concursos da loteria:
    table_class = app_config.JC_table_class_find.format(id_loteria)
    # formato do HTML atual:  <table class="tabela-resultado supersete">
    table = soup.find("table", {"class": table_class})
    # logger.debug(f"len(table) = {len(table)}")
    if table is None or len(table) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return []
    else:
        logger.info(f"Parsing do arquivo HTM da loteria '{nome_loteria}' efetuado com sucesso.")

    # cada linha de resultado/concurso esta envolta em um TBODY:
    table_body = table.find_all("tbody", recursive=False)
    # logger.debug(f"len(table_body) = {len(table_body)}")
    if table_body is None or len(table_body) == 0:
        logger.fatal(f"*** ATENCAO: O formato do arquivo HTM da loteria "
                     f"'{nome_loteria}' foi modificado! ***")
        return []
    else:
        logger.info(f"Encontradas #{len(table_body)} linhas de resultados no arquivo HTM da "
                    f"loteria '{nome_loteria}'.")

    # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
    list_sorteios: list[tuple[int, ...]] = []
    for tbody in table_body:
        tr = tbody.find("tr", recursive=False)
        # logger.debug(f"tr = {type(tr)} {len(tr)}")
        td = tr.find_all("td", recursive=False)
        # logger.debug(f"td = {type(td)} {len(td)}")
        # logger.debug(f"td[0] = {type(td[0])} {len(td[0])} {td[0].text}")
        parse_sorteio(id_loteria, td, list_sorteios)

    return list_sorteios


# exporta os sorteios da loteria em arquivo CSV, para comunicacao com o jLothon:
def export_sorteios_loteria(nome_loteria: str, list_sorteios: list[tuple[int, ...]]) -> int:
    # cria arquivo fisico para conter apenas as dezenas sorteadas:
    loteria_sorteios_file: str = app_config.JC_sorteios_csv_name.format(nome_loteria)
    loteria_sorteios_path: str = os.path.join(app_config.RT_www_path, loteria_sorteios_file)

    # abre arquivo para escrita e salva todas as dezenas sorteadas:
    qt_rows: int = 0
    with open(loteria_sorteios_path, 'w', newline='', encoding='utf-8') as file_csv:
        # o conteudo do arquivo sera formatado como CSV padrao:
        csv_writer = csv.writer(file_csv)

        # percorre lista de concursos e exporta as bolas:
        for sorteio in list_sorteios:
            # salva as dezenas separadas por virgula:
            csv_writer.writerow(sorteio)
            qt_rows += 1

    # informa quantas linhas de sorteios foram gravadas:
    return qt_rows


def executar_jlothon(tag_loteria: str) -> bool | None:
    # somente executa rotina Java para processamento e geracao dos jogos computados das loterias:
    # Dia de Sorte, Dupla Sena, Lotofacil, Mega-Sena e Quina.
    if tag_loteria not in "dplmq":
        return None

    # indica a loteria para o jLothon como argumento do script batch:
    jlothon: str = app_config.JC_jlothon_batch.format(app_config.RT_www_path, tag_loteria)
    workdir: str = app_config.RT_lib_path
    try:
        # executa o programa jLothon para processar os jogos da loteria indicada:
        exit_code: int = subprocess.call(jlothon, cwd=workdir)

        # informa True se foi executado com sucesso ou False caso contrario.
        return exit_code == 0

    # qualquer erro significa que nao pode executar o programa jLothon:
    except (subprocess.CalledProcessError, OSError) as err:
        logger.critical(f"Erro ao tentar executar o jLothon para a loteria '{tag_loteria}'.\n"
                        f"\tComando executado: {workdir} / {jlothon} \n"
                        f"\tERRO: {repr(err)}")
        return False


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class ComputeSorteiosLoterias(AbstractJob):
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
        return "JOGO_COMPUTADO"

    @property
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        interval = app_config.JC_job_interval
        return interval

    # --- METODOS DE INSTANCIA -----------------------------------------------

    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        _startWatch = startwatch()
        logger.info("Iniciando job '%s' para processamento e filtro dos sorteios das loterias.",
                    self.job_id)

        # gera o nome do arquivo de controle para a data de hoje.
        ctrl_file_job = commons.arquivo_controle(app_config.JC_ctrl_file_mask)
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

        # identifica os arquivos das loterias da Caixa que ja foram baixados no job anterior:
        files_loterias: list[str] = list_files_loterias()
        # verifica se ha arquivos a processar:
        if len(files_loterias) == 0:  # testa soh por garantia.
            logger.error("Nao ha arquivos de loterias da Caixa baixados para processamento.")
            if callback_func is not None:
                callback_func(self.job_id)
            return  # ao cancelar o job, nao sera mais executado novamente.

        # percorre lista de arquivos de loterias para processar os sorteios
        for file_name in files_loterias:
            # primeiro extrai a identificacao da loteria pelo nome de seu arquivo:
            id_loteria, nome_loteria, tag_loteria = get_id_loteria(file_name)

            # em seguida carrega o arquivo da loteria e faz o parser dos sorteios:
            list_sorteios: list[tuple[int, ...]] = load_sorteios_loteria(id_loteria, nome_loteria,
                                                                         file_name)
            # valida se a loteria possui sorteios a serem exportados:
            if list_sorteios is None or len(list_sorteios) == 0:
                continue
            logger.debug(f"{nome_loteria}: Carregou #{len(list_sorteios)} sorteios do "
                         f"arquivo: '{file_name}'.")

            # com os sorteios, exporta o arquivo CSV com as dezenas sorteadas da loteria:
            qtd_export: int = export_sorteios_loteria(nome_loteria, list_sorteios)
            logger.debug(f"{nome_loteria}: Foram exportados #{formatd(qtd_export)} sorteios da "
                         f"loteria em arquivo CSV.")

            # ao final, executa rotina Java para processamento e geracao dos jogos computados:
            run_ok: bool = executar_jlothon(tag_loteria)
            if run_ok is None:
                logger.debug(f"{nome_loteria}: Programa jLothon ainda nao processa essa loteria.")
            elif run_ok:
                logger.debug(f"{nome_loteria}: Programa jLothon foi executado com sucesso.")
            else:
                logger.error(f"{nome_loteria}: Erro na execucao do programa jLothon. "
                             f"Geracao de jogos computados abortada.")

        # salva arquivo de controle vazio para indicar que o job foi concluido com sucesso.
        open(ctrl_file_job, 'a').close()
        logger.debug("Criado arquivo de controle '%s' para indicar que job foi concluido.",
                     ctrl_file_job)

        # vai executar este job apenas uma vez, se for finalizado com sucesso:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Finalizado job '{self.job_id}' para processamento dos sorteios das loterias "
                    f"da Caixa EF. Tempo gasto: {_stopWatch}")
        if callback_func is not None:
            callback_func(self.job_id)

# ----------------------------------------------------------------------------
