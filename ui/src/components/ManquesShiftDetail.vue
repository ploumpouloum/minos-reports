<script setup lang="ts">
defineProps({
  total: {
    type: Number,
    required: true
  },
  manque: {
    type: Number,
    required: true
  }
})
</script>

<template>
  <span v-if="manque" class="todo">{{ manque }} / {{ total }}</span>
  <span v-else-if="total" class="done">0 / {{ total }}</span>
  <span v-else>&nbsp;</span>
</template>

<style scoped lang="css">
.todo {
  color: red;
}

.done {
  color: green;
}
</style>
