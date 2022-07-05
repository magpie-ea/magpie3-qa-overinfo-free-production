<template>
<Experiment title="magpie demo">
  <InstructionScreen :title="'Welcome'">
    This is a sample introduction screen.
  </InstructionScreen>

  <template v-for="(trial, i) in trials">
    <Screen>

      <Slide>

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
import trials from '../trials/trials.csv';

export default {
  name: 'App',
  data() {
    return {
      trials: trials
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
