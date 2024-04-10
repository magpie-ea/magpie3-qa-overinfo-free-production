import random
import os
import tqdm
import pandas as pd
from dotenv import load_dotenv

import numpy as np
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector.base import BaseExampleSelector
from langchain.example_generator import generate_example
# from langchain_community.llms import OpenAI
# from langchain.chains.llm import LLMChain
from langchain.chains import SequentialChain, TransformChain
# import openai
from datetime import datetime
import argparse

############ updated API ########
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
llm.invoke("how can langsmith help with testing?")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
chain.invoke({"input": "how can langsmith help with testing?"})

####################
# openai.api_key = os.getenv("OPENAI_API_KEY")

INSTRUCTIONS_DIR = 'instructions'

def transform_fct(inputs: dict) -> dict:
    print("Inputs received by transform fct ", inputs)
    inputs = inputs["sampled_objects"]
    print("executing transform fct")
    transformed_dict = {
        "basic_category": inputs.split('Object category: ')[-1].split('\n')[0],
        "typical": inputs.split('Common kind: ')[-1].split('\n')[0],
        "atypical": inputs.split('Uncommon kind: ')[-1].split('\n')[0],
    }
    return transformed_dict

# TODO generalize fct above to take I/O var names as params and be adaptive to both vignettes
def transform_goals(inputs: dict) -> dict:
    inputs = inputs["sampled_goals"]
    print("executing transform goals function")
    print("Input to transform goals ", inputs)
    # transformed_dict = {
    #     "goal": inputs.split('Goal: ')[-1].split('\n')[0],
    #     "method_1": inputs.split('Method 1: ')[-1].split('\n')[0],
    #     "method_2": inputs.split('Method 2: ')[-1].split('\n')[0],
    # }
    transformed_dict = {
        "goal": inputs.split('Goal: ')[-1].split('\n')[0],
        "step": inputs.split('Step: ')[-1].split('\n')[0],
        "scale": inputs.split('Scale: ')[-1].split('\n')[0],
        "value_1": inputs.split('Value 1: ')[-1].split('\n')[0],
        "value_2": inputs.split('Value 2: ')[-1].split('\n')[0],
    }
    print("Transformed dict out ", transformed_dict)
    
    return transformed_dict

def transform_fct_context(inputs: dict) -> dict:
    story = inputs["sampled_context"]
    print("executing transform fct context")

    transformed_dict = {
        "basic_category_c": inputs["basic_category"],
        "typical_c": inputs["typical"],
        "atypical_c": inputs["atypical"],
        "context_common": story.split('Context_common: ')[-1].split('\n')[0],
        "context_uncommon": story.split('Context_uncommon: ')[-1].split('\n')[0],
    }
    return transformed_dict 

def transform_fct_edit(inputs: dict) -> dict:
    revision = inputs["sampled_revision"]
    print("input s", inputs)
    transformed_dict = {
        "revision": revision.split('Revision: ')[-1].split('\n')[0],
        "context_e": inputs["context_common"],
        "question_e": inputs["question"],
    }
    return transformed_dict 


def transform_fct_preference(inputs: dict) -> dict:
    question = inputs["sampled_preference"]
    print("executing transform preference context")

    transformed_dict = {
        "basic_category_p": inputs["basic_category"],
        "typical_p": inputs["typical"],
        "atypical_p": inputs["atypical"],
        "context_common_p": inputs["context_common"],
        "question": question.split('Question: ')[-1].split('\n')[0],
    }
    return transformed_dict 

# TODO possibly adjust for passing through goal and methods
def transform_options(inputs: dict) -> dict:
    options = inputs["sampled_options"]
    print("executing transform options function")
    print("Input to transform options ", inputs)
    transformed_dict = {
        "option_1": options.split('Option 1: ')[-1].split('\n')[0],
        "option_2": options.split('Option 2: ')[-1].split('\n')[0],
        "value_1_o": inputs["value_1"],
        "value_2_o": inputs["value_2"],
        "goal_o": inputs["goal"],
        "scale_o": inputs["scale"],
        "step_o": inputs["step"],
    }
    print("Transformed dict out ", transformed_dict)
    return transformed_dict


def transform_context(inputs: dict) -> dict:
    context = inputs["context"]
    print("executing transform context function")
    print("Input to transform context ", inputs)
    # transformed_dict = {
    #     "context_c": context.split('Context: ')[-1].split('\n')[0],
    #     "question": context.split('Question: ')[-1].split('\n')[0],
    #     "option_1_c": inputs["option_1"],
    #     "option_2_c": inputs["option_2"],
    #     "method_1_c": inputs["method_1"],
    #     "method_2_c": inputs["method_2"],
    #     "goal_c": inputs["goal"],
    # }
    transformed_dict = {
        "context_c": context.split('Context: ')[-1].split('\n')[0],
        "question": context.split('Question: ')[-1].split('\n')[0],
        "option_1_c": inputs["option_1"],
        "option_2_c": inputs["option_2"],
        "value_1_c": inputs["value_1"],
        "value_2_c": inputs["value_2"],
        "goal_c": inputs["goal"],
        "scale_c": inputs["scale"],
        "step_c": inputs["step"],
    }
    print("Transformed dict out ", transformed_dict)
    return transformed_dict        

