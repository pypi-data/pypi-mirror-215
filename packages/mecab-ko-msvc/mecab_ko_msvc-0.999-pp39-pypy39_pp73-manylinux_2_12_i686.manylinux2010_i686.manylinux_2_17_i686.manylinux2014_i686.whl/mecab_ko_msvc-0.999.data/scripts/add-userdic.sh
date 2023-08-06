#!/bin/bash

readonly DIC_PATH="/usr/local/share/mecab-ko-dic"
readonly USERDIC_PATH="/usr/local/share/mecab-ko-dic/user-dic"
readonly MECAB_EXEC_PATH="/usr/local/bin/mecab"
readonly DICT_INDEX="/usr/local/bin/mecab-dict-index"

get_userdics() {
    pushd $USERDIC_PATH &> /dev/null
    echo $(ls *.csv)
    popd &> /dev/null
}

gen_cost() {
    local input_dic=$1
    echo $input_dic

    $DICT_INDEX \
        -m ${DIC_PATH}/model.def \
        -d ${DIC_PATH} \
        -u ${DIC_PATH}/user-${input_dic} \
        -f utf-8 \
        -t utf-8 \
        -a ${USERDIC_PATH}/$input_dic
}

compile() {
    rm -r ${DIC_PATH}/*.bin
    rm -r ${DIC_PATH}/*.txt
    $DICT_INDEX -d "${DIC_PATH}" -o "${DIC_PATH}" -f UTF-8 -t UTF-8
}

main() {
    echo "generating userdic..."

    for dic in $(get_userdics); do
        gen_cost $dic
    done

    compile
}

main
