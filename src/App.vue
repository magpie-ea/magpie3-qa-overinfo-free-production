<template>
<Experiment title="magpie demo">
  <InstructionScreen :title="'Welcome'">
    This is a sample introduction screen.
  </InstructionScreen>

  <template v-for="(trial, i) in trials">
    <Screen>

      <Slide>

      <Record
        :data="{
          trialNr: i + 1,
          itemName: trial.itemName,
          settingName: trial.settingName
        }"
      />

        <span
         v-for="(line,lineNumber) of trial.vignette.split('\\n')"
         v-bind:key="lineNumber" >
         {{ line }}<br/>
        </span>

        <TextareaInput
          :response.sync= "$magpie.measurements.answer"
          />

        <button v-if= "$magpie.measurements.answer && $magpie.measurements.answer.length > 2"
                @click="$magpie.saveAndNextScreen();">
          Submit
        </button>
      </Slide>

    </Screen>

</template>

    <SubmitResultsScreen />
  </Experiment>
</template>

<script>
import _ from 'lodash';
import trialsAll from '../trials/trials.csv';

var group = _.sample(['odd', 'even']);


const trials = group == 'odd' ?
      trialsAll.filter((element, index) => {
        return (index % 2 === 0);
      }) :
      trialsAll.filter((element, index) => {
        return (index % 2 != 0);
      });

console.log(group, trials)

console.log('test')

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