def transform_secondary_goal(inputs: dict) -> dict:
    secondary_goal = inputs["secondary_goal"]
    print("executing transform secondary goal function")
    print("Input to transform context ", inputs)
    # transformed_dict = {
    #     "version_1": secondary_goal.split('Version 1: ')[-1].split('\n')[0],
    #     "version_2": secondary_goal.split('Version 2: ')[-1].split('\n')[0],
    #     "context_g": inputs["context"],
    #     "question_g": inputs["question"],
    #     "option_1_g": inputs["option_1"],
    #     "option_2_g": inputs["option_2"],
    #     "method_1_g": inputs["method_1"],
    #     "method_2_g": inputs["method_2"],
    #     "goal_g": inputs["goal"],
    # }
    transformed_dict = {
        "version_1": secondary_goal.split('Version 1: ')[-1].split('\n')[0],
        "version_2": secondary_goal.split('Version 2: ')[-1].split('\n')[0],
        "question_g": inputs["question"],
        "context_g": inputs["context_c"],
        "option_1_g": inputs["option_1"],
        "option_2_g": inputs["option_2"],
        "value_1_g": inputs["value_1"],
        "value_2_g": inputs["value_2"],
        "step_g": inputs["step"],
        "scale_g": inputs["scale"],
        "goal_g": inputs["goal"],
    }
    print("Transformed dict out ", transformed_dict)
    return transformed_dict

def transform_edits(inputs: dict) -> dict:
    edits = inputs["edited_questions"]
    print("executing transform edits function")
    print("Input to transform context ", inputs)
    transformed_dict = {
        "edit_1": edits.split('Edit 1: ')[-1].split('\n')[0],
        "edit_2": edits.split('Edit 2: ')[-1].split('\n')[0],
        "value_1_e": inputs["value_1"],
        "value_2_e": inputs["value_2"],
        "version_1_e": inputs["version_1"],
        "version_2_e": inputs["version_2"],
        "goal_e": inputs["goal"],
    }
    print("Transformed dict out ", transformed_dict)
    return transformed_dict

class RandomExampleSelector(BaseExampleSelector):
    
    def __init__(self, examples: pd.DataFrame, stage: str, expt: str = "prior"):
        self.examples = examples
        self.stage = stage
        if expt == "prior":
            if self.stage == "stage1":
                self.keys = ["basic_category", "typical", "atypical"]
            elif self.stage == "stage2":
                self.keys = ["basic_category", "typical", "atypical", "context_common", "context_uncommon"]
            elif self.stage == "stage3":
                self.keys = ["basic_category", "typical", "atypical", "context_common", "question"]
            elif self.stage == "stage4":
                self.keys = ["context", "question", "revision" ]
            else:
                raise ValueError("Stage must be one of stage1, stage2, stage3")
        else:
            if self.stage == "stage1":
                self.keys = ["goal", "step", "scale", "value_1", "value_2"]#["goal", "method_1", "method_2"]
            elif self.stage == "stage2":
                self.keys = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2"] #["goal", "method_1", "method_2", "option_1", "option_2"]
            elif self.stage == "stage3":
                self.keys = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context", "question"] #["goal", "method_1", "method_2", "option_1", "option_2", "context", "question"]
            elif self.stage == "stage4":
                self.keys = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context", "question", "version_1", "version_2"] #["goal", "method_1", "method_2", "option_1", "option_2", "context", "question", "version_1", "version_2"]
            elif self.stage == "stage5":
                self.keys = ["goal", "aspect_1", "aspect_2", "question_1", "question_2", "edit_1", "edit_2"]
            else:
                raise ValueError("Stage must be one of stage1, stage2, stage3, stage4, stage5")
    
    def add_example(self, example: pd.DataFrame) -> None:
        """Add new example to store for a key."""
        self.examples.append(example)

    def select_examples(self, num_examples: int = 5) -> list[dict]:
        """Select which examples to use based on the inputs."""
        num_examples = min(num_examples, len(self.examples))
        selected_rows = self.examples.sample(n=num_examples, replace=False, random_state=42)
        print("selected rows ", selected_rows)
        print("columns ", selected_rows.columns)
        selected_examples = []
        for _, row in selected_rows.iterrows():
            example = {}
            for key in self.keys:
                example[key] = row[key]
            selected_examples.append(example)

        return selected_examples
    
