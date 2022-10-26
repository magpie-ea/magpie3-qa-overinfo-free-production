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
          itemOrder: itemOrder,
          answerOptionsOrder: answerOptionsOrder
        }"
      />

      
      <span v-html="createContext(trial, itemOrder)">
      </span>
      <p>How likely is it that you would provide each of these responses?</p>
      <br />

      <span v-html="createAnswerOption(trial, answerOptionsOrder[0], itemOrder)"></span>
      <SliderInput
        left="very unlikely"
        right="very likely"
        initial="20"
        :response.sync=$magpie.measurements[answerOptionsOrder[0]]
      />

      <span v-html="createAnswerOption(trial, answerOptionsOrder[1], itemOrder)"></span>
      <SliderInput
        left="very unlikely"
        right="very likely"
        initial="20"
        :response.sync=$magpie.measurements[answerOptionsOrder[1]]
      />
      <span v-html="createAnswerOption(trial, answerOptionsOrder[2], itemOrder)"></span>
      <SliderInput
        left="very unlikely"
        right="very likely"
        initial="20"
        :response.sync=$magpie.measurements[answerOptionsOrder[2]]
      />
      <span v-html="createAnswerOption(trial, answerOptionsOrder[3], itemOrder)"></span>
      <SliderInput
        left="very unlikely"
        right="very likely"
        initial="20"
        :response.sync=$magpie.measurements[answerOptionsOrder[3]]
      />
      <span v-html="createAnswerOption(trial, answerOptionsOrder[4], itemOrder)"></span>
      <SliderInput
        left="very unlikely"
        right="very likely"
        initial="20"
        :response.sync=$magpie.measurements[answerOptionsOrder[4]]
      />

      
      <button
        v-if="checkResponses(
            $magpie.measurements[answerOptionsOrder[0]],
            $magpie.measurements[answerOptionsOrder[1]],
            $magpie.measurements[answerOptionsOrder[2]],
            $magpie.measurements[answerOptionsOrder[3]],
            $magpie.measurements[answerOptionsOrder[4]]
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

function createContext(trial, itemOrder){
      console.log(itemOrder)
      var vignette_start = trial.vignette_start
      var vignette_continuation = trial.vignette_continuation
      var question = trial.question
      var context = itemOrder.map(x => trial[x])
      context.splice(-1, 1, "and ".concat(context.at(-1)));
      var context = context.join(", ").concat(".");
      var slide_text = [vignette_start, context, "<br/><br/>", vignette_continuation, "<b>", "\"".concat(question).concat("\""), "</b>", "<br/><br/>"].join(" ");
      return slide_text
};

function createAnswerOption(trial, option, itemOrder) {
      var taciturn = trial.taciturn
      var answerTemplate = trial.answer_template

      if (option == 'competitor' ){
        var orderedAlternatives = trial['competitor']

      } else if (option == 'sameCategory') {
        // compute index or respective elements in itemOrder

        // TODO competitor missing 
        var sameCat1 = itemOrder.indexOf('sameCategory1');
        var sameCat2 = itemOrder.indexOf('sameCategory2');
        var comp = itemOrder.indexOf('competitor');
        var orderedAlternatives = orderAlternativesByIndex([comp, sameCat1, sameCat2], trial, itemOrder)

      } else if (option == 'otherCategory') {
        // compute index or respective elements in itemOrder
        var otherCat1 = itemOrder.indexOf('otherCategory1')
        var otherCat2 = itemOrder.indexOf('otherCategory2')
        var orderedAlternatives = orderAlternativesByIndex([otherCat1, otherCat2], trial, itemOrder)
        
      } else if (option == 'taciturn') {
        var orderedAlternatives = trial['taciturn']
        
      } else {
        // filler condition and context
        var orderedAlternatives = itemOrder.map(x => trial[x]);
        orderedAlternatives.splice(-1, 1, "and ".concat(orderedAlternatives.at(-1)));
        orderedAlternatives = orderedAlternatives.join(", ");
        
      }
      // construct slide text
      if (option != 'taciturn') {
        var answer = answerTemplate.replace("*", orderedAlternatives);
      }  else {
        var answer = ""; 
      }
      
      var slide_text = ["<br/>You reply: ", "<b>", "\"".concat(taciturn), answer.concat("\""), "</b>"].join(" ");
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
        answerOptionsOrder: {
            type: Array,
            required: true
        }
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