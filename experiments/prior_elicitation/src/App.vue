<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment! It will take approximately 4-5 minutes.
      <br />
      <br />
      In this study we are interested in how you think about other people.
      On each trial, you will be given some information about a person: 'Suppose someone wants to have Italian food.'
      <br />
      Then we'll ask how happy you think this person would be about other things, given this information. For instance, we might ask: 'How happy do you think they would be if they had French food instead?'
      You'll use sliders to answer the questions. 
      <br />
      <br />
      Notice that there will also be simple <b>attention checking trials</b>. 
      You will recognize them immediately when you read the important text on each trial carefully -- those trials contain instructions for you to move the sliders in a certain way. 
      Please follow these instructions on the respective trial. 
      <br />
      <br />
      In some cases, you'll think the person would be much less happy, given the information you learned about the person. In other cases you'll think they'll be much happier. Sometimes the information about the person won't tell you anything, in which case you should move the slider to the midpoint. <br />
      Please try to respond naturally and reasonably, do not overthink your ratings. <br />
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
        <template v-if="trial.length == 2">       
          <ParallelRatingScreen 
              :key=i 
              :trial=trial[0] 
              :index=i 
              :trial_type="'main'" 
              :targetOption="trial[1]"
              :progress="i / trials.length" 
              :itemOrder="_.shuffle(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2', 'itemQuestion'])" 
          />      
        
        </template>
        <template v-else>
          <ParallelRatingScreen 
              :key=i 
              :trial=trial 
              :index=i 
              :trial_type="'filler'" 
              :targetOption="'itemQuestion'"
              :progress="i / trials.length" 
              :itemOrder="_.shuffle(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2', 'itemQuestion'])" 
          />   
        </template>
    </template>

    <PostTestScreen />

    <DebugResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials_split_priorElicitation_pilot2.csv';
import fillersAll from '../trials/fillers_split_priorElicitation_pilot2.csv';
import ParallelRatingScreen from './ParallelRatingScreen';

var group = _.sample(['odd', 'even']);

const n_vignettes = 1;
const n_fillers = 1;

const trials =
  // group == 'odd'
     trialsAll.filter((element, index) => {
        return _.includes([ _.sample(["cafe-pie", "electronics-laptop"]), _.sample(["plants-green", "furniture-outdoors"])], element["itemName"]);
      });
  // : trialsAll.filter((element, index) => {
  //      return index % 2 != 0;
  //    });
const repeating_trials = _.sampleSize(trials, n_vignettes).map(x => _.fill(Array(6), x)).flat()
const repeating_targets = Array(_.sampleSize(trials, n_vignettes).length).fill(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2', 'itemQuestion']).flat()
const trials_w_target = _.zip(repeating_trials, repeating_targets)
console.log("trails_w_target")
console.log(repeating_trials)
console.log("targets ", repeating_targets)
console.log(trials_w_target)

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
  components: { ParallelRatingScreen },
  data() {
    return {
      trials: _.shuffle(_.concat( trials_w_target, _.sampleSize(fillers, n_fillers)))
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
