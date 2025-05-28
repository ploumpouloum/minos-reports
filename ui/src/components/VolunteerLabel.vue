<script setup lang="ts">
import type { Volunteer } from '@/types/main'
import { type PropType } from 'vue'

defineProps({
  volunteer: {
    type: Object as PropType<Volunteer>,
    required: true
  }
})
</script>

<template>
  {{ volunteer.lastname }} {{ volunteer.firstname }} ({{ volunteer.department
  }}<template v-if="volunteer.minor"> - M</template>)
</template>
