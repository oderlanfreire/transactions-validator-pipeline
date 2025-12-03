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
        if ls "${FOLDER}/*.csv"
}
#python transactions_pipeline_main.py 