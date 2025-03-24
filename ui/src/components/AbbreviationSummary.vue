<script setup lang="ts">
import { stationsRolesMaps } from '@/constants'
</script>
<template>
  <div id="role-map">
    <h4>Abbrévations :</h4>
    <div v-for="(key, value) in stationsRolesMaps" :key="key">{{ key }} : {{ value }}</div>
  </div>
</template>

<style scoped>
input {
  margin-right: 6px;
  margin-bottom: 12px;
}
.report {
  margin-left: 30px;
  margin-right: 30px;
}

.day {
  background-color: #e40613;
  color: white;
  text-align: center;
  margin-bottom: 10px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

table {
  margin-bottom: 10px;
  width: 100%;
  border-collapse: collapse;
}

th.noborder {
  border: none;
  background-color: transparent;
  width: auto;
  color: black;
  text-align: right;
  padding: 0 1rem;
}

#role-map {
  padding: 0 3rem;
  font-size: small;
  display: flex;
  flex-wrap: wrap;
}

#role-map div {
  padding: 0 1rem;
  margin: 0.1rem;
  border: #717171 1px solid;
  border-radius: 2px;
}

#role-map h4 {
  margin: 0.1rem;
}
</style>
