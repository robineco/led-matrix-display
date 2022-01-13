<template>
  <div id="app">
    <div class="wrapper">
      <ColorPicker
        :colors="colors"
        :currentColor="currentColor"
        @change="changeCurrentColor"
        @create="addColor"
      />
      <div>
        <Controls
          @export="exportImage"
          @save="saveFrame"
          @exportFrames="exportFrames"
          @saveImage="saveImage"
          @uploadImage="uploadImage"
          @brightness="changeBrightness"
        />
        <Grid
          :currentColor="currentColor"
          :grid="grid"
          @changeColor="changeColor"
        />
      </div>
      <SavedGrids
        :data="saved"
        @loadImage="loadImage"
      />
    </div>
    <ImageTimeLine
      :images="images"
      />
  </div>
</template>

<script>
import Grid from './components/Grid.vue'
import ColorPicker from '@/components/ColorPicker';
import Controls from "@/components/Controls";
import ImageTimeLine from "@/components/ImageTimeLine";
import SavedGrids from "@/components/SavedGrids";
import {createImage, uploadImage} from "@/api";
const axios = require('axios');

export default {
  name: 'App',
  components: {
    Grid,
    ColorPicker,
    Controls,
    ImageTimeLine,
    SavedGrids,
  },
  data: () => ({
    grid: [],
    x: 16,
    y : 16,
    colors: ['black', 'white', 'red', 'green', 'blue', 'yellow', 'darkorange'],
    currentColor: 'black',
    frames: [],
    images: [],
    saved: {
      grids: [],
      images: [],
    },
  }),
  created() {
    this.createGridStructure();
    this.loadSavedGrids();
  },
  methods: {
    createGridStructure() {
      for (let i = 0; i < this.x; i++) {
        this.grid.push([])
        for (let j = 0; j < this.y; j++) {
          this.grid[i][j] = ''
        }
      }
    },
    loadSavedGrids() {
      const saved = JSON.parse(window.localStorage.getItem('matrix'));
      if (saved != null) {
        const { images, grids } = saved;
        this.saved.images = images;
        this.saved.grids = grids;
      }
    },
    changeColor(position) {
      const { x, y, color } = position;
      if (color) {
        this.grid[x].splice(y, 1, '');
        return;
      }
      this.grid[x].splice(y, 1, this.currentColor);
    },
    changeCurrentColor(color) {
      this.currentColor = color;
    },
    addColor(newColor) {
      if (this.colors.includes(newColor)) {
        return;
      }
      this.colors.push(newColor)
    },
    loadImage(index) {
      this.grid = this.saved.grids[index]
    },
    async saveFrame() {
      const {image, frame} = await createImage(this.grid, false);
      this.images.push(image);
      this.frames.push(frame)
    },
    exportFrames() {
      const data = JSON.stringify(this.frames);
      console.log(data);
    },
    exportImage() {
      const headers = {
        'Content-Type': 'application/json',
      };
      const data = {
        matrix: this.grid,
      }
      axios.post('http://192.168.178.62:5000/matrix', data, {
        headers,
      }).then((response) => {
        console.log(response);
      });
    },
    async saveImage() {
      const {image, frame} = await createImage(this.grid, true);
      this.saved.grids.push(frame);
      this.saved.images.push(image);
    },
    async uploadImage(image) {
      const { success } = await uploadImage(image);
      if (!success) {
        this.danger();
      }
    },
    danger() {
      this.$buefy.toast.open({
        duration: 5000,
        message: 'Sorry something went wrong. Please tyr another image',
        position: 'is-bottom',
        type: 'is-danger'
      })
    },
    changeBrightness(brightness) {
      const headers = {
        'Content-Type': 'application/json',
      };
      const data = {
        brightness: brightness,
      }
      axios.post('http://192.168.178.62:5000/brightness', data, {
        headers,
      }).then((response) => {
        console.log(response);
      });
    },
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background-color: #f5f8f8;
  > h1 {
    margin-top: 2%;
    font-size: xx-large;
  }
}
.wrapper {
  height: 100%;
  width: 100%;
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}
</style>
