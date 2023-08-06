#!/bin/bash
unset LD_LIBRARY_PATH
declare -x PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:"${ASCENDPATH}""
readonly LOG_SIZE_THRESHOLD=$((20 * 1024 * 1024))
readonly LOG_COUNT_THRESHOLD=5
readonly BASE_DIR=$(
    cd "$(dirname $0)" >/dev/null 2>&1
    pwd -P
)

export ANSIBLE_CONFIG=$BASE_DIR/ansible.cfg
export ANSIBLE_LOG_PATH=$BASE_DIR/install.log
export ANSIBLE_CACHE_PLUGIN_CONNECTION=$BASE_DIR/facts_cache

function log_info() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[INFO] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >>${BASE_DIR}/install.log
}

function log_warning() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[WARNING] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [WARNING] $*" >>${BASE_DIR}/install.log
}

function log_error() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[ERROR] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [ERROR] $*" >>${BASE_DIR}/install.log
}

function operation_log_info() {
    local DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N=$(whoami)
    local IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >>${BASE_DIR}/install_operation.log
}

function get_specified_python() {
    if [ ! -z ${ASCEND_PYTHON_VERSION} ]; then
        echo ${ASCEND_PYTHON_VERSION}
    else
        echo $(grep -oP "^ascend_python_version=\K.*" ${BASE_DIR}/downloader/config.ini | sed 's/\r$//')
    fi
}

readonly specified_python=$(get_specified_python)
readonly PYTHON_VERSION=$(echo ${specified_python} | sed 's/P/p/;s/-//')
readonly PYTHON_PREFIX=${HOME}/.local/${PYTHON_VERSION}
export PATH=${PYTHON_PREFIX}/bin:$PATH
export LD_LIBRARY_PATH=${PYTHON_PREFIX}/lib:$LD_LIBRARY_PATH

function rotate_log() {
    local log_list=$(ls $1* | sort -r)
    for item in $log_list; do
        local suffix=${item##*.}
        local prefix=${item%.*}
        if [[ ${suffix} != "log" ]]; then
            if [[ ${suffix} -lt ${LOG_COUNT_THRESHOLD} ]]; then
                suffix=$(($suffix + 1))
                mv -f $item $prefix.$suffix
            fi
        else
            mv -f ${item} ${item}.1
            cat /dev/null >${item}
        fi
    done
}

function check_log() {
    if [[ ! -e $1 ]]; then
        touch $1
    fi
    local log_size=$(ls -l $1 | awk '{ print $5 }')
    if [[ ${log_size} -ge ${LOG_SIZE_THRESHOLD} ]]; then
        rotate_log $1
    fi
}

function set_permission() {
    chmod -R 750 $(find ${BASE_DIR}/ -type d ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*") 2>/dev/null
    chmod -R 640 $(find ${BASE_DIR}/ -type f ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*") 2>/dev/null
    for f in $(find ${BASE_DIR}/ -maxdepth 2 -type f -name "*.sh" -o -name "*.py" ! -path "${BASE_DIR}/.git*" ! -path "${BASE_DIR}/resources/run_from_*_zip/*"); do
        is_exe=$(file ${f} | grep executable | wc -l)
        if [[ ${is_exe} -eq 1 ]]; then
            chmod 550 ${f} 2>/dev/null
        fi
    done
    chmod 750 $BASE_DIR/ $BASE_DIR/playbooks/install
    chmod 600 ${BASE_DIR}/*.log ${BASE_DIR}/tools/*.log ${BASE_DIR}/inventory_file $BASE_DIR/ansible.cfg ${BASE_DIR}/downloader/config.ini 2>/dev/null
    chmod 400 ${BASE_DIR}/*.log.? ${BASE_DIR}/tools/*.log.? 2>/dev/null
}

main() {
    local os_name=$(grep -oP "^ID=\"?\K\w+" /etc/os-release)
    check_log ${BASE_DIR}/install.log
    check_log ${BASE_DIR}/install_operation.log
    set_permission

    python3 -V > /dev/null 2>&1
    if [[ $? != 0 ]]; then
      python ${BASE_DIR}/ascend_deployer.py $*
    else
      python3 ${BASE_DIR}/ascend_deployer.py $*
    fi
}

main $*
main_status=$?
if [[ ${main_status} != 0 ]] && [[ ${main_status} != 6 ]]; then
    operation_log_info "parameter error,run failed"
else
    operation_log_info "$0 $*:Success"
fi
exit ${main_status}
