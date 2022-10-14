<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment!
      <br />
      <br />
      In the following, you will see short descriptions of scenes in which a
      character asks a question. Below, you will see different possible answers to that question. 
      Your task is to rate how likely it is for each of the answers to provide helpful information for the questioner.
      <br />
      <br />
      Please imagine that you are answering the question in a situation like the one described on each screen. 
      Imagine you are trying to be helpful for the questioner.
      Please try to respond intuitively, do not overthink your ratings. <br />
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
      

      <Screen :key="i">

      <template
            v-for="(answerOption, index) of [trial.taciturn, trial.competitor, trial.sameCategory, trial.otherCategory, trial.fullList]"
            
      >
        <Slide :key="index">
          <Record
            :data="{
              trialNr: i + 1,
              itemName: trial.itemName,
              settingName: trial.settingName
            }"
          />
      
         <span
            v-for="(line, lineNumber) of trial.vignette.split('\\n')"
            :key="lineNumber"
          >
            {{ line }}<br /><br />
          </span>
          
            {{answerOption}} <br />
            <SliderInput
              left="not helpful at all"
              right="very helpful"
              :response.sync= "$magpie.measurements.rating" 
            />
            
            <button
              v-if="
                $magpie.measurements.rating &&
                index < 4
              "
              @click="$magpie.addTrialData({
                rating: $magpie.measurements.rating, 
                answerOption: answerOption,
                trialNr: i + 1,
              itemName: trial.itemName,
              settingName: trial.settingName
              }); $magpie.nextSlide()"
            >
              Submit
            </button>
            <button
              v-else-if="
                index == 4
              "
              @click="$magpie.addTrialData({
                rating: $magpie.measurements.rating, 
                answerOption: answerOption,
                trialNr: i + 1,
              itemName: trial.itemName,
              settingName: trial.settingName
              }); $magpie.nextScreen()"
            >
              Submit
            </button>
          
        </Slide>
        </template>
        
      </Screen>

      
    
    </template>

    <PostTestScreen />

    <DebugResultsScreen />

  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials.csv';

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
