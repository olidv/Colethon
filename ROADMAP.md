
--- PENDENTE --------------------------------------------------------

Ajustar os intervalos de execucao dos jobs para evitar conflitos entre baixar loterias e cotacoes.

Printar no log um ALERTA para quando precisar atualizar o WebDriver:
    2022-04-29 04:59:04,585 ERROR [Thread-3 (run_job)] infinite.jobs.commons->open_webdriver_chrome<113>  Erro ao tentar inicializar o WebDriver do Chrome:
      WebDriverException('chrome not reachable', None, ['Backtrace:', '\tOrdinal0 [0x01527413+2389011]', '\tOrdinal0 [0x014B9F61+1941345]', '\tOrdinal0 [0x013AC520+836896]', '\tOrdinal0 [0x013A05AB+787883]', '\tOrdinal0 [0x013CC128+966952]', '\tOrdinal0 [0x013C837A+951162]', '\tOrdinal0 [0x013C5C51+941137]', '\tOrdinal0 [0x013F8C80+1150080]', '\tOrdinal0 [0x013F88DA+1149146]', '\tOrdinal0 [0x013F3F66+1130342]', '\tOrdinal0 [0x013CE546+976198]', '\tOrdinal0 [0x013CF456+980054]', '\tGetHandleVerifier [0x016D9632+1727522]', '\tGetHandleVerifier [0x0178BA4D+2457661]', '\tGetHandleVerifier [0x015BEB81+569713]', '\tGetHandleVerifier [0x015BDD76+566118]', '\tOrdinal0 [0x014C0B2B+1968939]', '\tOrdinal0 [0x014C5988+1989000]', '\tOrdinal0 [0x014C5A75+1989237]', '\tOrdinal0 [0x014CECB1+2026673]', '\tBaseThreadInitThunk [0x76BE6A14+36]', '\tRtlInitializeExceptionChain [0x7785AB4F+143]', '\tRtlInitializeExceptionChain [0x7785AB1A+90]', ''])
    2022-04-29 04:59:04,587 ERROR [Thread-3 (run_job)] infinite.jobs.download_ibovespa_b3->run_job<191>  O job 'CARTEIRA_IBOVESPA' nao pode prosseguir sem o WebDriver do Chrome.

    ---------- INFINITE\LOGS\INFINITE.LOG
    [311]2022-04-29 04:59:04,585 ERROR [Thread-3 (run_job)] infinite.jobs.commons->open_webdriver_chrome<113>  Erro ao tentar inicializar o WebDriver do Chrome:
    [313]2022-04-29 04:59:04,587 ERROR [Thread-3 (run_job)] infinite.jobs.download_ibovespa_b3->run_job<191>  O job 'CARTEIRA_IBOVESPA' nao pode prosseguir sem o WebDriver do Chrome.

Modificar job das loterias para buscar o texto/anchor "Resultados da ..." 
ao inves de localizar pelo XPATH.
    Resultados da Dia de Sorte por ordem crescente.
    Resultados da Lotofácil por ordem crescente.
    Resultados da Super Sete por ordem crescente.
    Resultados da Dupla Sena por ordem crescente.
    Resultados da Quina por ordem crescente.
    Resultados da Mega-Sena por ordem crescente.
    Resultados da Lotomania por ordem crescente.
    Resultados da Timemania por ordem crescente.

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
