<template>
  <div class="grid-wrapper">
    <div class="grid_x" @mousedown.left="handleDown" @mouseup="handleUp" @mouseleave="handleUp" @contextmenu.p.prevent>
      <div class="grid_row" v-for="(row, rowKey) in grid" :key="rowKey">
        <div class="grid_col" v-for="(col, colKey) in row" :key="colKey">
          <Pixel
            :x="colKey"
            :y="rowKey"
            :color="grid[colKey][rowKey]"
            :mouseDown="mouseDown"
            @changeColor="changeColor"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Pixel from "./Pixel.vue";

  export default {
    name: 'Grid',
    components: {
      Pixel,
    },
    props: {
      currentColor: {
        type: String,
        required: true,
      },
      grid: {
        type: Array,
        required: true,
      },
    },
    data: () => ({
      mouseDown: false,
    }),
    methods: {
      changeColor(position) {
        this.$emit('changeColor', position);
      },
      handleDown() {
        this.mouseDown = true;
      },
      handleUp() {
        this.mouseDown = false;
      },
    },
  }
</script>

<style lang="scss" scoped>
.grid-wrapper {
  padding: 1rem;
  border: 3px solid darkorange;
  display: flex;
  justify-content: center;
  .grid_x {
    display: flex;
    flex-direction: row;
  }
}
</style>
