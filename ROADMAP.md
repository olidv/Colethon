Criar classe ancestral e aplicar POO nos jobs
    substituir o "duck typing" no scheduler.

Incluir arquivo de controle em todos os jobs
    se já executou no dia, nem arquivo de log copia...

Mover os arquivos de logging, para não deixar acumular na estação Dell.
    Logging do InFiniTe e Digital-Clock.

Apos a aplicação atingir maturidade, desligar o logging dos frameworks.
    loggers:
      schedule:
        level: ERROR
      selenium:
        level: ERROR
      urllib3:
        level: ERROR

Incluir zip do diretorio \dist\*.* no InFiniTe.
    <app>.zip

Criar novo job de manutenção para apagar logs antigos
    apagar arquivos de controle de dias anteriores (\infinite\temp\*), etc...

Criar novo job para download dos arquivos de resultados das loterias da caixa.
    dia de sorte:  //*[@id="resultados"]/div[2]/ul/li/a
    megasena:      //*[@id="resultados"]/div[2]/ul/li/a
    quina:         //*[@id="resultados"]/div[2]/ul/li/a
    timemania:     //*[@id="resultados"]/div[2]/ul/li/a
    lotomania:     //*[@id="resultados"]/div[2]/ul/li/a
    dupla-sena:    //*[@id="resultados"]/div[2]/ul/li/a 
    lotofacil:     //*[@id="resultados"]/div[2]/ul/li/a

Criar novo job para alertar para vencimentos de ativos como mini índices e opções.
    Indicar próximos ativos a serem negociados apos vencimento e dia/data da troca.

Adotar "async def" nos métodos de jobs.

Criar novo job para baixar as cotações de commodities no mundo inteiro.
Criar novo job para download de todas as comodities que afetem a bolsa no brasil.
    Milho, Soja, Café, Boi Gordo, Barril de Petróleo, Minério

Criar novo job para baixar as cotações dos índices das principais bolsas no mundo.

Mudar o codename de cada job para 3 letras ao gerar arquivo de controle (\temp).

Criar tela principal com o Qt Designer, parar de usar DOS shell.

---------------------------------------------------------------------

** Dia 01/Janeiro/2022: revisar feriados B3 no InFiniTe (Python).

Substituir level CRITICAL por FATAL.
