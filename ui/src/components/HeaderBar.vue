<script setup lang="ts">
import logoImage from '@/assets/logo.jpg'
import { useMainStore } from '@/stores/main'
import { useRoute } from 'vue-router'

const main = useMainStore()

const route = useRoute()
main.fetchData()
</script>

<template>
  <div class="header-bar">
    <div id="whoami">{{ main.whoami }}</div>
    <div id="logo">
      <router-link to="/">
        <v-img id="logo" :src="logoImage" alt="Logo" class="logo" height="70" />
      </router-link>
    </div>
    <div id="title">Maxi-Race 2025</div>
    <template v-if="main.isSupervisor">
      <div class="header-btns">
        <router-link to="/restrictions" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/restrictions' }" @click="navigate"
            >Restrictions</v-btn
          >
        </router-link>
        <router-link to="/freebuzy" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/freebuzy' }" @click="navigate"
            >Disponibilités</v-btn
          >
        </router-link>
        <router-link to="/vacations" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/vacations' }" @click="navigate">Vacations</v-btn>
        </router-link>
        <router-link to="/manques" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/manques' }" @click="navigate">Manques</v-btn>
        </router-link>
        <router-link to="/volunteers" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/volunteers' }" @click="navigate"
            >Volontaires</v-btn
          >
        </router-link>
        <router-link to="/data" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/data' }" @click="navigate"
            >Gérer les données</v-btn
          >
        </router-link>
        <router-link to="/volunteers-dlus" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/volunteers-dlus' }" @click="navigate"
            >Vue DLUS</v-btn
          >
        </router-link>
        <router-link to="/missions" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/missions' }" @click="navigate"
            >Vue Volontaire</v-btn
          >
        </router-link>
      </div>
    </template>
    <template v-if="main.isDlus">
      <div class="header-btns">
        <router-link to="/volunteers-dlus" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/volunteers-dlus' }" @click="navigate"
            >Vue DLUS</v-btn
          >
        </router-link>
        <router-link to="/missions" custom v-slot="{ navigate }">
          <v-btn :class="{ active: route.path == '/missions' }" @click="navigate"
            >Vue Volontaire</v-btn
          >
        </router-link>
      </div>
    </template>
  </div>
</template>

<style scoped>
#whoami {
  position: absolute;
  top: 10px;
  right: 10px;
}
#title {
  position: absolute;
  top: 10px;
  left: 10px;
}
.header-bar {
  padding: 0.25rem;
  display: flex;
  flex-direction: column;
}

.header-btns {
  padding: 0.25rem;
  display: flex;
  flex-direction: row;
  margin: auto;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.v-btn.active {
  background-color: #676767;
  color: white;
}

#logo {
  flex-grow: 1;
}

a:after {
  content: none;
}

img#online {
  height: 20px;
  padding-right: 10px;
}

@media print {
  .header-bar {
    display: none;
  }
}
</style>