def sample_prior_vignettes(model, temperature, **kwargs):

    # instantiate model
    model = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        **kwargs   
    ) 
    examples = pd.read_csv("../data+analysis/vignette_examples/prior_examples.csv")

    # read in instructions
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage1_sample_objects.txt'), 'r') as f:
        instructions_text = f.read()

    objects_template = """
    Object category: {basic_category}
    Common kind: {typical}
    Uncommon kind: {atypical}
    """
    # read in examples    
    example_selector_s1 = RandomExampleSelector(examples, "stage1")
    selected_examples = example_selector_s1.select_examples(num_examples=3)
    print("selected examples stage 1 ", selected_examples)

    prompt_template = PromptTemplate(
        template = objects_template,
        input_variables = ['basic_category', 'typical', 'atypical'],
    )
    # format the few_shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        prefix=instructions_text, 
        examples=selected_examples,
        example_prompt=prompt_template, 
        input_variables=[], 
        suffix="Object category:",
        example_separator="\n\n",
    )    
    print("Predicting objects")
    
    # objects_chain = LLMChain(
    #     llm=model, 
    #     prompt=few_shot_prompt, 
    #     verbose=True, 
    #     output_key="sampled_objects"
    # ) 
    object_transformation_chain = TransformChain(
        input_variables=["sampled_objects"], 
        output_variables=["basic_category", "typical", "atypical"], 
        transform=transform_fct, 
        verbose=True
    )
    chain = few_shot_prompt | model | output_parser | object_transformation_chain
    r = chain.invoke({"input": ""})

    # TODO add a an agent based check / LMQL or so to check whether the proposals match the criteria

   #######################################################################################
    # read in instructions
#     with open(os.path.join(INSTRUCTIONS_DIR, 'stage2_sample_context.txt'), 'r') as f:
#         instructions_text_context = f.read()

#     context_template = """
#     Object category: {basic_category}
#     Common kind: {typical}
#     Uncommon kind: {atypical}
#     Context_common: {context_common}
#     Context_uncommon: {context_uncommon}    
#     """

#     # read in examples
#     example_selector_s2 = RandomExampleSelector(examples, "stage2")
#     selected_examples_context = example_selector_s2.select_examples(num_examples=3)
#     print("selected examples stage 2 ", selected_examples_context)
#     # model = OpenAI(model_name=model, temperature=temperature, **kwargs)
#     # out_parser_list = CommaSeparatedListOutputParser()
#     prompt_template_context = PromptTemplate(
#         template = context_template,
#         input_variables = ['basic_category', 'context_common', 'context_uncommon', 'typical', 'atypical'],
#     )
#     suffix_template_context = """
#     Object category: {basic_category}
#     Common kind: {typical}
#     Uncommon kind: {atypical}
#     """
#     # format the few_shot prompt
#     few_shot_prompt_context = FewShotPromptTemplate(
#         prefix=instructions_text_context, 
#         examples=selected_examples_context,
#         example_prompt=prompt_template_context, 
#         input_variables=["basic_category", "typical", "atypical"], 
#         suffix=suffix_template_context,
#         example_separator="\n\n",
#     )    

#     print("Predicting context")

#     context_chain = LLMChain(llm=model, prompt=few_shot_prompt_context, verbose=True, output_key="sampled_context") 
#     print("transformation of context")
#     context_transformation_chain = TransformChain(
#         input_variables=["sampled_context", "basic_category", "typical", "atypical"], 
#         output_variables=["basic_category_c", "typical_c", "atypical_c", "context_common", "context_uncommon"], 
#         transform=transform_fct_context
#     )
    
#   ############################################################################################
#     # read in instructions
#     with open(os.path.join(INSTRUCTIONS_DIR, 'stage3_sample_preference.txt'), 'r') as f:
#         instructions_text_pref = f.read()
#     preference_template ="""
#     Object category: {basic_category}
#     Common kind: {typical}
#     Uncommon kind: {atypical}
#     Context: {context_common}
#     Question: {question}
#     """
#     suffix_template_pref = """
#     Object category: {basic_category_c}
#     Common kind: {typical_c}
#     Uncommon kind: {atypical_c}
#     Context: {context_common}
#     """

#     example_selector_s3 = RandomExampleSelector(examples, "stage3")
#     selected_examples_preference = example_selector_s3.select_examples(num_examples=3)
#     print("selected examples stage 3 ", selected_examples_preference)

#     prompt_template_pref = PromptTemplate(
#         template = preference_template,
#         input_variables = ['question', 'typical', 'atypical', 'basic_category', 'context_common'],
#     )

