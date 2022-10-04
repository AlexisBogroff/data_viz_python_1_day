#!/bin/bash

# Delete previous export
rm -rf ../build/export

# Re-create folders
mkdir ../build/export
mkdir ../build/export/exercises
mkdir ../build/export/correction
mkdir ../build/export/exercises/examples
mkdir ../build/export/correction/examples
mkdir ../build/export/project

# Exercises
# ---------

# Statement
cp intro_python_exercise_statement.ipynb ../build/export/exercises/intro_python_exercise_statement.ipynb
# Correction
cp intro_python_exercise_correction.ipynb ../build/export/correction/intro_python_exercise_correction.ipynb

# Module used in exo
cp truc.py ../build/export/exercises/truc.py
cp truc.py ../build/export/correction/truc.py
# Data
cp examples/TD6_Exam_MCQ.csv ../build/export/exercises/examples/TD6_Exam_MCQ.csv
cp examples/TD6_Exam_MCQ.csv ../build/export/correction/examples/TD6_Exam_MCQ.csv

# Project
# -------

# Statement
cp ../build/Project.pdf ../build/export/project/Project.pdf
# Data
cp masse-salariale-et-assiette-chomage-partiel-mensuelles-du-secteur-prive_modif.csv ../build/export/project/masse-salariale-et-assiette-chomage-partiel-mensuelles-du-secteur-prive_modif.csv
# Correction
cp Project_correction.ipynb ../build/export/project/Project_correction.ipynb
