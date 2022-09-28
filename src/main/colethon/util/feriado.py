"""
   Package colethon.util
   Module  feriado.py

   Funcoes utilitarias para verificar se uma data eh feriado no Forex ou na bolsa.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date

# Libs/Frameworks modules
# Own/Project modules
from colethon.conf import app_config


# ----------------------------------------------------------------------------
# DIAS DA SEMANA
# ----------------------------------------------------------------------------

# tupla com descricao dos dias da semana:
WEEK_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",  # Dias Uteis
             "Saturday", "Sunday")                                    # Final de semana

# constantes para cada dia da semana:
MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


# verifica se o dia eh final de semana (sabado ou domingo)
def is_final_semana(dia: int) -> bool:
    if dia is None:
        return False

    return (dia == SATURDAY) or (dia == SUNDAY)  # 5 = sabado, 6 = domingo


# ----------------------------------------------------------------------------
# FOREX - MERCADO INTERNACIONAL
# ----------------------------------------------------------------------------

# verifica se o dia/mes eh feriado no mercado internacional:
def is_feriado_forex(dia: int, mes: int) -> bool:
    if (dia is None) or (mes is None):
        return False

    for (diaf, mesf) in app_config.FX_feriados_forex:
        if dia == diaf and mes == mesf:
            return True

    return False


# verifica se a data eh dia util no mercado internacional:
def is_dia_util_forex(data: date) -> bool:
    if data is None:
        return False

    dia = data.day
    mes = data.month
    wdia = data.weekday()

    # sera dia util se nao for sabado e nem feriado:
    return not ((wdia == SATURDAY) or is_feriado_forex(dia, mes))


# ----------------------------------------------------------------------------
# BOLSA - MERCADO NACIONAL
# ----------------------------------------------------------------------------

# verifica se o dia/mes eh feriado no mercado nacional:
def is_feriado_bolsa(dia: int, mes: int) -> bool:
    if (dia is None) or (mes is None):
        return False

    for (diaf, mesf) in app_config.B3_feriados_bolsa:
        if dia == diaf and mes == mesf:
            return True

    return False


# verifica se a data eh dia util no mercado nacional:
def is_dia_util_bolsa(data: date) -> bool:
    if data is None:
        return False

    dia = data.day
    mes = data.month
    wdia = data.weekday()

    # sera dia util se nao for final de semana e nem feriado:
    return not (is_final_semana(wdia) or is_feriado_bolsa(dia, mes))

# ----------------------------------------------------------------------------
