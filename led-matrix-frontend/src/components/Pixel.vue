<template>
  <div
    class="pixel"
    :style="{backgroundColor: getDefaultColor}"
    @click.left="handleClick"
    @mouseover.left="handleOver"
    @mouseleave.left="handleOver"
    @click.right="restoreDefaultColor"
  >
  </div>
</template>

<script>
  export default {
    name: 'Pixel',
    props: {
      x: {
        type: Number,
        required: true
      },
      y: {
        type: Number,
        required: true
      },
      color: {
        type: String,
      },
      mouseDown: {
        type: Boolean,
      }
    },
    data: () => ({
      //
    }),
    methods: {
      handleClick() {
        const position = {
          x: this.x,
          y: this.y,
        }
        this.$emit('changeColor', position);
      },
      handleOver() {
        if (this.mouseDown) {
          this.handleClick();
        }
      },
      debugLog() {
        console.log(`${this.x} | ${this.y}`);
      },
      restoreDefaultColor() {
        const position = {
          x: this.x,
          y: this.y,
        }
        if (this.x % 2 === 0 && this.y % 2 === 0 || this.x % 2 === 1 && this.y % 2 === 1) {
          this.$emit('changeColor', {
            ...position,
            color: '#757575',
          });
        } else {
          this.$emit('changeColor', {
            ...position,
            color: '#ffffff',
          });
        }
      },
    },
    computed: {
      getDefaultColor() {
        if (this.color && this.color !== '') {
          return this.color;
        }
        if (this.x % 2 === 0 && this.y % 2 === 0 || this.x % 2 === 1 && this.y % 2 === 1) {
          return 'grey'
        }
        return '#f2f0f5'
      }
    }
  }
</script>

<style lang="scss" scoped>
.pixel {
  width: 4vh;
  height: 4vh;
  cursor: pointer;
}
</style>
