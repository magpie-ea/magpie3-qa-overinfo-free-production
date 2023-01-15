<!-- FreetypingScreen.vue -->
<template>
    <Screen :progress="progress">
        <Slide>
          <Record
            :data="{
              trialNr: index + 1,
              itemName: trial.itemName,
              settingName: trial.settingName,
              trial_type: trial_type,
              correct_response: trial.correct_response
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
              $magpie.measurements.answer.length > 4
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

function createText(trial){
      // shuffle the order of the alternatives
      var itemOrder = _.shuffle(['competitor', 'mostSimilar', 'sameCategory', 'otherCategory'])
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
};

export default {
    name: 'FreetypingScreen',
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
        }
    },
    methods: {
      createText
    },
    computed: {
      createScreen(){
        return createText(this.trial)
      }
    }
};  
</script>