#!/bin/bash

BLUE="\033[34m"
RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0m"
FOLDER="/input"

iniciar_job(){
    echo "${RED}${date '+%Y-%m-%d  %H:%M:%S'}${NC} | ${GREEN}INFO${NC} | Iniciando a pipeline de validação de transações..."

}

verificando_arquivo(){
    echo "${RED}${date '+%Y-%m-%d  %H:%M:%S'}${NC} | ${BLUE}INFO${NC} | Verificando a existência do arquivo de transações..."
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
            echo "${RED}${date '+%Y-%m-%d %H:%M:%S'}${NC} | ${GREEN}INFO${NC} | Arquivo encontrado."
            break
        fi
    done
}
excutar_pipe(){
    echo "${RED}${date '+%Y=%m-%d %H:%M:%S'}${NC} | ${BLUE}INFO${NC} | Iniciando processamento do arquivo."
    python transactions_pipeline_main.py
}
