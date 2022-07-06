<template>
  <Experiment title="question-answering-experiment">

    <InstructionScreen :title="'Welcome'">
      Thanks for taking part in our experiment!
      <br />
      <br />
      In the following, you will see short descriptions of scenes in which a
      character asks a question. Your task is to write down an answer to that
      question.
      <br />
      <br />
      Please answer like you would naturally do when you were in a situation
      like the one described on each screen. <br />
      Please respond naturally and reasonably. <br />
      Please avoid jokes, insults or otherwise making the dialogues into
      something else than simple, harmless exchanges of information.
    </InstructionScreen>

    <template v-for="(trial, i) in trials">
      <Screen :key="i">
        <Slide>
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
            {{ line }}<br />
          </span>

          <textarea
            v-model="$magpie.measurements.answer"
            style="width: 500px; height: 200px"
          />

          <button
            v-if="
              $magpie.measurements.answer &&
              $magpie.measurements.answer.length > 2
            "
            @click="$magpie.saveAndNextScreen()"
          >
            Submit
          </button>
        </Slide>
      </Screen>
    </template>

    <PostTestScreen />

    <SubmitResultsScreen />

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
