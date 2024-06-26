<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thank you for taking part in our experiment! 
      <br />
      You are participating in a study conducted by cognitive scientists at the University of Tübingen. 
      Your participation in this research is voluntary.
      You may decline to answer any or all of the following questions.
      You may decline further participation, at any time, without adverse consequences.<br />
      The experiment will take 5-6 minutes.
      <br />
      <br />
      Your anonymity is assured; the researchers who have requested your
      participation will not receive any personal information about you.
      <br />
      <br />
      By pressing the button 'Next' you confirm that you are at least 18 years old and agree to participate in this study. 
    </InstructionScreen>
    <InstructionScreen :title="'Instructions'">
      In the following, you will see short descriptions of scenes in which a
      person asks a question. <b>Your task is to write down an answer to that
      question that the respondent in the scene might provide.</b>
      <br />
      <br />
      Notice that there will also be simple <b>attention checking</b> trials. 
      You will recognize them immediately when you read the important text on each trial carefully -- those trials contain instructions for you to type a certain word in the textbox. 
      Please spell the words exactly as stated in the instructions. 
      <br />
      <br />
      Please answer like you would naturally do if you were in a situation
      like the one described on each screen. <br />
      Please respond naturally and reasonably. <br />
      Please avoid jokes, insults or otherwise making the dialogues into
      something else than simple, harmless exchanges of information.
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
     <template v-if="!trial.type">
      <FreetypingScreen :key=i :trial=trial[0] :trial_type="'main'" :index=i :progress="i / trials.length" :condition=trial[1] :trialAlternatives=trial[2] />     
     </template>
     <template v-else>
      <FreetypingScreen :key=i :trial=trial :trial_type="'filler'" :index=i :progress="i / trials.length" :condition="'filler'" />     
     </template>
    </template>

    <PostTestScreen />

    <SubmitResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trials from '../trials/trials_pilot3_general.csv';
import fillersAll from '../trials/fillers.csv';
import FreetypingScreen from './FreetypingScreen';

var group = _.sample(['odd', 'even']);

const powerSetRecursive = (arr, prefix=[], set=[[]]) => {
  if(arr.length === 0) return// Base case, end recursion
  
  for (let i = 0; i < arr.length; i++) {
      set.push(prefix.concat(arr[i]))// If a prefix comes through, concatenate value
      powerSetRecursive(arr.slice(i + 1), prefix.concat(arr[i]), set)
      // Call function recursively removing values at or before i and adding  
      // value at i to prefix
  }
  return set
};

const createAlternatives = (condition) => {
  // split the condition to get the question and the applicable context
  var questionKey = condition.split("|")[0]
  var contextKey = condition.split("|")[1]
  console.log(condition)
  console.log(questionKey)
  console.log(contextKey)
  if (contextKey == "yes") {
    var alternativesPowerset = [['optionA', 'optionB', 'optionC'], ['optionA'], ['optionA', 'optionB'], ['optionA', 'optionC']];
  } else {
    var alternativesPowerset = powerSetRecursive( _.shuffle(['optionB', 'optionC']));
  }
  // remove the empty set
  alternativesPowerset.shift();
  console.log(alternativesPowerset);
  // select a random alternative set
  var alternativeOrder = _.sample(alternativesPowerset);

  return alternativeOrder
};

var allOptions = ['optionA', 'optionB', 'optionC'];

const n_vignettes = 6;
const n_fillers = 1;
// trials types to be used in expt (equal number of high and low prior trials)
const trial_types = _.shuffle(['question_any', 'question_any', 'question_optionA|yes', 'question_optionA|no', 'question_optionA|yes', 'question_optionA|no']);
const trial_alternatives = trial_types.map(createAlternatives);
console.log("trial_alternatives")
console.log(trial_alternatives);
// sample main trials
const selected_trials =_.sampleSize(trials, n_vignettes);
// combine trials and their types at random
const trials_w_types = _.zip(selected_trials, trial_types, trial_alternatives);

const fillers =
  group == 'odd'
    ? fillersAll.filter((element, index) => {
        return index % 2 === 0;
      })
    : fillersAll.filter((element, index) => {
        return index % 2 != 0;
      });

// Disable selecting text
// Supported by the following browsers:
// https://caniuse.com/mdn-api_document_selectstart_event
document.onselectstart = () => false;

// Disable context menu
// Supported by the following browsers:
// https://caniuse.com/mdn-api_element_contextmenu_event
document.oncontextmenu = () => false;

export default {
  name: 'App',
  components: { FreetypingScreen },
  data() {
    return {
      trials: _.shuffle(_.concat( trials_w_types, _.sampleSize(fillers, n_fillers)))
    };
  },
  computed: {
    // Expose lodash to template code
    _() {
      return _;
    }
  }
};
</script>
<style>
body {
  /*
  Disable selecting text via css
  Supported by the following browsers
  https://caniuse.com/mdn-css_properties_user-select
  */
  user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -webkit-user-select: none;
}
</style>
