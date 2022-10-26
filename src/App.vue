<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment!
      <br />
      <br />
      In the following, you will see short descriptions of scenes in which a
      character asks a question. Please read them very carefully, even if they appear to be repeated and you think that you remember them well enough.
      <br />
      You will see a possible answer to that question. 
      <b>Your task is to rate how likely it is that you would provide that answer to the questioner.</b>
      <br />
      <br />
      Notice that there will also be simple attention checking trials. 
      You will recognize them immediately when you read the important text on each trial carefully -- those trials contain instructions for you to move the slider in a certain way. 
      Please follow those instructions in the text and ignore the instructions appearing above the rating slider.
      <br />
      <br />
      Please imagine that you are answering the question in a situation like the one described on each screen. 
      Imagine you are trying to be helpful for the questioner.
      Please try to respond intuitively, do not overthink your ratings. 
      <br />
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
            :answerOptionsOrder="_.shuffle(['taciturn', 'competitor', 'sameCategory', 'otherCategory', 'fullList'])"
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
            :answerOptionsOrder="_.shuffle(['taciturn', 'competitor', 'sameCategory', 'otherCategory', 'fullList'])"
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
import SliderRatingScreen from './SliderRatingScreen';
import ParallelRatingScreen from './ParallelRatingScreen';

var group = _.sample(['odd', 'even']);

const n_vignettes = 4;

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
      trials: _.shuffle(_.concat(_.sampleSize(trials, n_vignettes), fillers))
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
