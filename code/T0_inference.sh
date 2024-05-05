#!/bin/bash
#SBATCH --partition=single
#SBATCH --tasks=1
#SBATCH --gres=gpu:A100:2
#SBATCH --time=08:00:00
#SBATCH --mem=237gb

module load devel/miniconda/3
source $MINICONDA_HOME/etc/profile.d/conda.sh
conda deactivate
conda activate llmlink
echo $(which python)
module load devel/cuda/11.6

prompts=("zero-shot" "explanation" "example" "cot")
prompts_e2=("zero-shot" "explanation" "example" "cot")
expts=("e1" "e2")
for j in ${!expts[*]}; do
    echo "Running prompt: ${expts[$j]}"
    case "${expts[$j]}" in 
        "e2")
        for i in ${!prompts_e2[*]}; do
            echo "Running prompt: ${prompts_e2[$i]}"
            python QA_models_answer_sampling.py -m="mistralai/Mixtral-8x7B-Instruct-v0.1" \
                -o="../data_paper_neural/results_post_cogsci/" \
                -p="../experiments/contextSensitive_free_production/trials/trials_e2_fctPrompt_fixedOrder.csv" \
                -ml=128 \
                -topk=5 \
                -tm=1 \
                -pr="${prompts_e2[$i]}" \
                -t="lm_sampling" \
                -fs \
                -ex="${expts[$j]}"
        done
    ;;
        "e1")
        for i in ${!prompts[*]}; do
            echo "Running prompt: ${prompts[$i]}"
            python QA_models_answer_sampling.py -m="mistralai/Mixtral-8x7B-Instruct-v0.1" \
                -o="../data_paper_neural/results_post_cogsci/" \
                -p="../experiments/free_production/trials/trials_LLMs_all_options_postprocessed.csv" \
                -ml=128 \
                -topk=5 \
                -tm=1 \
                -pr="${prompts[$i]}" \
                -t="lm_sampling" \
                -fs \
                -ex="${expts[$j]}"
        done
    esac
done
