<!-- SliderRatingScreen.vue -->
<template>
    <Screen>
        <span
            v-for="(line, lineNumber) of trial.vignette.split('\\n')"
            :key="lineNumber"
          >
            {{ line }}<br /><br />
          </span>

            <Record
                :data="{
                    trialNr: index + 1,
                    itemName: trial.itemName,
                    settingName: trial.settingName,
                    answerOption: answerOption
                }"
            />
      
            <b>{{trial[answerOption]}} </b><br /> <br />
            
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
    </Screen>
</template>

<script>
export default {
    name: 'SliderRatingScreen',
    props: {
        trial: {
            type: Object,
            required: true
        },
        answerOption: {
            type: String,
            required: true
        },
        index: {
            type: Number,
            required: true
        }
    }
}    
</script>