#!/bin/bash
#SBATCH --partition=single
#SBATCH --tasks=1
#SBATCH --gres=gpu:A100:2
#SBATCH --time=03:15:00
#SBATCH --mem=237gb
#SBATCH --output=st_t0_sampling_%j

module load devel/miniconda/3
source $MINICONDA_HOME/etc/profile.d/conda.sh
conda deactivate
conda activate llmlink
echo $(which python)
module load devel/cuda/11.6
python QA_models_answer_sampling.py -m="mistralai/Mixtral-8x7B-Instruct-v0.1" \
    -o="../data_paper_neural/results_post_cogsci/trials_LLMs_e1_mixtral-instruct_zero-shot.csv" \
    -p="../experiments/free_production/trials/trials_LLMs_all_options_postprocessed.csv" \
    -topk=5 \
    -tm=1 \
    -pr="zero-shot" \
    -t="lm_sampling"
