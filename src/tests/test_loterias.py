"""
   Package .
   Module  test_loterias.py

   Modulo Suite para teste dos jobs e demais funcionalidades do Colethon.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from colethon.jobs.caixa.download_loterias_caixa import DownloadLoteriasCaixa


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

def test_job():
    DownloadLoteriasCaixa().run_job()
