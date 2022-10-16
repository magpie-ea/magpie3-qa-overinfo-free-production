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
      Please imagine that you are answering the question in a situation like the one described on each screen. 
      Imagine you are trying to be helpful for the questioner.
      Please try to respond intuitively, do not overthink your ratings. 
      <br />
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
     
      <Screen :key="i">
        <Slide>
          <Record
            :data="{
              trialNr: i + 1,
              itemName: trial.itemName,
              settingName: trial.settingName,
              answerOption: trial.variable
            }"
          />
      
         <span
            v-for="(line, lineNumber) of trial.vignette.split('\\n')"
            :key="lineNumber"
          >
            {{ line }}<br /><br />
          </span>
            AnswerOption {{trial.variable}} <br/>
            I {{i}}
            <br/>
            <b>{{trial.value}} </b><br /> <br />
            
            How good is this answer for the questioner?

            <SliderInput
              left="not helpful at all"
              right="very helpful"
              initial="50"
              :response.sync= "$magpie.measurements.rating" 
            />
            
            
            <button
              v-if="$magpie.measurements.rating"
              @click="$magpie.saveAndNextScreen()"
            >
              Submit
            </button>
          
        </Slide>

        </Screen>
        
    
    </template>

    <PostTestScreen />

    <DebugResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials_long.csv';

var group = _.sample(['odd', 'even']);

const trials =
  group == 'odd'
    ? trialsAll.filter((element, index) => {
        return index % 2 === 0;
      })
    : trialsAll.filter((element, index) => {
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
  data() {
    return {
      trials: _.shuffle(trials)
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
