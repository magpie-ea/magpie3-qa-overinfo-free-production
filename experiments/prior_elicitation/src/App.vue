<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment! It will take approximately 7-8 minutes.
      <br />
      <br />
      In this study we are interested in how you think about other people.
      On each trial, you will be given some information about a person: 'Suppose you learn someone likes Italian food.'
      <br />
      Then we'll ask whether this information changes your opinion about several other things. For instance, we might ask: 'How much does that change your beliefs about whether they like spaghetti?'
      You'll use sliders to answer the questions. 
      <br />
      <br />
      Notice that there will also be simple attention checking trials. 
      You will recognize them immediately when you read the important text on each trial carefully -- those trials contain instructions for you to move the sliders in a certain way. 
      Please follow these instructions on the respective trial. 
      <br />
      <br />
      In some cases, you'll think the described events are now much less likely, given the information you learned about the person. In other cases you'll think the events are much more likely. Sometimes the information about the person won't tell you anything, in which case you should move the slider to the midpoint. <br />
      Please try to respond naturally and reasonably, do not overthink your ratings. <br />
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
      <template v-if="!trial.type">
               
         <ParallelRatingScreen 
            :key=i 
            :trial=trial 
            :index=i 
            :trial_type="'main'" 
            :progress="i / trials.length" 
            :itemOrder="_.shuffle(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2'])" 
         />      
       
      </template>
      <template v-else>
        <ParallelRatingScreen 
            :key=i 
            :trial=trial 
            :index=i 
            :trial_type="'filler'" 
            :progress="i / trials.length" 
            :itemOrder="_.shuffle(['competitor', 'sameCategory1', 'sameCategory2', 'otherCategory1', 'otherCategory2'])"
        />   
      </template>
    </template>

    <PostTestScreen />

    <SubmitResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials_split.csv';
import fillersAll from '../trials/fillers_split.csv';
import ParallelRatingScreen from './ParallelRatingScreen';

var group = _.sample(['odd', 'even']);

const n_vignettes = 8;
const n_fillers = 3;

const trials =
  group == 'odd'
    ? trialsAll.filter((element, index) => {
        return index % 2 === 0;
      })
    : trialsAll.filter((element, index) => {
        return index % 2 != 0;
      });
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
      trials: _.shuffle(_.concat( _.sampleSize(trials, n_vignettes), _.sampleSize(fillers, n_fillers)))
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
