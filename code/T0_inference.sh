#!/bin/bash
#SBATCH --partition=single
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:A40:1
#SBATCH --time=00:15:00
#SBATCH --mem=25gb
#SBATCH --output=st_t0_sampling_%j
#SBATCH --verbose
module load devel/miniconda/3
source $MINICONDA_HOME/etc/profile.d/conda.sh
conda deactivate
conda activate qa_models
echo $(which python)
module load devel/cuda/11.6
python QA_models_answer_sampling.py -m="bigscience/T0_3B" -o="results/trials_LLMs_bigscience_T0_3B.csv" -p="trials_LLMs_postprocessed.csv" -t="lm_prob"