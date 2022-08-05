"""
   Package .
   Module  test_loterias.py

   Modulo Suite para teste dos jobs e demais funcionalidades do Infinite.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from infinite.jobs.caixa.download_loterias_caixa import DownloadLoteriasCaixa


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

def test_job():
    DownloadLoteriasCaixa().run_job()
