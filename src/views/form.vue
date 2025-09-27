<template>
  <div>
    <v-card variant="outlined" class="mx-auto h-full" max-width="1000" >
      <template #title>
        Questionnaire
      </template>
      <v-window v-model="step">
        <v-item-group multiple v-model="selected">
        <v-window-item :value="0">
          <v-card-text>
            <div class="grid grid-cols-3 gap-[10px] text-center">
              <v-item v-for="(item, index) in items1" :key="index" >
                <template #default="{ isSelected, toggle }">
                  <v-card
                    :elevation="isSelected ? 12 : 2"
                    :color="isSelected ? 'primary' : 'white'"
                    class="pa-4 "
                    @click="toggle"
                  >
                    <v-img :src="item.image" height="200" cover></v-img>
                    <v-card-text class="h-full text-[28px]">
                      <p :class="[isSelected ? 'text-white' : 'text-black', 'font-extrabold text-shadow-title']">
                        {{ item.title }}
                      </p>
                    </v-card-text>
                  </v-card>
                </template>
              </v-item>
            </div>
          </v-card-text>
        </v-window-item>
        <v-window-item :value="1">
          <v-card-text>
            <div class="grid grid-cols-3 gap-[10px] text-center">
              <v-item v-for="(item, index) in items2" :key="index">
                <template #default="{ isSelected, toggle }">
                  <v-card
                    :elevation="isSelected ? 12 : 2"
                    :color="isSelected ? 'primary' : 'white'"
                    class="pa-4 "
                    @click="toggle"
                  >
                    <v-img :src="item.image" height="200" cover></v-img>
                    <v-card-text class="h-full text-[28px]">
                      <p :class="[isSelected ? 'text-white' : 'text-black', 'font-extrabold text-shadow-title']">
                        {{ item.title }}
                      </p>
                    </v-card-text>
                  </v-card>
                </template>
              </v-item>
            </div>
          </v-card-text>
        </v-window-item>
        </v-item-group>
      </v-window>
      <v-card-actions>
        <v-btn
          :disabled="step === 0"
          @click="step--"
        >
          Previous
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          :disabled="step === 1 && selected.length === 0"
          @click="nextStep"
        >
          {{ step === 1 ? 'Submit' : 'Next' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Business from "@/assets/images/business.jpg";
import ComedyAndPerformance from "@/assets/images/comedy_and_performance.jpg";
import CommunityAndCulture from "@/assets/images/community_and_culture.jpg";
import HealthAndFitness from "@/assets/images/health_and_fitness.jpg";
import FoodAndDrink from "@/assets/images/food_and_drink.jpg";
import NightlifeAndParties from "@/assets/images/nightlife_and_parties.jpg";
import STEM from "@/assets/images/stem.jpg";
import HomeAndLifestyle from "@/assets/images/home_and_lifestyle.jpg";
import CharityAndSocialCauses from "@/assets/images/charity_and_social_causes.jpg";
import Music from "@/assets/images/music.jpg";
import Education from "@/assets/images/education.jpg";
import Dating from "@/assets/images/dating.jpg";
import router from '@/router';

enum Category {
  ComedyAndPerformance = 0,
  CommunityAndCulture = 1,
  HealthAndFitness = 2,
  FoodAndDrink = 3,
  NightlifeAndParties = 4,
  STEM = 5,
  HomeAndLifestyle = 6,
  CharityAndSocialCauses = 7,
  Business = 8,
  Music = 9,
  Education = 10,
  Dating = 11
}

const step = ref(0);
const items1 = [
  {
    "title": "Comedy & Performance",
    "image": ComedyAndPerformance
  },
  {
    "title": "Community & Culture",
    "image": CommunityAndCulture
  },
  {
    "title": "Health & Fitness",
    "image": HealthAndFitness
  },
  {
    "title": "Food & Drink",
    "image": FoodAndDrink
  },
  {
    "title": "Nightlife & Parties",
    "image": NightlifeAndParties
  },
  {
    "title": "STEM",
    "image": STEM
  },
]
const items2 = [
  {
    "title": "Home & Lifestyle",
    "image": HomeAndLifestyle
  },
  {
    "title": "Charity & Social Causes",
    "image": CharityAndSocialCauses
  },
  {
    "title": "Business",
    "image": Business
  },
  {
    "title": "Music",
    "image": Music
  },
  {
    "title": "Education",
    "image": Education
  },
  {
    "title": "Dating",
    "image": Dating
  }
]

const selected = ref<number[]>([]);

function nextStep() {
  if (step.value < 1) {
    step.value++;
    return;
  }
  router.push({ name: 'Recommendations', query: { tags: selected.value.map(i => Category[i]) } });
}

</script>

<style scoped>


.text-shadow-title {
  text-shadow:
    0 4px 8px rgba(0,0,0,0.45),
    0 1px 0 rgba(0,0,0,0.7),
    1px 1px 2px rgba(0,0,0,0.35);
}
</style>