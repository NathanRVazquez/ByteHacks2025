<template>
  <div>
    <!-- Content for recommendations will go here -->
      <v-list lines="three">
        <v-list-item-title class="ml-2 text-[36px]">Recommended Events</v-list-item-title>
        <v-list-item prepend-avatar="https://i.insider.com/602ee9ced3ad27001837f2ac?width=700" v-for="(event, index) in ['Event 1', 'Event 2', 'Event 3']" :key="index">
          <div>
            <v-list-item-title>{{ event }}</v-list-item-title>
            <v-list-item-subtitle><v-chip variant="outlined">ASS</v-chip></v-list-item-subtitle>
          </div>
        </v-list-item>
        <v-list-item-title class="ml-2 text-[36px]">Events We Think You'll Like!</v-list-item-title>
        <v-list-item prepend-avatar="https://i.insider.com/602ee9ced3ad27001837f2ac?width=700" v-for="(event, index) in ['Event 1', 'Event 2', 'Event 3']" :key="index">
          <div>
            <v-list-item-title>{{ event }}</v-list-item-title>
            <v-list-item-subtitle><v-chip variant="outlined">ASS</v-chip></v-list-item-subtitle>
          </div>
        </v-list-item>
      </v-list>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>

</style>