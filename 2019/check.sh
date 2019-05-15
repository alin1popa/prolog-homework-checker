#!/bin/bash

let score=0

function run_simple
{
    echo -e "\e[95m\n~~~ Running simple tests ~~~\n\e[39m"

    for i in `seq 1 10`; do
        echo -n "Running test $i.........."
        rm -f output.txt &> /dev/null
        python2 checker.py main.pl teste/simple/in_simple_t"$i".txt &> /dev/null
        
        diff teste/simple/out_simple_t"$i".txt output.txt &> /dev/null
        
        if [ $? -le 0 ]; then
            echo -e "\e[92mOK\e[39m"
			score=$((score+1))
        else
            echo -e "\e[91mWRONG\e[39m"
        fi
    done
}

function run_easy
{
    echo -e "\e[95m\n~~~ Running easy tests ~~~\n\e[39m"

    for i in `seq 1 25`; do
        echo -n "Running test $i.........."
        rm -f output.txt &> /dev/null
        python2 checker.py main.pl teste/easy/in_easy_t"$i".txt &> /dev/null
        
        diff teste/easy/out_easy_t"$i".txt output.txt &> /dev/null
        
        if [ $? -le 0 ]; then
            echo -e "\e[92mOK\e[39m"
			score=$((score+1))
        else
            echo -e "\e[91mWRONG\e[39m"
        fi
    done
}

if [ "$#" -eq 0 ]; then
    run_simple
	run_easy
	echo -e "\e[95m\n~~~ Total: "$(($score * 2))"/120 ~~~\n\e[39m"
elif [ "$#" -eq 1 ]; then
    if [ "$1" = "s" ]; then
        run_simple
	elif [ "$1" = "e" ]; then
        run_easy
    fi
else
    if [ "$1" = "s" ]; then
        rm -f output.txt &> /dev/null
        python2 checker.py main.pl teste/simple/in_simple_t"$2".txt
        
        printf "\e[93m\nYour output:\n\n"
        cat output.txt
        
        printf "\e[92m\n\nCorrect:\n\n"
        cat teste/simple/out_simple_t"$2".txt
        echo
	elif [ "$1" = "e" ]; then
        rm -f output.txt &> /dev/null
        python2 checker.py main.pl teste/easy/in_easy_t"$2".txt
        
        printf "\e[93m\nYour output:\n\n"
        cat output.txt
        
        printf "\e[92m\n\nCorrect:\n\n"
        cat teste/easy/out_easy_t"$2".txt
        echo
    fi
fi
