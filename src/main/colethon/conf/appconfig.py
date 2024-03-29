"""
   Package colethon.conf
   Module  appconfig.py

   Carga das configuracoes da aplicacao a partir de arquivo INI.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass
from configparser import ConfigParser


# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE
# ----------------------------------------------------------------------------

@dataclass
class AppConfig:
    """
       Classe contendo toda a configuracao INI da aplicacao.
    """

    # Estrutura de diretorios da aplicacao:
    RT_app_home: str = ''
    RT_data_path: str = ''
    RT_lib_path: str = ''
    RT_log_path: str = ''
    RT_www_path: str = ''
    RT_tmp_path: str = ''

    RT_mt5_platform_home: str = ''
    RT_mt5_terminal_home: str = ''
    RT_mt5_terminal_commons: str = ''
    RT_mt5_terminal_mql5_files: str = ''
    RT_mt5_instances_id: list[tuple[str, ...]] = None

    RT_files_csv_mask: str = ''
    RT_files_htm_mask: str = ''
    RT_files_zip_mask: str = ''
    RT_files_all_mask: str = ''

    # Parametrizacao do scheduler utilizado para o agendamento de jobs:
    SC_time_wait: int = 0

    # Parametrizacao do site de loterias da Caixa EF:
    CX_uri_site: str = ''
    CX_uri_port: int = 0
    CX_timeout_loadpage: int = 0
    CX_timeout_download: int = 0

    # Parametrizacao das loterias da Caixa EF:
    LC_job_interval: int = 0
    LC_caixa_loterias_url: list[tuple[str, ...]] = None
    LC_xpath_concurso: str = ''
    LC_xpath_dezenas: str = ''
    LC_text_resultado: str = ''
    LC_loterias_htm_mask: str = ''
    LC_loteria_htm_name: str = ''
    LC_ctrl_file_mask: str = ''

    # Parametrizacao dos processamentos das loterias:
    JC_job_interval: int = 0
    JC_table_class_find: str = ''
    JC_sorteios_csv_name: str = ''
    JC_jlothon_batch: str = ''
    JC_ctrl_file_mask: str = ''

    # Parametrizacao do mercado da bolsa B3:
    B3_uri_site: str = ''
    B3_uri_port: int = 0
    B3_timeout_loadpage: int = 0
    B3_timeout_download: int = 0
    B3_feriados_bolsa: list[tuple[int, ...]] = None

    # Parametrizacao do job para baixa da Carteira Teorica do IBovespa:
    CI_job_interval: int = 0
    CI_url_carteira_ibov: str = ''
    CI_xpath_a_click: str = ''
    CI_ibov_csv_mask: str = ''
    CI_derivativos: list[str] = None
    CI_ibov_txt_name: str = ''
    CI_ctrl_file_mask: str = ''

    # Parametrizacao do job para baixa das Cotacoes IntraDay da B3:
    IB_job_interval: int = 0
    IB_url_cotacoes_intraday: str = ''
    IB_intraday_url_mask: str = ''
    IB_intraday_zip_mask: str = ''
    IB_intraday_zip_name: str = ''
    IB_ctrl_file_mask: str = ''

    # Parametrizacao do job para compactar arquivos CSV nos terminais MT5:
    ZM_job_interval: int = 0
    ZM_ctrl_file_mask: str = ''

    # Parametrizacao do job para copiar/mover arquivos para outra estacao:
    MI_job_interval: int = 0
    MI_local_folder: str = ''
    MI_shared_folder: str = ''
    MI_lothon_data: str = ''
    MI_lothon_data_caixa: str = ''
    MI_lothon_data_cache: str = ''
    MI_sorteios_csv_mask: str = ''
    MI_jogos_csv_mask: str = ''
    MI_quanthon_data: str = ''
    MI_quanthon_data_mtrader5: str = ''
    MI_quanthon_data_ibovespa: str = ''
    MI_quanthon_data_cotacoes: str = ''
    MI_ctrl_file_mask: str = ''
    MI_temp_safe_del: str = ''

    # Parametrizacao do mercado de FOREX:
    FX_feriados_forex: list[tuple[int, ...]] = None

    # .
    def load_properties(self, parser: ConfigParser) -> None:
        # nao faz nada se nao forneceu o parser...
        if parser is None:
            return

        # com o parser, carrega o arquivo INI nos parametros da dataclass:
        self.RT_app_home = parser.get("ROOT", "app_home")
        self.RT_data_path = parser.get("ROOT", "data_path")
        self.RT_lib_path = parser.get("ROOT", "lib_path")
        self.RT_log_path = parser.get("ROOT", "log_path")
        self.RT_www_path = parser.get("ROOT", "www_path")
        self.RT_tmp_path = parser.get("ROOT", "tmp_path")

        self.RT_mt5_platform_home = parser.get("ROOT", "mt5_platform_home")
        self.RT_mt5_terminal_home = parser.get("ROOT", "mt5_terminal_home")
        self.RT_mt5_terminal_commons = parser.get("ROOT", "mt5_terminal_commons")
        self.RT_mt5_terminal_mql5_files = parser.get("ROOT", "mt5_terminal_mql5_files")
        instances = parser.get("ROOT", "mt5_instances_id").split(',')
        self.RT_mt5_instances_id = [tuple(i.strip().split(';')) for i in instances]

        self.RT_files_csv_mask = parser.get("ROOT", "files_csv_mask")
        self.RT_files_htm_mask = parser.get("ROOT", "files_htm_mask")
        self.RT_files_zip_mask = parser.get("ROOT", "files_zip_mask")
        self.RT_files_all_mask = parser.get("ROOT", "files_all_mask")

        # Parametrizacao do scheduler utilizado para o agendamento de jobs:
        self.SC_time_wait = parser.getint("SCHEDULER", "time_wait")

        # Parametrizacao do site de loterias da Caixa EF:
        self.CX_uri_site = parser.get("CAIXA", "uri_site")
        self.CX_uri_port = parser.getint("CAIXA", "uri_port")
        self.CX_timeout_loadpage = parser.getint("CAIXA", "timeout_loadpage")
        self.CX_timeout_download = parser.getint("CAIXA", "timeout_download")

        # Parametrizacao do job para download dos resultados das loterias da Caixa EF:
        self.LC_job_interval = parser.getint("LOTERIA_CAIXA", "job_interval")
        self.LC_xpath_concurso = parser.get("LOTERIA_CAIXA", "xpath_concurso")
        self.LC_xpath_dezenas = parser.get("LOTERIA_CAIXA", "xpath_dezenas")
        self.LC_text_resultado = parser.get("LOTERIA_CAIXA", "text_resultado")
        self.LC_loterias_htm_mask = parser.get("LOTERIA_CAIXA", "loterias_htm_mask")
        self.LC_loteria_htm_name = parser.get("LOTERIA_CAIXA", "loteria_htm_name")
        self.LC_ctrl_file_mask = parser.get("LOTERIA_CAIXA", "ctrl_file_mask")

        loterias = parser.get("LOTERIA_CAIXA", "caixa_loterias_url").split(',')
        self.LC_caixa_loterias_url = [tuple(link.strip().split(';')) for link in loterias]

        # Parametrizacao do job para processamento dos sorteios das loterias:
        self.JC_job_interval = parser.getint("JOGO_COMPUTADO", "job_interval")
        self.JC_table_class_find = parser.get("JOGO_COMPUTADO", "table_class_find")
        self.JC_sorteios_csv_name = parser.get("JOGO_COMPUTADO", "sorteios_csv_name")
        self.JC_jlothon_batch = parser.get("JOGO_COMPUTADO", "jlothon_batch")
        self.JC_ctrl_file_mask = parser.get("JOGO_COMPUTADO", "ctrl_file_mask")

        # Parametrizacao do acesso ao web site da B3:
        self.B3_uri_site = parser.get("B3", "uri_site")
        self.B3_uri_port = parser.getint("B3", "uri_port")
        self.B3_timeout_loadpage = parser.getint("B3", "timeout_loadpage")
        self.B3_timeout_download = parser.getint("B3", "timeout_download")

        datas = parser.get("B3", "feriados_bolsa").split(',')
        self.B3_feriados_bolsa = [tuple(map(int, dia.split('/'))) for dia in datas]

        # Parametrizacao do job para baixa da Carteira Teorica do IBovespa:
        self.CI_job_interval = parser.getint("CARTEIRA_IBOVESPA", "job_interval")
        self.CI_url_carteira_ibov = parser.get("CARTEIRA_IBOVESPA", "url_carteira_ibov")
        self.CI_xpath_a_click = parser.get("CARTEIRA_IBOVESPA", "xpath_a_click")
        self.CI_ibov_csv_mask = parser.get("CARTEIRA_IBOVESPA", "ibov_csv_mask")
        self.CI_derivativos = parser.get("CARTEIRA_IBOVESPA", "derivativos").split(',')
        self.CI_ibov_txt_name = parser.get("CARTEIRA_IBOVESPA", "ibov_txt_name")
        self.CI_ctrl_file_mask = parser.get("CARTEIRA_IBOVESPA", "ctrl_file_mask")

        # Parametrizacao do job para baixa das Cotacoes IntraDay da B3:
        self.IB_job_interval = parser.getint("INTRADAY_B3", "job_interval")
        self.IB_url_cotacoes_intraday = parser.get("INTRADAY_B3", "url_cotacoes_intraday")
        self.IB_intraday_url_mask = parser.get("INTRADAY_B3", "intraday_url_mask")
        self.IB_intraday_zip_mask = parser.get("INTRADAY_B3", "intraday_zip_mask")
        self.IB_intraday_zip_name = parser.get("INTRADAY_B3", "intraday_zip_name")
        self.IB_ctrl_file_mask = parser.get("INTRADAY_B3", "ctrl_file_mask")

        # Parametrizacao do job para compactar arquivos CSV nos terminais MT5:
        self.ZM_job_interval = parser.getint("ZIP_MQL5", "job_interval")
        self.ZM_ctrl_file_mask = parser.get("ZIP_MQL5", "ctrl_file_mask")

        # Parametrizacao do job para copiar/mover arquivos para outra estacao:
        self.MI_job_interval = parser.getint("MOVE_INTRANET", "job_interval")

        self.MI_local_folder = parser.get("MOVE_INTRANET", "local_folder")
        self.MI_shared_folder = parser.get("MOVE_INTRANET", "shared_folder")

        self.MI_lothon_data = parser.get("MOVE_INTRANET", "lothon_data")
        self.MI_lothon_data_caixa = parser.get("MOVE_INTRANET", "lothon_data_caixa")
        self.MI_lothon_data_cache = parser.get("MOVE_INTRANET", "lothon_data_cache")
        self.MI_sorteios_csv_mask = parser.get("MOVE_INTRANET", "sorteios_csv_mask")
        self.MI_jogos_csv_mask = parser.get("MOVE_INTRANET", "jogos_csv_mask")

        self.MI_quanthon_data = parser.get("MOVE_INTRANET", "quanthon_data")
        self.MI_quanthon_data_mtrader5 = parser.get("MOVE_INTRANET", "quanthon_data_mtrader5")
        self.MI_quanthon_data_ibovespa = parser.get("MOVE_INTRANET", "quanthon_data_ibovespa")
        self.MI_quanthon_data_cotacoes = parser.get("MOVE_INTRANET", "quanthon_data_cotacoes")

        self.MI_ctrl_file_mask = parser.get("MOVE_INTRANET", "ctrl_file_mask")
        self.MI_temp_safe_del = parser.get("MOVE_INTRANET", "temp_safe_del")

        # Parametrizacao do mercado de FOREX:
        datas = parser.get("FOREX", "feriados_forex").split(',')
        self.FX_feriados_forex = [tuple(map(int, dia.split('/'))) for dia in datas]

# ----------------------------------------------------------------------------
