<!-- ParallelRatingScreen.vue -->
<template>
  <Screen :progress="progress">
    <Slide>
      <Record
        :data="{
          trialNr: index + 1,
          itemName: trial.itemName,
          settingName: trial.settingName,
          trial_type: trial_type,
          itemOrder: itemOrder.join(','),
        }"
      />

      
      <span v-html="createContext(trial)">
      </span>
      <p>How much does that change your beliefs about whether they would also...</p>
      <br />

      <span v-html="createAnswerOption(trial, itemOrder[0])"></span>
      <SliderInput
        left="makes it much less likely"
        right="makes it much more likely"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[0]]
      />
      <p style="color:grey; margin-top: -25px;">no change at all</p>

      <span v-html="createAnswerOption(trial, itemOrder[1])"></span>
      <SliderInput
        left="makes it much less likely"
        right="makes it much more likely"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[1]]
      />
      <p style="color:grey; margin-top: -25px;">no change at all</p>

      <span v-html="createAnswerOption(trial, itemOrder[2])"></span>
      <SliderInput
        left="makes it much less likely"
        right="makes it much more likely"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[2]]
      />
      <p style="color:grey; margin-top: -25px;">no change at all</p>

      <span v-html="createAnswerOption(trial, itemOrder[3])"></span>
      <SliderInput
        left="makes it much less likely"
        right="makes it much more likely"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[3]]
      />
      <p style="color:grey; margin-top: -25px;">no change at all</p>

      <span v-html="createAnswerOption(trial, itemOrder[4])"></span>
      <SliderInput
        left="makes it much less likely"
        right="makes it much more likely"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[4]]
      />
      <p style="color:grey; margin-top: -25px;">no change at all</p>

      
      <button
        v-if="checkResponses(
            $magpie.measurements[itemOrder[0]],
            $magpie.measurements[itemOrder[1]],
            $magpie.measurements[itemOrder[2]],
            $magpie.measurements[itemOrder[3]],
            $magpie.measurements[itemOrder[4]]
        )"
        @click="$magpie.saveAndNextScreen()"
      >
        Submit
      </button>
    </Slide>
  </Screen>
</template>

<script>
function orderAlternativesByIndex(inds, trial, itemOrder) {
  // sort indices of the relevant alternatives
  inds.sort();
  var orderedAlternatives = inds.map(x => trial[itemOrder[x]]);
  // add and before last alternative
  orderedAlternatives.splice(-1, 1, "and ".concat(orderedAlternatives.at(-1)));
  orderedAlternatives = orderedAlternatives.join(", ");
  return orderedAlternatives
}

function createContext(trial) {
    var target = trial["itemQuestion"];
    var slide_text = [trial["priorElicitation_context"], " <b>", target, ".</b>"].join("");
    return slide_text
}

function createAnswerOption(trial, option) {  
      var alternative = trial[option];
      
      var slide_text = ["<br/>", trial["priorElicitation_question"], " <b>", alternative, "</b>?"].join("");
      return slide_text
}
export default {
  name: 'ParallelRatingScreen',
  data(){
    return {response: 0}
  },
  props: {
    trial: {
            type: Object,
            required: true
        },
        index: {
            type: Number,
            required: true
        },
        trial_type: {
          type: String,
          required: true
        },
        progress: {
          type: Number,
          default: undefined
        },
        itemOrder: {
            type: Array,
            required: true
        },
  },
  methods: {
    checkResponses: function (a, b, c, d, e) {
      return !(isNaN(a) | isNaN(b) | isNaN(c) | isNaN(d) | isNaN(e));
    },
    createAnswerOption,
    createContext
  }
};
</script>