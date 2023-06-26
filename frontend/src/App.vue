<template>
  <div id="app" v-if="!loadingData">
    <div class="media-topic">
      <div class="media-topic-vector-reduction-view"></div>
      <div class="media-topic-difference-concat-view"></div>
    </div>
    <div class="event-evolution">
      <div class="union-event-evolution"></div>
      <div class="single-event-evolution"></div>
    </div>
  </div>
</template>

<script>


export default {
  name: 'App',
  data() {
    return {
      loadingData: false,
    }
  },
  components: {

  }
}
</script>

<style lang="less">
div{
  border-radius: 5px;
  margin: 1.5px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow-x: hidden;
  overflow-y: hidden;
  .media-topic{
    position: absolute;
    top: 0%;
    bottom: 65%;
    left: 0%;
    right: 0%;
    // background-color: steelblue;
    // margin: 5px;
    .media-topic-vector-reduction-view{
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border: 1px solid steelblue;
    }
    .media-topic-difference-concat-view{
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 50%;
      right: 0%;
      border: 1px solid steelblue;
    }
  }
  .event-evolution{
    position: absolute;
    top: 35%;
    bottom: 0%;
    left: 0%;
    right: 0%;
    margin: 0px !important;

    .union-event-evolution{
      position: absolute;
      top: 0%;
      bottom: 30%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }

    .single-event-evolution{
      position: absolute;
      top: 70%;
      bottom: 0%;
      left: 0%;
      right: 0%;

      border: 1px solid steelblue;
    }
  }
}
</style>
