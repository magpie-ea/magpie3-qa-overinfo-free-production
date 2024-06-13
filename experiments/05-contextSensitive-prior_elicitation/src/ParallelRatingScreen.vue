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
          targetOption: targetOption,
        }"
      />

      
      <span v-html="createContext(trial, targetOption)">
      </span>
      <p>How useful do you think they would find it if...</p>
      <br />

      <span v-html="createAnswerOption(trial, itemOrder[0], targetOption)"></span>
      <SliderInput
        left="completely useless"
        right="very useful"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[0]]
      />
      

      <span v-html="createAnswerOption(trial, itemOrder[1], targetOption)"></span>
      <SliderInput
        left="completely useless"
        right="very useful"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[1]]
      />
     

      <span v-html="createAnswerOption(trial, itemOrder[2], targetOption)"></span>
      <SliderInput
        left="completely useless"
        right="very useful"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[2]]
      />
      

      <span v-html="createAnswerOption(trial, itemOrder[3], targetOption)"></span>
      <SliderInput
        left="completely useless"
        right="very useful"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[3]]
      />

      <span v-html="createAnswerOption(trial, itemOrder[4], targetOption)"></span>
      <SliderInput
        left="completely useless"
        right="very useful"
        initial="50"
        :response.sync=$magpie.measurements[itemOrder[4]]
      />
      
      <button
        v-if="checkResponses(
            $magpie.measurements[itemOrder[0]],
            $magpie.measurements[itemOrder[1]],
            $magpie.measurements[itemOrder[2]],
            $magpie.measurements[itemOrder[3]],
            $magpie.measurements[itemOrder[4]],
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

function createContext(trial, targetOption) {
    var target = trial[targetOption];
    var slide_text = [trial["priorElicitation_context"], " <b>", target, ".</b>"].join("");
    return slide_text
}

function createAnswerOption(trial, option, targetOption) {  
      if (targetOption == option) {
        var alternative = trial[option];
        var slide_text = ["<br/>","... they actually ", trial["priorElicitation_question"], " <b>", alternative, "</b>?"].join(""); // set to this to avoid incorrect formulation
      } else {
        var alternative = trial[option];
        var slide_text = ["<br/>","... they ", trial["priorElicitation_question"], " <b>", alternative, "</b> instead?"].join("");
      }
      
      //if (option != "itemQuestion") {
      //  var slide_text = ["<br/>","... they ", trial["priorElicitation_question"], " <b>", alternative, "</b> instead?"].join("");
      //} else {
      //  var slide_text = ["<br/>","... they ", trial["priorElicitation_question"], " <b>", alternative, "</b>?"].join("");
      //}
      
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
        targetOption: {
          type: String,
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