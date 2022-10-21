<!-- SliderRatingScreen.vue -->
<template>
    <Screen>
        <span
            v-for="(line, lineNumber) of createScreen.split('\\n')"
            :key="lineNumber"
          >
            {{ line }}<br/>
          </span>

            <Record
                :data="{
                    trialNr: index + 1,
                    itemName: trial.itemName,
                    settingName: trial.settingName,
                    answerOption: answerOption
                }"
            />

            <br/>
            <br/>
            How good is this answer for the questioner?

            <SliderInput
              left="not helpful at all"
              right="very helpful"
              initial=50
              :response.sync= "$magpie.measurements.rating" 
            />
            <button
              v-if="$magpie.measurements.rating"
              @click="$magpie.saveAndNextScreen()"
            >
              Submit
            </button>
            <button
              v-else-if="$magpie.measurements.rating == 0"
              @click="$magpie.saveAndNextScreen()"
            >
              Submit
            </button>
    </Screen>
</template>

<script>
import _ from 'lodash';
function orderAlternativesByIndex(inds, trial, itemOrder) {
  // sort indices of the relevant alternatives
  inds.sort();
  var orderedAlternatives = inds.map(x => trial[itemOrder[x]]);
  // add and before last alternative
  orderedAlternatives.splice(-1, 1, "and ".concat(orderedAlternatives.at(-1)));
  orderedAlternatives = orderedAlternatives.join(", ");

  return orderedAlternatives
}

function createText(trial, option){
      // shuffle the order of the alternatives
      var itemOrder = _.shuffle(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2'])
      console.log(itemOrder)
      var vignette_start = trial.vignette_start
      var vignette_continuation = trial.vignette_continuation
      var question = trial.question
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
      var context = itemOrder.map(x => trial[x])
      context.splice(-1, 1, "and ".concat(context.at(-1)));
      var context = context.join(", ").concat(".");
      var slide_text = [vignette_start, context, vignette_continuation, question, "\\n\\n", "You reply: ", "\"".concat(taciturn), answer.concat("\"")].join(" ");
      return slide_text
};

export default {
    name: 'SliderRatingScreen',
    props: {
        trial: {
            type: Object,
            required: true
        },
        answerOption: {
            type: String,
            required: true
        },
        index: {
            type: Number,
            required: true
        }
    },
    methods: {
      createText
    },
    computed: {
      createScreen(){
        return createText(this.trial, this.answerOption)
      }
    }
};  
</script>