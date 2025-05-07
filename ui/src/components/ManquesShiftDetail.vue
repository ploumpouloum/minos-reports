<script setup lang="ts">
defineProps({
  total: {
    type: Number,
    required: true
  },
  manque: {
    type: Number,
    required: true
  },
  showTotal: {
    // show total amount expected
    type: Boolean
  },
  showDone: {
    // show amounts when there is no manque
    type: Boolean
  }
})
</script>

<template>
  <span v-if="manque" class="todo"
    >{{ manque }}<template v-if="showTotal"> / {{ total }}</template></span
  >
  <span v-else-if="total && showDone" class="done"
    >0<template v-if="showTotal"> / {{ total }}</template></span
  >
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
