<template>
  <div>
    <v-list lines="three">
    <v-list-item-title class="ml-2 text-[36px]">Recommended Events</v-list-item-title>
    <v-list-item :prepend-avatar="event.image" v-for="(event, index) of recommendedData" :key="index">
      <div>
        <v-list-item-title>{{ event.title }} | <span class="text-grey">{{ new Date(event.start_time).toLocaleString() }} TO {{ new Date(event.end_time).toLocaleString() }}</span>
        </v-list-item-title>
        <v-list-item-subtitle>
          <p>{{ event.description }}</p>
          <br>
          <v-chip v-if="event.category_1" variant="outlined">{{ event.category_1 }}</v-chip>
          <v-chip class="ml-2" v-if="event.category_2" variant="outlined">{{ event.category_2 }}</v-chip>
          <v-chip class="ml-2" v-if="event.category_3" variant="outlined">{{ event.category_3 }}</v-chip>
          <br>
        </v-list-item-subtitle>
      </div>
    </v-list-item>
    <v-list-item-title class="ml-2 text-[36px]">Events We Think You'll Like!</v-list-item-title>
    <v-list-item :prepend-avatar="event.image" v-for="(event, index) of suggestionData" :key="index">
      <div>
        <v-list-item-title>{{ event.title }} | <span class="text-grey">{{ new Date(event.start_time).toLocaleString() }} TO {{ new Date(event.end_time).toLocaleString() }}</span>
        </v-list-item-title>
        <v-list-item-subtitle>
          <p>{{ event.description }}</p>
          <br>
          <v-chip v-if="event.category_1" variant="outlined">{{ event.category_1 }}</v-chip>
          <v-chip class="ml-2" v-if="event.category_2" variant="outlined">{{ event.category_2 }}</v-chip>
          <v-chip class="ml-2" v-if="event.category_3" variant="outlined">{{ event.category_3 }}</v-chip>
          <br>
        </v-list-item-subtitle>
      </div>
      </v-list-item>
    </v-list>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router'
const route = useRoute();
if (!route.query.tags) {
  router.push("/");
}

const recommendedData = ref([]);
const suggestionData = ref([]);


onMounted(async () => {
  let tags = "";
  let query = "";
  for (const tag of route.query.tags) {
    tags += `tags=${tag}&`;
    query += `query=${tag}&`;
  }

  const events = await fetch(`http://localhost:8000/recommendations/tags?${tags}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  }).then((res) => res.json());

  for (const event of events) {
    const eventRes = await fetch(`http://localhost:8000/event?eventId=${event.event_id}`);
    const eventData = await eventRes.json();
    recommendedData.value.push(eventData);
  }

  const suggestions = await fetch(`http://localhost:8000/recommendations/description?${query}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  }).then((res) => res.json());
  for (const event of suggestions) {
    const eventRes = await fetch(`http://localhost:8000/event?eventId=${event.event_id}`);
    const eventData = await eventRes.json();
    suggestionData.value.push(eventData);
  }
})


</script>

<style scoped>

</style>