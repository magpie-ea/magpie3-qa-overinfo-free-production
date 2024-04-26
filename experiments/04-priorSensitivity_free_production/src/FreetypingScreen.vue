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
              $magpie.measurements.answer.length > 3
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
        // retrieve text corresponding to condition
        var continuation = trial[condition]
        console.log(continuation)
        // var vignette_start = trial.vignette_start
        // var vignette_continuation = trial.vignette_continuation
        var question = trial.question
        // console.log(trial.correct_response)
        var context = trial.context //itemOrder.map(x => trial[x])
        var answerTemplate = trial.answer_template
        // context.splice(-1, 1, "and ".concat(context.at(-1)));
        var slide_text = [context, continuation, question, answerTemplate].join("\\n\\n"); //context.join(", ").concat(".");
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