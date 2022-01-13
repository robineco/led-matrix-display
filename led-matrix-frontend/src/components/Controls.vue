<template>
  <div class="control-wrapper">
    <div class="controls__buttons">
      <b-button
          type="is-primary"
          @click="saveFrame"
      >
        Save as frame
      </b-button>
      <b-button
          type="is-primary"
          @click="exportFrames"
      >
        Export all frames
      </b-button>
      <b-button
          type="is-primary"
          @click="exportImage"
      >
        Update Image
      </b-button>
      <b-button
          type="is-primary"
          @click="saveImage"
      >
        Save Image
      </b-button>
    </div>
    <div class="controls__image">
      <b-field class="file is-primary" :class="{'has-name': !!file}">
        <b-upload v-model="file" class="file-label" @input="uploadedImage">
            <span class="file-cta">
                <b-icon class="file-icon" icon="upload"></b-icon>
                <span class="file-label">Upload Image</span>
            </span>
          <span class="file-name" v-if="file">
                {{ file.name }}
            </span>
        </b-upload>
      </b-field>
    </div>
    <div class="controls__leds">
      <section>
        <b-field label="Brightness">
          <b-slider :min="1" :max="100" v-model="brightness"></b-slider>
          <b-button
              id="slider-btn"
              type="is-primary is-light"
              @click="changeBrightness"
          >
            Update
          </b-button>
        </b-field>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Controls",
  data: () => ({
    brightness: 20,
    file: null,
  }),
  methods: {
    exportImage() {
      this.$emit('export');
    },
    saveFrame() {
      this.$emit('save');
    },
    exportFrames() {
      this.$emit('exportFrames')
    },
    saveImage() {
      this.$emit('saveImage')
    },
    changeBrightness() {
      this.$emit('brightness', this.brightness);
    },
    uploadedImage() {
      this.$emit('uploadImage', this.file)
    }
  }
}
</script>

<style lang="scss" scoped>
.control-wrapper {
  display: flex;
  margin: 1rem;
  gap: 1rem;
  flex-direction: column;

  .controls__buttons {
    display: flex;
    gap: 1rem;
  }

  .controls__leds {
    section {
      max-width: 50%;
    }
    #slider-btn {
      margin-left: 1rem;
    }
  }
}
</style>
