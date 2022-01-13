<template>
<div class="timeline-wrapper">
  <div
      class="image-list"
      v-if="images.length > 0"
  >
    <img
      v-for="(image, index) in images"
      :src="getImage(image)"
      :key="index"
      alt="image preview"
    >
  </div>
</div>
</template>

<script>
export default {
  name: "ImageTimeLine",
  props: {
    images: {
      type: Array,
    },
  },
  methods: {
    getImage(encoded) {
      return `data:image/png;base64, ${encoded}`;
    }
  }
}
</script>

<style lang="scss" scoped>
.timeline-wrapper {
  width: 70%;
  margin-top: 2rem;
}
.image-list {
  overflow: auto;
  display: flex;
  gap: 3rem;
  > img {
    flex-shrink: 0;
    width: 12vh;
  }
}
</style>
