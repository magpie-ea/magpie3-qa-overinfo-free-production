<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thank you for taking part in our experiment! 
      <br />
      You are participating in a study conducted by cognitive scientists at the University of Tübingen. 
      Your participation in this research is voluntary.
      You may decline to answer any or all of the following questions.
      You may decline further participation, at any time, without adverse consequences.
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
      character asks a question. Your task is to write down an answer to that
      question.
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
      <FreetypingScreen :key=i :trial=trial :trial_type="'main'" :index=i :progress="i / trials.length" />     
     </template>
     <template v-else>
      <FreetypingScreen :key=i :trial=trial :trial_type="'filler'" :index=i :progress="i / trials.length" />     
     </template>
    </template>
  
    <PostTestScreen />

    <SubmitResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials_split_cogsci_pilot4.csv';
import fillersAll from '../trials/fillers_split_priorElicitation_pilot2.csv';
import FreetypingScreen from './FreetypingScreen';

var group = _.sample(['odd', 'even']);

const n_vignettes = 4;
const n_fillers = 1;

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
  components: { FreetypingScreen },
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
