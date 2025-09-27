<template>
  <div class="ma-4">
    <div class="mb-4 flex w-full justify-between">
      <div class="flex gap-[10px]">
        <router-link
          v-for="page in leftPages"
          :key="page.path"
          :to="page.path"
          class="p-4"
        >
          <v-btn color="primary">{{ page.title }}
            <template #prepend>
              <font-awesome-icon :icon="['fa', page.icon]" class="mr-2" />
            </template>
          </v-btn>
        </router-link>
      </div>
      <div class="flex gap-[10px] justify-end flex-row-reverse">
        <router-link
          v-for="page in rightPages"
          :key="page.path"
          :to="page.path"
          class="p-4"
        >
          <v-btn color="primary">{{ page.title }}
            <template #prepend>
              <font-awesome-icon :icon="['fa', page.icon]" class="mr-2" />
            </template>
          </v-btn>
        </router-link>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
const leftPages = [
  { title: "Home", path: "/", icon: "fa-house" },
  { title: "Form", path: "/form", icon: "fa-file" },
  { title: "Recommendations", path: "/recommendations", icon: "fa-thumbs-up" },
  { title: "My Schedule", path: "/schedule", icon: "fa-calendar-days" },
  { title: "Profile", path: "/profile", icon: "fa-user" },
]
const rightPages = [
  { title: "SignUp", path: "/signup", icon: "fa-house" },
] 
</script>

<style scoped>
@import "tailwindcss";

</style>