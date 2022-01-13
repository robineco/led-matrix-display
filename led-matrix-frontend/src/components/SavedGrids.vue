<template>
  <div class="saved-grid-wrapper">
    <b-field label="Saved Images"></b-field>
    <div
        class="image-list"
        v-if="data.images.length > 0"
    >
      <img
          v-for="(image, index) in data.images"
          :src="getImage(image)"
          :key="index"
          alt="image preview"
          @click="loadImage(index)"
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "SavedGrids",
  props: {
    data: {
      type: Object,
    },
  },
  methods: {
    getImage(encoded) {
      return `data:image/png;base64, ${encoded}`;
    },
    loadImage(index) {
      this.$emit('loadImage', index)
    }
  },
  watch: {
    data: {
      handler: function() {
        window.localStorage.setItem('matrix', JSON.stringify(this.data));
      },
      deep: true,
    }
  }
}
</script>

<style lang="scss" scoped>
.saved-grid-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 5rem 0 0 2rem;
  width: 10%;

  .image-list {
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    > img {
      flex-shrink: 0;
      width: 12vh;
      cursor: pointer;
    }
  }
}
</style>
