"""
   Package .
   Module  __main__.py

   Modulo principal do aplicativo Infinite, entry-point para execucao de
   tarefas individuais ou pelo agendador utilitario do Python (lib schedule).
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import sys
import getopt
import logging

# Libs/Frameworks modules
# Own/Project modules
from infinite.conf import settings
from infinite import scheduler_bolsas
from infinite import scheduler_loterias
from infinite import scheduler_apostas


# ----------------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------------

# argumentos da linha de comando:
CMD_LINE_ARGS = "blac:t:"

# Possiveis erros que podem ocorrer na execucao da aplicacao para retorno no sys.exit():
EXIT_ERROR_INVALID_ARGS = 1
EXIT_ERROR_NO_ARGS = 2
EXIT_ERROR_CONFIG_LOGGING = 3
EXIT_ERROR_CONFIG_INI = 4
EXIT_ERROR_MAIN = "O modulo '__main__.py' nao pode ser carregado por outro modulo!"

EXIT_SUCCESS = 0  # informa que na verdade nao ocorreu erro, executou com sucesso.


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# Este modulo nao pode ser carregado por outro modulo
if __name__ != '__main__':
    sys.exit(EXIT_ERROR_MAIN)
# prossegue somente se este programa foi executado como entry-point...


# ----------------------------------------------------------------------------
# ARGUMENTOS DE LINHA DE COMANDO
# ----------------------------------------------------------------------------

# exibe ao usuario a forma correta de execucao do programa:
def print_usage():
    print('\n'
          'Uso:\n'
          '  python infinite.zip [opcoes]\n'
          '\n'
          'Opcoes Gerais:\n'
          '  -b          Agenda as tarefas para Bolsas de Valores\n'
          '  -l          Agenda as tarefas para Loterias da Caixa\n'
          '  -a          Agenda as tarefas para Apostas Esportivas\n'
          '  -c <path>   Informa o path para os arquivos de configuracao\n'
          '  -t <job>    Executa teste de funcionamento de algum job\n')


# faz o parsing das opcoes e argumentos da linha de comando:
opts = None
try:
    # se parsing feito com sucesso - programa ira prosseguir:
    opts, args = getopt.getopt(sys.argv[1:], CMD_LINE_ARGS)

except getopt.GetoptError as ex:
    print("Erro no parsing dos argumentos da linha de comando:", repr(ex))
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_INVALID_ARGS)  # aborta apos avisar usuario

# se nenhuma opcao de execucao foi fornecida na linha de comando:
if (opts is None) or (len(opts) == 0):
    print("Erro no parsing dos argumentos da linha de comando...")
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)  # nao ha porque prosseguir...

# comandos e opcoes de execucao:
opt_bolsav = False   # Flag para tarefas relativas a bolsas de valores
opt_lotocx = False   # Flag para tarefas relativas a loterias da caixa
opt_aposte = False   # Flag para tarefas relativas a apostas esportivas
opt_cfpath = ''      # path para os arquivos de configuracao
opt_testef = False   # Flag para teste de funcionamento
opt_tstjob = ''      # id do job a ser executado para testes

# identifica o comando/tarefa/job do Infinite a ser executado:
for opt, val in opts:
    if opt == '-b':
        opt_bolsav = True
    elif opt == '-l':
        opt_lotocx = True
    elif opt == '-a':
        opt_aposte = True
    elif opt == '-c':
        opt_cfpath = val
    elif opt == '-t':
        opt_testef = True
        opt_tstjob = val

# valida o path para os arquivos de configuracao:
if len(opt_cfpath) == 0:
    opt_cfpath = '.'  # utiliza o proprio diretorio do executavel.


# ----------------------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------------------

# verifica se conseguiu fazer a configuracao do logging:
if not settings.setup_logging(opt_cfpath):
    print("Erro ao configurar o logging da aplicacao...")
    sys.exit(EXIT_ERROR_CONFIG_LOGGING)  # nao ha porque prosseguir...

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)
logger.info("O logging foi configurado com sucesso para a aplicacao.")


# ----------------------------------------------------------------------------
# SETTINGS
# ----------------------------------------------------------------------------

# verifica se conseguiu fazer a leitura do arquivo de configuracao INI:
if not settings.setup_config(opt_cfpath):
    logger.critical("Execucao da aplicacao foi interrompida.")
    sys.exit(EXIT_ERROR_CONFIG_INI)  # aborta se nao puder carregar INI

# tudo ok, prossegue entao com o processamento:
logger.info("Aplicacao configurada e inicializada com sucesso.")
logger.debug("Argumentos da linha de comando: " + str(opts).strip('[]'))


# ----------------------------------------------------------------------------
# TESTES
# ----------------------------------------------------------------------------

# Rotina de testes:
if opt_testef:
    if opt_tstjob == 'lc':
        import test_loterias as suite
        logger.info("Vai executar suite de testes do job 'DownloadLoteriasCaixa'...")
        suite.test_job()
        logger.info("Suite de testes do job 'DownloadLoteriasCaixa' foi executado.")
    else:
        # Informa que tudo ok ate aqui, Infinite funcionando normalmente:
        logger.info("Modulo main() executado com sucesso! opt_testef = %s", opt_testef)

    # aborta o processamento se esta apenas testando:
    sys.exit(EXIT_SUCCESS)


# ----------------------------------------------------------------------------
# STARTUP
# ----------------------------------------------------------------------------

# configura as tarefas no scheduler de acordo com as opcoes de execucao:
if opt_bolsav:  # bolsas de valores
    logger.debug("Vai iniciar o scheduler para tarefas relativas a Bolsas de Valores...")
    # Executa o scheduler para agendar as respectivas tarefas (jobs)
    sys.exit(scheduler_bolsas.main())

elif opt_lotocx:  # loterias da caixa
    logger.debug("Vai iniciar o scheduler para tarefas relativas a Loterias da Caixa...")
    # Executa o scheduler para agendar as respectivas tarefas (jobs)
    sys.exit(scheduler_loterias.main())

elif opt_aposte:  # apostas esportivas
    logger.debug("Vai iniciar o scheduler para tarefas relativas a Apostas Esportivas...")
    # Executa o scheduler para agendar as respectivas tarefas (jobs)
    sys.exit(scheduler_apostas.main())

# se a opcao de execucao fornecida na linha de comando nao foi reconhecida:
else:
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)

# ----------------------------------------------------------------------------
