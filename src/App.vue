<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment!
      <br />
      <br />
      In the following, you will see short descriptions of scenes in which a
      character asks a question. Please read them very carefully, even if they appear to be repeated and you think that you remember them well enough. 
      <br />
      Below, you will see a possible answer to that question. 
      <b>Your task is to rate how likely it is that the answer provides helpful information for the questioner.</b>
      <br />
      <br />
      Notice that there will also be simple attention checking trials. 
      You will recognize them immediately when you read the important text on each trial carefully - those trials contain instructions for you to move the slider in a certain way. 
      Please follow those instructions.
      <br />
      <br />
      Please imagine that you are answering the question in a situation like the one described on each screen. 
      Imagine you are trying to be helpful for the questioner.
      Please try to respond intuitively, do not overthink your ratings. 
      <br />
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
      <template v-if="!trial.type">
       <template
            v-for="(answerOption, index) of _.shuffle(['taciturn', 'competitor', 'sameCategory', 'otherCategory', 'fullList'])"
       >         
         <SliderRatingScreen :key=i :trial=trial :answerOption=answerOption :index=i :progress="i / trials.length"/>      
       </template>
      </template>
      <template v-else>
        <SliderRatingScreen :key=i :trial=trial :answerOption='filler' :index=i :progress="i / trials.length"/>   
      </template>
    </template>

    <PostTestScreen />

    <DebugResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials_extended.csv';
import fillersAll from '../trials/fillers.csv';
import SliderRatingScreen from './SliderRatingScreen';

var group = _.sample(['odd', 'even']);

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
  components: { SliderRatingScreen },
  data() {
    return {
      trials: _.shuffle(_.concat(trials, fillers))
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
