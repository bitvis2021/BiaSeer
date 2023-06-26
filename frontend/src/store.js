import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	displayMode: 'vis',
    // Specify the current media in order to display a feature trend view; 
    // Ultimately, it can be replaced with a global feature trend view.
    currMedium: 'msn.com',
  },
  mutations: {
    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode;
    },
    ['UPDATE_CURRENT_MEDIUM'] (state, currMedium) {
      console.log(currMedium);
      state.currMedium = currMedium;
    },
  },
  actions: {
  }
})