#     few_shot_prompt_pref = FewShotPromptTemplate(
#         prefix=instructions_text_pref, 
#         examples=selected_examples_preference,
#         example_prompt=prompt_template_pref, 
#         input_variables=['basic_category_c', 'typical_c', 'atypical_c', 'context_common'], 
#         suffix=suffix_template_pref,
#         example_separator="\n\n",
#     )    

#     print("Predicting preference")
#     preferences_chain = LLMChain(llm=model, prompt=few_shot_prompt_pref, output_key="sampled_preference") 

#     print("trasnformation of preference")
#     preference_transformation_chain = TransformChain(
#         input_variables=["context_common", "basic_category", "typical", "atypical", "sampled_preference"], 
#         output_variables=["basic_category_p", "typical_p", "atypical_p", "context_common_p", "question"], 
#         transform=transform_fct_preference
#     )
#     #######################################
#     # sanity check of the resulting story
#     # TODO this can be extended as an agent with different tools 
#     # including editing the stories to be more natural
#     with open(os.path.join(INSTRUCTIONS_DIR, 'stage4_edit_priors.txt'), 'r') as f:
#         instructions_text_edit = f.read()
#     edit_template ="""
#     Context: {context}
#     Question: {question}
#     Revision: {revision}
#     """
#     suffix_template_edit = """
#     Context: {context_common}
#     Question: {question}
#     """

#     example_selector_s4 = RandomExampleSelector(
#         pd.read_csv("../data+analysis/vignette_examples/prior_edits.csv"), 
#         "stage4"
#     )
#     selected_examples_edit = example_selector_s4.select_examples(num_examples=3)
#     print("selected examples stage 4 ", selected_examples_edit)

#     prompt_template_edit = PromptTemplate(
#         template = edit_template,
#         input_variables = ['question','revision', 'context'],
#     )

#     few_shot_prompt_edit = FewShotPromptTemplate(
#         prefix=instructions_text_edit, 
#         examples=selected_examples_preference,
#         example_prompt=prompt_template_pref, 
#         input_variables=['context_common', 'question'], 
#         suffix=suffix_template_edit,
#         example_separator="\n\n",
#     )    

#     print("Predicting preference")
#     edit_chain = LLMChain(llm=model, prompt=few_shot_prompt_edit, output_key="sampled_revision") 

#     print("trasnformation of preference")
#     edit_transformation_chain = TransformChain(
#         input_variables=["context_common", "question", "sampled_revision"], 
#         output_variables=["context_e", "question_e", "revision"], 
#         transform=transform_fct_edit
#     )
#     #######################################
#     # define chain end to end
#     overall_chain = SequentialChain(
#         chains=[objects_chain,
#                 object_transformation_chain, 
#                 context_chain,
#                 context_transformation_chain,
#                 preferences_chain,
#                 preference_transformation_chain,
#                 edit_chain,
#                 edit_transformation_chain,
#                 ],
#         input_variables=[""], ############# THIS IS THE BIT THAT CAUSED THE STR VS DICT INPUT ISSUES #########
#         # Here we return multiple variables
#         output_variables=["basic_category", "typical", "atypical", "context_common", "context_uncommon", "question", "revision"], # this is the bit defining how outputs are called at each step and what is returned from the entire chain (otherwise default key of generation is 'text')
#         verbose=True
#     )
#     r = overall_chain(inputs=[])
    print("------ FINAL OUTPUTS ------ ", r)
    # df = pd.DataFrame({
    #     "basic_category": r["basic_category"],
    #     "typical": r["typical"],
    #     "atypical": r["atypical"],
    #     "sampled_context_common": r["context_common"],
    #     "sampled_context_uncommon": r["context_uncommon"],
    #     "question": r["question"],
    #     "revision": r["revision"],
    # }, index=[0])
    # print("DF ", df)
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # # df.to_csv(f"vignettes_LLM/output_{timestamp}.csv", index=False)
    # return df

