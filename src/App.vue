<template>
  <div class="ma-4">
    <div class="mb-4 flex w-full justify-between">
      <div class="flex gap-[10px]">
        <div v-for="page in leftPages" :key="page.path">
          <router-link
            :to="page.path"
            class="p-4"
            v-if="page.auth ? userStore.isAuthenticated : true"
          >
            <v-btn color="primary">{{ page.title }}
              <template #prepend>
                <font-awesome-icon :icon="['fa', page.icon]" class="mr-2" />
              </template>
            </v-btn>
          </router-link>
        </div>

      </div>
      <div class="flex gap-[10px] justify-end flex-row-reverse">
        <router-link v-if="!userStore.isAuthenticated"
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
        <div v-else class="p-4">
          <v-btn color="primary" @click="logout">Logout
            <template #prepend>
              <font-awesome-icon :icon="['fa', 'fa-right-from-bracket']" class="mr-2" />
            </template>
          </v-btn>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();


const leftPages = [
  { title: "Home", path: "/", icon: "fa-house" },
  { title: "Form", path: "/form", icon: "fa-file", auth: true },
  // { title: "My Schedule", path: "/schedule", icon: "fa-calendar-days", auth: true },
  // { title: "Profile", path: "/profile", icon: "fa-user", auth: true },
]
const rightPages = [
  { title: "SignUp", path: "/signup", icon: "fa-house" },
] 

function logout() {
  userStore.setUser(null);
}
</script>

<style scoped>
@import "tailwindcss";

</style>