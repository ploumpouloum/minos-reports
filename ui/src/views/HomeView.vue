<script setup lang="ts">
import { useMainStore } from '@/stores/main'
import { useRouter } from 'vue-router'

const router = useRouter()

const main = useMainStore()

main.fetchData().then(() => {
  if (main.isSupervisor) {
    router.push({
      name: 'restrictions'
    })
  } else if (main.isDlus) {
    router.push({
      name: 'volunteers-dlus'
    })
  } else {
    router.push({
      name: 'missions'
    })
  }
})
</script>
