<!-- FreetypingScreen.vue -->
<template>
    <Screen :progress="progress">
        <Slide>
          <Record
            :data="{
              trialNr: index + 1,
              itemName: trial.itemName,
              trial_type: trial_type,
              correct_response: trial.correct_response,
              condition: condition
            }"
          />

          <span
            v-for="(line, lineNumber) of createScreen.split('\\n')"
            :key="lineNumber"
          >
            {{ line }}<br />
          </span>
          <textarea
            v-model="$magpie.measurements.answer"
            style="width: 500px; height: 200px"
          />

          <button
            v-if="
              $magpie.measurements.answer &&
              $magpie.measurements.answer.length > 1
            "
            @click="$magpie.saveAndNextScreen()"
          >
            Submit
          </button>
        </Slide>
      </Screen>
</template>

<script>
import _ from 'lodash';


function createText(trial, condition, trial_type){
      if (trial_type == 'filler'){
        // shuffle the order of the alternatives
        var itemOrder = _.shuffle(['competitor', 'sameCategory', 'otherCategory'])
        console.log(itemOrder)
        var vignette_start = trial.vignette_start
        var vignette_continuation = trial.vignette_continuation
        var question = trial.question
        console.log(trial.correct_response)
        var context = itemOrder.map(x => trial[x])
        context.splice(-1, 1, "and ".concat(context.at(-1)));
        var context = context.join(", ").concat(".");
        var slide_text = [vignette_start, context, vignette_continuation, "\"".concat(question).concat("\""), "\\n\\n", "You reply: "].join(" ");
        return slide_text
      } else {

        const powerSetRecursive = (arr, prefix=[], set=[[]]) => {
          if(arr.length === 0) return// Base case, end recursion
          
          for (let i = 0; i < arr.length; i++) {
              set.push(prefix.concat(arr[i]))// If a prefix comes through, concatenate value
              powerSetRecursive(arr.slice(i + 1), prefix.concat(arr[i]), set)
              // Call function recursively removing values at or before i and adding  
              // value at i to prefix
          }
          return set
        }
        var allOptions = ['optionA', 'optionB', 'optionC'];
        
        // retrieve question corresponding to condition
        var continuation = trial['continuation']
        console.log(continuation)
        var vignette_start = trial.context_begin
        var vignette_continuation = trial.context_cont
        // split the condition to get the question and the applicable context
        var questionKey = condition.split("|")[0]
        var contextKey = condition.split("|")[1]
        var question = trial[questionKey]
        console.log(condition)
        console.log(questionKey)
        console.log(contextKey)
        if (contextKey == "yes") {
          var alternativesPowerset = powerSetRecursive( _.shuffle(['optionA', 'optionB', 'optionC']));
        } else {
          var alternativesPowerset = powerSetRecursive( _.shuffle(['optionB', 'optionC']));
        }
        // remove the empty set
        alternativesPowerset.shift();
        console.log(alternativesPowerset);
        // select a random alternative set
        var alternativeOrder = _.sample(alternativesPowerset)
        console.log(alternativeOrder)

        // retrieve the alternatives in the randomized order
        var context = allOptions.map(x => trial[x])
        // add and before the last alternative
        context.splice(-1, 1, "and ".concat(context.at(-1))).concat(".");
        var context = context.join(", ").concat(".");

        var available_alternatives = alternativeOrder.map(x => trial[x])
        if (available_alternatives.length > 1) {
          available_alternatives.splice(-1, 1, "and ".concat(available_alternatives.at(-1)));
        } 
        var available_alternatives = available_alternatives.join(", ").concat(".");
        var question_prep = trial['question_prep']
        
        var answerTemplate = trial.answer_template
        var slide_text = [[
          [vignette_start, context].join(" "), [continuation, available_alternatives].join(" ")].join("\\n"), [question_prep, question].join(" "), answerTemplate].join("\\n\\n"); //context.join(", ").concat(".");
        console.log(slide_text)
        // var slide_text = [vignette_start, context, vignette_continuation, "\"".concat(question).concat("\""), "\\n\\n", "You reply: "].join(" ");
        return slide_text
      }
};

export default {
    name: 'SliderRatingScreen',
    props: {
        trial: {
          type: Object,
          required: true
        },
        trial_type: {
          type: String,
          required: true
        },
        index: {
          type: Number,
          required: true
        },
        progress: {
          type: Number,
          default: undefined
        },
        condition: {
          type: String,
          default: undefined
        }
    },
    methods: {
      createText
    },
    computed: {
      createScreen(){
        return createText(this.trial, this.condition, this.trial_type)
      }
    }
};  
</script>