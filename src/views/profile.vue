<template>
	<div class="flex items-center justify-center min-h-screen">
		<div
			class="flex w-[80vw] h-[80vh] rounded-2xl shadow-xl overflow-hidden rounded-lg"
		>
			<div class="flex w-[60%] items-center justify-center p-10 bg-white">
				<div class="w-full max-w-sm px-12">
					<h1 class="text-3xl font-bold mb-2">Profile</h1>
					<p class="text-sm text-gray-500 mb-8">
						Manage your profile and update your lifestyles
					</p>
					<h2 class="text-lg font-semibold mb-2">Lifestyles</h2>
					<div
						class="flex flex-wrap content-start gap-3 mb-4 max-h-[40%] overflow-y-auto pr-2 border rounded-md p-2"
					>
						<v-chip
							v-for="(lifestyle, index) in lifestyles"
							:key="lifestyle"
							color="primary"
							class="text-white items-center gap-2"
						>
							<font-awesome-icon
								:icon="['fas', 'times']"
								class="cursor-pointer"
								@click.stop="removeLifestyle(index)"
							/>
							<span>{{ lifestyle }}</span>
						</v-chip>
					</div>
					<v-text-field
						v-model="newLifestyle"
						label="Add a lifestyle"
						variant="outlined"
						density="comfortable"
						class="mb-4"
						@keyup.enter="addLifestyle"
					>
						<template v-slot:append>
							<v-btn
								color="primary"
								variant="flat"
								size="small"
								icon
								class="rounded-full"
								@click="addLifestyle"
							>
								<font-awesome-icon :icon="['fas', 'plus']" />
							</v-btn>
						</template>
					</v-text-field>
				</div>
			</div>
			<div
				class="w-[40%] md:flex items-center justify-center bg-cover bg-center"
				style="background-image: url('/eiffel-tower.jpg')"
			></div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const lifestyles = ref<string[]>([]);
const newLifestyle = ref("");

function addLifestyle() {
	const lifestyle = newLifestyle.value.trim();
	if (lifestyle && !lifestyles.value.includes(lifestyle)) {
		lifestyles.value.push(lifestyle);
	}
	newLifestyle.value = "";
}

function removeLifestyle(index: number) {
	lifestyles.value.splice(index, 1);
}
</script>