def sample_secondary_goals_vignettes(
        model: str = 'text-davinci-003',
        temperature: float = 0.7,
        **kwargs,
):    
     # instantiate model
    model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    examples = pd.read_csv("../data+analysis/vignette_examples/secondary_goals_subgoals_examples.csv")

    # read in instructions
    # with open(os.path.join(INSTRUCTIONS_DIR, 'stage1_sample_goals.txt'), 'r') as f:
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage1_sample_goals_subgoals.txt'), 'r') as f:
        instructions_text = f.read()

    # goals_template = """
    # Goal: {goal}
    # Method 1: {method_1}
    # Method 2: {method_2}
    # """
    goals_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    """
    # read in examples
    example_selector_s1 = RandomExampleSelector(examples, "stage1", "secondary_goals")
    selected_examples = example_selector_s1.select_examples(num_examples=3)
    print("selected examples stage 1 ", selected_examples)

    prompt_template = PromptTemplate(
        template = goals_template,
        input_variables = ["goal", "step", "scale", "value_1", "value_2"]#['goal', 'method_1', 'method_2'],
    )
    # format the few_shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        prefix=instructions_text, 
        examples=selected_examples,
        example_prompt=prompt_template, 
        input_variables=[], 
        suffix="Goal:",
        example_separator="\n\n",
    )    
    print("Predicting goals")
    goals_chain = LLMChain(
        llm=model, 
        prompt=few_shot_prompt, 
        verbose=True, 
        output_key="sampled_goals"
    ) 
    goals_transformation_chain = TransformChain(
        input_variables=["sampled_goals"], 
        output_variables=["goal", "step", "scale", "value_1", "value_2"], #["goal", "method_1", "method_2"], 
        transform=transform_goals, 
        verbose=True
    )
    #####################################################
    # sample options suiting each of the methods of achieving the goal
    # read in instructions
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage2_sample_options_subgoals.txt'), 'r') as f:
        instructions_options_text = f.read()

    # options_template = """
    # Goal: {goal}
    # Method 1: {method_1}
    # Method 2: {method_2}
    # Option 1: {option_1}
    # Option 2: {option_2}
    # """
    options_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    Option 1: {option_1}
    Option 2: {option_2}
    """
    
    # read in examples    
    example_selector_s2 = RandomExampleSelector(examples, "stage2", "secondary_goals")
    selected_examples_options = example_selector_s2.select_examples(num_examples=3)
    print("selected examples stage 2 ", selected_examples_options)

    # define the templates and the chain
    options_infer_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    """
    options_ex_template = PromptTemplate(
        template = options_template,
        input_variables = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2"] #['goal', 'method_1', 'method_2', 'option_1', 'option_2'],
    )
    # format the few_shot prompt
    few_shot_prompt_options = FewShotPromptTemplate(
        prefix=instructions_options_text, 
        examples=selected_examples_options,
        example_prompt=options_ex_template, 
        input_variables=["goal", "step", "scale", "value_1", "value_2"],#['goal', 'method_1', 'method_2'], 
        suffix=options_infer_template,
        example_separator="\n\n",
    )  
    print("Predicting options for goals")
    options_chain = LLMChain(
        llm=model, 
        prompt=few_shot_prompt_options, 
        verbose=True, 
        output_key="sampled_options"
    ) 
    options_transformation_chain = TransformChain(
        input_variables=["sampled_options", "goal", "step", "scale", "value_1", "value_2"], # TODO check if goal and methods will be passed differently
        output_variables=["goal_o", "step_o", "scale_o", "value_1_o", "value_2_o", "option_1", "option_2"],#["goal_o", "method_1_o", "method_2_o", "option_1", "option_2"], 
        transform=transform_options, 
        verbose=True
    )
    #####################################
    # generate the question and possibly the context in one step
    ####################################
    # possibly put together the whole story

    # read in instructions
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage3_sample_context_question_subgoals.txt'), 'r') as f:
        instructions_context_text = f.read()

    context_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    Option 1: {option_1}
    Option 2: {option_2}
    Context: {context}
    Question: {question}
    """
    
    example_selector_s3 = RandomExampleSelector(examples, "stage3", "secondary_goals")
    selected_examples_context = example_selector_s3.select_examples(num_examples=3)
    print("selected examples stage 2 ", selected_examples_context)

    # define the templates and the chain
    # context_infer_template = """
    # Goal: {goal}
    # Method 1: {method_1}
    # Method 2: {method_2}
    # Option 1: {option_1}
    # Option 2: {option_2}
    # """
    context_infer_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    Option 1: {option_1}
    Option 2: {option_2}
    """
    context_ex_template = PromptTemplate(
        template = context_template,
        input_variables = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context", "question"] #['goal', 'method_1', 'method_2', 'option_1', 'option_2', 'context', 'question'],
    )
    # format the few_shot prompt
    few_shot_prompt_context = FewShotPromptTemplate(
        prefix=instructions_context_text, 
        examples=selected_examples_context,
        example_prompt=context_ex_template, 
        input_variables=["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2"],#['goal', 'method_1', 'method_2', 'option_1', 'option_2'], 
        suffix=context_infer_template,
        example_separator="\n\n",
    )  
    print("Predicting context and questions")
    context_chain = LLMChain(
        llm=model, 
        prompt=few_shot_prompt_context, 
        verbose=True, 
        output_key="context"
    ) 
    # transform
    context_transformation_chain = TransformChain(
        input_variables=["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context"], #["context", "goal", "method_1", "method_2", "option_1", "option_2"], 
        output_variables=["goal_c", "step_c", "scale_c", "value_1_c", "value_2_c", "option_1_c", "option_2_c", "context_c", "question"],#["goal_c", "method_1_c", "method_2_c", "option_1_c", "option_2_c", "context_c", "question"],
        transform=transform_context,
        verbose=True,
    )
    #######################
    # read in instructions
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage4_sample_secondary_goal.txt'), 'r') as f:
        instructions_secondary_goal_text = f.read()

    # secondary_goal_template = """
    # Goal: {goal}
    # Method 1: {method_1}
    # Method 2: {method_2}
    # Option 1: {option_1}
    # Option 2: {option_2}
    # Context: {context}
    # Question: {question}
    # Version 1: {version_1}
    # Version 2: {version_2}
    # """
    secondary_goal_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    Option 1: {option_1}
    Option 2: {option_2}
    Context: {context}
    Question: {question}
    Version 1: {version_1}
    Version 2: {version_2}
    """

    # ] # potentially reason step by step
    example_selector_s4 = RandomExampleSelector(examples, "stage4", "secondary_goals")
    selected_examples_sg = example_selector_s4.select_examples(num_examples=3)
    print("selected examples stage 2 ", selected_examples_sg)


    # define the templates and the chain
    # secondary_goal_infer_template = """
    # Goal: {goal}
    # Method 1: {method_1}
    # Method 2: {method_2}
    # Option 1: {option_1}
    # Option 2: {option_2}
    # Context: {context}
    # Question: {question}
    # """
    secondary_goal_infer_template = """
    Goal: {goal}
    Step: {step}
    Scale: {scale}
    Value 1: {value_1}
    Value 2: {value_2}
    Option 1: {option_1}
    Option 2: {option_2}
    Context: {context_c}
    Question: {question}
    """
    secondary_goal_ex_template = PromptTemplate(
        template = secondary_goal_template,
        input_variables = ["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context", "question", "version_1", "version_2"] #['goal', 'method_1', 'method_2', 'option_1', 'option_2', 'context', 'question', 'version_1', 'version_2'],
    )
    # format the few_shot prompt
    few_shot_prompt_secondary_goal = FewShotPromptTemplate(
        prefix=instructions_secondary_goal_text, 
        examples=selected_examples_sg,
        example_prompt=secondary_goal_ex_template, 
        input_variables=["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context_c", "question"],#['goal', 'method_1', 'method_2', 'option_1', 'option_2', 'context', 'question'], 
        suffix=secondary_goal_infer_template,
        example_separator="\n\n",
    )  
    print("Predicting secondary goal")
    secondary_goal_chain = LLMChain(
        llm=model, 
        prompt=few_shot_prompt_secondary_goal, 
        verbose=True, 
        output_key="secondary_goal"
    ) 

    secondary_goal_transformation_chain = TransformChain(
        input_variables=["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context_c", "question", "secondary_goal"], #["context", "question", "goal", "method_1", "method_2", "option_1", "option_2", "secondary_goal"], 
        output_variables=["goal_g","step_g", "scale_g", "value_1_g", "value_2_g", "option_1_g", "option_2_g", "context_g", "question_g", "version_1", "version_2"],#["goal_g", "method_1_g", "method_2_g", "option_1_g", "option_2_g", "context_g", "question_g", "version_1", "version_2"],
        transform=transform_secondary_goal,
        verbose=True,
    )
    ###############
    # edit the final question to remove explicit secondary goal mentions
    with open(os.path.join(INSTRUCTIONS_DIR, 'stage5_correct_preferences.txt'), 'r') as f:
        instructions_edit_text = f.read()

    editing_template = """
    Goal: {goal}
    Aspect 1: {aspect_1}
    Aspect 2: {aspect_2}
    Question 1: {question_1}
    Question 2: {question_2}
    Edit 1: {edit_1}
    Edit 2: {edit_2}
    """

    # ] # potentially reason step by step
    example_selector_s5 = RandomExampleSelector(
        pd.read_csv("../data+analysis/vignette_examples/secondary_goals_editing.csv"), 
        "stage5", 
        "secondary_goals",
    )
    selected_examples_edit = example_selector_s5.select_examples(num_examples=3)
    print("selected examples stage 5 ", selected_examples_edit)
    editing_infer_template = """
        Goal: {goal}
        Aspect 1: {value_1}
        Aspect 2: {value_2}
        Question 1: {version_1}
        Question 2: {version_2}
    """
    editing_ex_template = PromptTemplate(
        template = editing_template,
        input_variables = ["goal", "aspect_1", "aspect_2", "question_1", "question_2", "edit_1", "edit_2"], 
    )
    # format the few_shot prompt
    few_shot_prompt_editing = FewShotPromptTemplate(
        prefix=instructions_edit_text, 
        examples=selected_examples_edit,
        example_prompt=editing_ex_template, 
        input_variables=["goal", "value_1", "value_2", "version_1", "version_2"],
        suffix=editing_infer_template,
        example_separator="\n\n",
    )  
    print("Predicting secondary goal")
    editing_chain = LLMChain(
        llm=model, 
        prompt=few_shot_prompt_editing, 
        verbose=True, 
        output_key="edited_questions"
    ) 
    editing_transformation_chain = TransformChain(
        input_variables=["goal", "value_1", "value_2", "version_1", "version_2"], 
        output_variables=["goal_e", "value_1_e", "value_2_e", "version_1_e", "version_2_e", "edit_1", "edit_2"],#["goal_g", "method_1_g", "method_2_g", "option_1_g", "option_2_g", "context_g", "question_g", "version_1", "version_2"],
        transform=transform_edits,
        verbose=True,
    )
    ###############################
    # define chain end to end
    overall_chain = SequentialChain(
        chains=[goals_chain,
                goals_transformation_chain, 
                options_chain,
                options_transformation_chain,
                context_chain,
                context_transformation_chain,
                secondary_goal_chain,
                secondary_goal_transformation_chain,
                editing_chain,
                editing_transformation_chain,
                ],
        input_variables=[""], ############# THIS IS THE BIT THAT CAUSED THE STR VS DICT INPUT ISSUES #########
        # Here we return multiple variables
        output_variables=["goal", "step", "scale", "value_1", "value_2", "option_1", "option_2", "context_c", "question", "version_1", "version_2", "edit_1", "edit_2"],#["goal", "method_1", "method_2", "option_1", "option_2", "context_c", "question_g", "version_1", "version_2"], # "sampled_goals", "sampled_options", "sampled_context" this is the bit defining how outputs are called at each step and what is returned from the entire chain (otherwise default key of generation is 'text')
        verbose=True
    )
    r = overall_chain(inputs=[])
    print("------ FINAL OUTPUTS ------ ", r)
    # df = pd.DataFrame({
    #     "goal": r["goal"],
    #     "method_1": r["method_1"],
    #     "method_2": r["method_2"],
    #     "options_1": r["option_1"],
    #     "option_2": r["option_2"],
    #     "context": r["context_c"],
    #     "question": r["question_g"],
    #     "version_1": r["version_1"],
    #     "version_2": r["version_2"],
    # }, index=[0])
    df = pd.DataFrame({
        "goal": r["goal"],
        "step": r["step"],
        "scale": r["scale"],
        "value_1": r["value_1"],
        "value_2": r["value_2"],
        "options_1": r["option_1"],
        "option_2": r["option_2"],
        "context": r["context_c"],
        "question": r["question"],
        "version_1": r["version_1"],
        "version_2": r["version_2"],
        "edit_1": r["edit_1"],
        "edit_2": r["edit_2"],
    }, index=[0])
    print("DF ", df)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # df.to_csv(f"vignettes_LLM/e2_output_{timestamp}.csv", index=False)
    return df 

