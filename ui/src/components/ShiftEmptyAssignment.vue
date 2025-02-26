<script setup lang="ts">
const props = defineProps({
  role: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div>{{ props.role }}: <span>Manquant</span></div>
</template>

<style lang="css" scoped>
div {
  margin: 10px 0;
}
span {
  color: red;
}
</style>
