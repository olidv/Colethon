
* Em 02/09/2022 gastou de 04:36 a 06:14 para executar todos os jobs: 1h38min.

Após mudança no scheduler:
    * Em 03/09/2022 gastou de 05:18 a 06:04 para executar todos os jobs: 0h46min.

Renomeado projeto para Colethon. Infinite é o nome de toda a plataforma financeira.

--- PENDENTE --------------------------------------------------------

Mover job de baixar de resultados de loterias para tarefas lotéricas.

Adotar "async def" nos métodos de jobs.

Criar novo job para alertar para vencimentos de ativos como mini índices e opções.
    Indicar próximos ativos a serem negociados apos vencimento e dia/data da troca.

Criar novo job para baixar as cotações dos índices das principais bolsas no mundo.

Criar novo job para baixar as cotações de commodities no mundo inteiro.
Criar novo job para download de todas as comodities que afetem a bolsa no brasil.
    Milho, Soja, Café, Boi Gordo, Barril de Petróleo, Minério

Criar tela principal com o Qt Designer - parar de usar DOS shell.

Apos a aplicação atingir maturidade, desligar o logging dos frameworks.
    loggers:
      schedule:
        level: ERROR
      selenium:
        level: ERROR
      urllib3:
        level: ERROR
    

--- OK --------------------------------------------------------------

Substituir level CRITICAL por FATAL.

Criar classe ancestral e aplicar POO nos jobs
    substituir o "duck typing" no scheduler.

Incluir arquivo de controle em todos os jobs
    se já executou no dia, nem arquivo de log copia...

Mover os arquivos de logging, para não deixar acumular na estação Dell.
    Logging do InFiniTe e Digital-Clock.

Criar novo job de manutenção para apagar logs antigos
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

---------------------------------------------------------------------
