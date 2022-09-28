"""
   Package colethon.jobs
   Module  abstract_job.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE JOB
# ----------------------------------------------------------------------------

class AbstractJob(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de jobs.
    """

    @property
    @abstractmethod
    def job_id(self) -> str:
        """
        Tag de identificacao do job, para agendamento e cancelamento.

        :return: Retorna o id do job, unico entre todos os jobs do Colethon, normalmente
        uma sigla de 2 ou 3 letras em maiusculo.
        """
        pass

    @property
    @abstractmethod
    def job_interval(self) -> int:
        """
        Obtem a parametrizacao do intervalo de tempo, em minutos, para o scheduler.

        :return: Medida de tempo para parametrizar o job no scheduler, em minutos.
        """
        pass

    @abstractmethod
    def run_job(self, callback_func=None) -> None:
        """
        Rotina de processamento do job, a ser executada quando o scheduler ativar o job.

        :param callback_func: Funcao de callback a ser executada ao final do processamento
        do job.
        """
        pass
