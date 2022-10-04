#!/bin/bash

tex_file=$1
filename="${tex_file%.*}"

# build CM or TD a first time
pdflatex -shell-escape $1

if [[ $1 == "CM"* ]]
then
    # build CM a second time for table of content
    pdflatex -shell-escape $1
fi

# TD3 has no answer for the moment as it is only manipulation on git branches.
# TD5 has no answer as it is the exam.
if [[ $1 == "TD"* && $1 != "TD3"* && $1 != "TD5"* ]] 
then
    # build TD a second time with answers displayed
    pdflatex -shell-escape -jobname=${filename}_answers "\gdef\answer{} \input $1"
fi

mkdir -p ../build
mv *.pdf ../build

mkdir -p ../logs
mv *.aux ../logs
mv *.log ../logs
mv *.nav ../logs
mv *.out ../logs
mv *.snm ../logs
mv *.toc ../logs
mv *.vrb ../logs
mv *.pyg ../logs
mv _minted-*/ ../logs
