<template>
  <div>
    <b-alert
      :show="dismissCountDown"
      :variant="alertvariant"
      dismissible
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
      >
      <span class="message">
      {{ message }}
      </span>
    </b-alert>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
    alertvariant: String,
  },
  data() {
    return {
      dismissCountDown: 0,
    };
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert(dismissSecs) {
      this.dismissCountDown = dismissSecs;
    },
  },
};
</script>