# TODO make the single chains components properly modular
def edit_secondary_goals_vignettes(
        df: str,
        model: str = 'text-davinci-003',
        temperature: float = 0.7,
        **kwargs,
):  
    
    model = OpenAI(model_name=model, temperature=temperature, **kwargs)

    goals = []
    values_1 = []
    values_2 = []
    versions_1 = []
    versions_2 = []
    edits_1 = []
    edits_2 = []

    # read csv with old vignettes to edit
    df_in = pd.read_csv(df)[:2]

    with open(os.path.join(INSTRUCTIONS_DIR, 'stage5_correct_preferences.txt'), 'r') as f:
        instructions_edit_text = f.read()

    editing_template = """
    Goal: {goal}
    Aspect 1: {aspect_1}
    Aspect 2: {aspect_2}
    Question 1: {question_1}
    Question 2: {question_2}
    Edit 1: {edit_1}
    Edit 2: {edit_2}
    """

    # ] # potentially reason step by step
    example_selector_s5 = RandomExampleSelector(
        pd.read_csv("../data+analysis/vignette_examples/secondary_goals_editing.csv"), 
        "stage5", 
        "secondary_goals",
    )
    selected_examples_edit = example_selector_s5.select_examples(num_examples=3)
    print("selected examples stage 5 ", selected_examples_edit)
    
    
    for i, r in df_in.iterrows():
        print({"goal": r["goal"],
            "value_1": r["value_1"],
            "value_2": r["value_2"],
            "version_1": r["version_1"],
            "version_2": r["version_2"]})
        goal = r["goal"]
        value_1 = r["value_1"]
        value_2 = r["value_2"]
        version_1 = r["version_1"]
        version_2 = r["version_2"]

        editing_infer_template = """
        Goal: {goal}
        Aspect 1: {value_1}
        Aspect 2: {value_2}
        Question 1: {version_1}
        Question 2: {version_2}
        """
        editing_ex_template = PromptTemplate(
            template = editing_template,
            input_variables = ["goal", "aspect_1", "aspect_2", "question_1", "question_2", "edit_1", "edit_2"], 
        )
        print("Predicting secondary goal")
        # format the few_shot prompt
        few_shot_prompt_editing = FewShotPromptTemplate(
            prefix=instructions_edit_text, 
            examples=selected_examples_edit,
            example_prompt=editing_ex_template, 
            input_variables=["goal", "value_1", "value_2", "version_1", "version_2"],
            suffix=editing_infer_template,
            example_separator="\n\n",
        ) .format(goal = r["goal"],
        value_1 = r["value_1"],
        value_2 = r["value_2"],
        version_1 = r["version_1"],
        version_2 = r["version_2"])  

        print("few_shot_prompt_editing", few_shot_prompt_editing)

        editing_chain = LLMChain(
            llm=model, 
            prompt=few_shot_prompt_editing, 
            verbose=True, 
            output_key="edited_questions"
        ) 
        prediction = editing_chain()
        print("Prediction ", prediction)

        editing_transformation_chain = TransformChain(
            input_variables=["goal", "value_1", "value_2", "version_1", "version_2"], 
            output_variables=["goal_e", "value_1_e", "value_2_e", "version_1_e", "version_2_e", "edit_1", "edit_2"],#["goal_g", "method_1_g", "method_2_g", "option_1_g", "option_2_g", "context_g", "question_g", "version_1", "version_2"],
            transform=transform_edits,
            verbose=True,
        )
        edited_prediction = editing_transformation_chain(**prediction)
        print("edited_prediction ", edited_prediction)
        # overall_chain = SequentialChain(
        #     chains=[editing_chain,
        #             editing_transformation_chain,
        #             ],
        #     input_variables=["goal", "value_1", "value_2", "version_1", "version_2"], ############# THIS IS THE BIT THAT CAUSED THE STR VS DICT INPUT ISSUES #########
        #     # Here we return multiple variables
        #     output_variables=["goal", "value_1", "value_2", "version_1", "version_2", "edit_1", "edit_2"],#["goal", "method_1", "method_2", "option_1", "option_2", "context_c", "question_g", "version_1", "version_2"], # "sampled_goals", "sampled_options", "sampled_context" this is the bit defining how outputs are called at each step and what is returned from the entire chain (otherwise default key of generation is 'text')
        #     verbose=True
        # )
    
    
    
        g, v_1, v_2, ver_1, ver_2, e_1, e_2 = overall_chain(
            inputs=input_dict
        )
        print("------ FINAL OUTPUTS ------ ", g, v_1, v_2, ver_1, ver_2, e_1, e_2)
        goals.append(g)
        values_1.append(v_1)
        values_2.append(v_2)
        versions_1.append(ver_1)
        versions_2.append(ver_2)
        edits_1.append(e_1)
        edits_2.append(e_2)

    df_out = pd.DataFrame({
        "goal": goals,
        "value_1": values_1,
        "value_2": values_2,
        "version_1": versions_1,
        "version_2": versions_2,
        "edit_1": edits_1,
        "edit_2": edits_2,
    })
    print("DF ", df_out)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df_out.to_csv(f"vignettes_LLM/goals_output_{timestamp}_editOnly.csv", index=False)
    return df 



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # add expt as arg 
    parser.add_argument(
        "--expt", 
        type=str, 
        default="prior", 
        help="Experiment for which to sample vignettes", 
        choices=["prior", "goals"]
    )
    parser.add_argument(
        "--n", 
        type=int, 
        default=1, 
        help="Number of vignettes to samples"
    )

    parser.add_argument(
        "--task",
        type=str,
        default="full",
        help="Tasks in the chain to run. If full, runs end to end, otherwise executes one.",
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df = pd.DataFrame()
    
    if args.task == "full":
        if args.expt == "prior":
            print("--- Running chain for priors expt --- ")
            print(f"--- Sampling {args.n} vignettes ---")
            for i in range(args.n):
                d = sample_prior_vignettes(model='gpt-4-turbo', temperature=0.7)
                df = pd.concat([df, d], axis=0)

            df.to_csv(f"vignettes_LLM/prior_output_gpt-4_{timestamp}.csv", index=False)

        elif args.expt == "goals":
            print("--- Running chain for secondary goals expt --- ")
            print(f"--- Sampling {args.n} vignettes ---")
            for i in range(args.n):
                d = sample_secondary_goals_vignettes(model='text-davinci-003', temperature=0.7)
                df = pd.concat([df, d], axis=0) 
            
            df.to_csv(f"vignettes_LLM/goals_output_{timestamp}.csv", index=False)

    else:
        edit_secondary_goals_vignettes(
            df="vignettes_LLM/goals_output_20230424_121924_20_2shot_subgoals.csv",
            model='text-davinci-003', 
            temperature=0.7,
        )
