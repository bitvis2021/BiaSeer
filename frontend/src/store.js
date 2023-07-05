import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	displayMode: 'vis',
    // Specify the current media in order to display a feature trend view; 
    // Ultimately, it can be replaced with a global feature trend view.
    currMedium: 'msn.com',
    mediaMatrixSelectedSignal: 1, // signal media matrix selected
  },
  mutations: {
    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode;
    },
    ['UPDATE_CURRENT_MEDIUM'] (state, currMedium) {
      console.log(currMedium);
      state.currMedium = currMedium;
    },
    ['UPDATE_MATRIX_SELECTED_SIGNAL'] (state) {
      console.log(state.mediaMatrixSelectedSignal);
      state.mediaMatrixSelectedSignal = (state.mediaMatrixSelectedSignal + 1) % 5;
    },
  },
  actions: {
  }
})
