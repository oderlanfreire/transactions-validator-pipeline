#!/bin/bash

TRACE_ID="$(date +%s)-$RANDOM"
export TRACE_ID

# Carragar as varuaveis de ambiente do arquivo .env
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
  set -o allexport
  . "$SCRIPT_DIR/.env"
  set +o allexport
else
  echo "Aviso: .env não encontrado em $SCRIPT_DIR"
fi

mkdir -p "$LOG_FOLDER_SH"
LOG_TS=$(date '+%Y%m%d_%H%M%S')

LOG_FILE="$LOG_FOLDER_SH/logs/transactions_pipeline_${LOG_TS}.log"
ERR_FILE="$LOG_FOLDER_SH/error/transactions_pipeline_${LOG_TS}.err"

exec > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERR_FILE" >&2)



TOTAL_TIME=$((TIMEOUT * 60))
THRESHOLD=$((TOTAL_TIME - 300))
WARN_PRINTED=false


timestamp(){
    date '+%Y-%m-%d %H:%M:%S'
}

log_info(){
    echo -e "$(timestamp) | $TRACE_ID | INFO | $1"
}

log_warn(){
    echo -e "$(timestamp) | $TRACE_ID | WARN | $1"
}

log_err(){
    echo -e "$(timestamp) | $TRACE_ID | ERROR | $1"
}

log_success(){
    echo -e "$(timestamp) | $TRACE_ID | SUCCESS | $1"
}

verify_input_folder(){
    if [ ! -d "$INPUT_FOLDER" ]; then
        log_err "A pasta de entrada especificada não existe: $INPUT_FOLDER"
        log_info "Encerrando o job."
        exit 1
    fi
}

has_files() {
    shopt -s nullglob
    files=(
        "$INPUT_FOLDER"/*.csv
        "$INPUT_FOLDER"/*.CSV
        "$INPUT_FOLDER"/*.txt
        "$INPUT_FOLDER"/*.TXT
        "$INPUT_FOLDER"/*.csv.gz
        "$INPUT_FOLDER"/*.CSV.gz
        "$INPUT_FOLDER"/*.csv.GZ
        "$INPUT_FOLDER"/*.CSV.GZ
        "$INPUT_FOLDER"/*.txt.gz
        "$INPUT_FOLDER"/*.TXT.gz
        "$INPUT_FOLDER"/*.txt.GZ
        "$INPUT_FOLDER"/*.TXT.GZ
    )
    shopt -u nullglob

    (( ${#files[@]} > 0 ))
}

iniciar_job(){
    log_success "Iniciando pipeline de validação de transações."
    verify_input_folder
}

verificando_arquivo(){
    log_info "Verificando a existência do arquivo de transações..."
    wait_time=0

    while true
    do
        if has_files; then
            log_success "Arquivo encontrado."
            break
        fi

        if [ "$wait_time" -ge "$THRESHOLD" ] && [ "$WARN_PRINTED" = false ]
        then
            log_warn "Faltam 5 minutos para o tempo limite de espera. Continuando a aguardar por arquivos na pasta ${INPUT_FOLDER}."
            WARN_PRINTED=true
        fi


        if [ "$wait_time" -ge "$TOTAL_TIME" ]
        then
            log_err "Tempo de espera esgotado. Nenhum arquivo encontrado na pasta ${INPUT_FOLDER}."
            log_info "Encerrando o job."
            exit 0
        fi

        sleep $INTERVAL
        wait_time=$((wait_time + INTERVAL))
    done
}
executar_processamento(){
    log_info "Iniciando processamento do arquivo."
    python transactions_pipeline_main.py
    if [ $? -ne 0 ]
        then
        log_err "Ocorreu um erro durante a execução do script."
        log_info "Encerrando o job."
        exit 1
    fi
}

encerrar_job(){
    log_success "Pipeline de validação de transações finalizada."
}


iniciar_job
verificando_arquivo
executar_processamento
encerrar_job