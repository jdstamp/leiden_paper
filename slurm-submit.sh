#!/usr/bin/env bash

#SBATCH -n 1
#SBATCH --mem=50G
#SBATCH -t 8:00:00

module load python/3.9.0 R/4.2.0 plink/1.90 fftw/3.3.8
. /users/jstamp1/.cache/pypoetry/virtualenvs/leiden-paper-DnciuFVg-py3.9/bin/activate

python /users/jstamp1/git/leiden_paper/population_structure_pipeline.py
