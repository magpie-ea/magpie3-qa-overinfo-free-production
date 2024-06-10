#!/bin/bash
#SBATCH --partition=single
#SBATCH --tasks=1
#SBATCH --time=02:00:00
#SBATCH --mem=2gb

module load devel/miniconda/3
source $MINICONDA_HOME/etc/profile.d/conda.sh
conda deactivate
conda activate llmlink
echo $(which python)
module load devel/cuda/11.6

prompts=("zero-shot")
for i in ${!prompts[*]}; do
    echo "Running prompt: ${prompts[$i]}"
    python GPT-overinformative-answers.py \
        -t="samples" \
        -os \
        -n=5 \
        -m=64 \
        -e="e3_highprior" \
        -pr="${prompts[$i]}"
done
