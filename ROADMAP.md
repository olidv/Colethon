
Substituir level CRITICAL por FATAL.

Criar classe ancestral e aplicar POO nos jobs
    substituir o "duck typing" no scheduler.

Incluir arquivo de controle em todos os jobs
    se j� executou no dia, nem arquivo de log copia...

Mover os arquivos de logging, para n�o deixar acumular na esta��o Dell.
    Logging do InFiniTe e Digital-Clock.

Criar novo job de manuten��o para apagar logs antigos
    apagar arquivos de controle de dias anteriores (\infinite\temp\*), etc...

Criacao de arquivo safeToDelete.tmp ao final do job move-files-intranet.

Criar novo job para download dos arquivos de resultados das loterias da caixa.
    dia de sorte:  http://loterias.caixa.gov.br/wps/portal/loterias/landing/diadesorte
    megasena:      http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena
    quina:         http://loterias.caixa.gov.br/wps/portal/loterias/landing/quina
    timemania:     http://loterias.caixa.gov.br/wps/portal/loterias/landing/timemania
    lotomania:     http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotomania
    dupla-sena:    http://loterias.caixa.gov.br/wps/portal/loterias/landing/duplasena
    lotofacil:     http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil

Incluir zip do diretorio \dist\*.* no InFiniTe.
    <app>.zip


--- OK --------------------------------------------------------------


Criar novo job para alertar para vencimentos de ativos como mini �ndices e op��es.
    Indicar pr�ximos ativos a serem negociados apos vencimento e dia/data da troca.

Criar novo job para baixar as cota��es dos �ndices das principais bolsas no mundo.

Criar novo job para baixar as cota��es de commodities no mundo inteiro.
Criar novo job para download de todas as comodities que afetem a bolsa no brasil.
    Milho, Soja, Caf�, Boi Gordo, Barril de Petr�leo, Min�rio

Criar tela principal com o Qt Designer - parar de usar DOS shell.

Adotar "async def" nos m�todos de jobs.

??? Mudar o codename de cada job para 3 letras ao gerar arquivo de controle (\temp) ???

Apos a aplica��o atingir maturidade, desligar o logging dos frameworks.
    loggers:
      schedule:
        level: ERROR
      selenium:
        level: ERROR
      urllib3:
        level: ERROR
    
---------------------------------------------------------------------
