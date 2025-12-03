#!/bin/bash

BLUE="\033[34m"
RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m"
FOLDER="./input"
TIMEOUT=30
INTERVAL=5
TOTAL_TIME=$((TIMEOUT * 60))

iniciar_job(){
    echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${GREEN}INFO${NC} | Iniciando a pipeline de validação de transações..."

}

verificando_arquivo(){
    echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${BLUE}INFO${NC} | Verificando a existência do arquivo de transações..."
    wait_time=0

    while true;
    do
        if ls "${FOLDER}"/*.csv \
        "${FOLDER}"/*.CSV \
        "${FOLDER}"/*.txt \
        "${FOLDER}"/*.TXT \
        "${FOLDER}"/*.txt.gz \
        "${FOLDER}"/*.TXT.gz \
        "${FOLDER}"/*.txt.GZ \
        "${FOLDER}"/*.TXT.GZ \
        "${FOLDER}"/*.csv.gz \
        "${FOLDER}"/*.CSV.gz \
        "${FOLDER}"/*.csv.GZ \
        "${FOLDER}"/*.CSV.GZ 1> /dev/null 2>&1;
        then
            echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${GREEN}INFO${NC} | Arquivo encontrado."
            break
        fi

        if [ "$wait_time" -ge "$TOTAL_TIME" ];
        then
            echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${BLUE}INFO${NC} | Tempo de espera esgotado. Nenhum arquivo encontrado na pasta ${FOLDER}."
            echo "Encerrando o job."
            exit 0
        fi
        sleep $INTERVAL
        wait_time=$((wait_time + INTERVAL))
    done
}
executar_processamento(){
    echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${BLUE}INFO${NC} | Iniciando processamento do arquivo."
    python transactions_pipeline_main.py
    if [ $? -ne 0 ];
        then
        echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${RED}ERRO${NC} | Ocorreu um erro durante a execução do script."
        echo "Encerrando o job."
        exit 1
    fi
}

encerrar_job(){
    echo -e "${RED}$(date '+%Y-%m-%d %H:%M:%S')${NC} | ${GREEN}INFO${NC} | Pipeline de validação de transações finalizada."
}


iniciar_job
verificando_arquivo
executar_processamento
encerrar_job