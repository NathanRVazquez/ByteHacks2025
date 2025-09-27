<template>
	<div class="flex items-center justify-center min-h-screen">
		<div
			class="flex w-[80vw] h-[80vh] rounded-2xl shadow-xl overflow-hidden rounded-lg"
		>
			<div class="flex w-[40%] items-center justify-center p-10 bg-white">
				<div class="w-full max-w-sm px-12">
					<h1 class="text-3xl font-bold mb-2">Sign up</h1>
					<p class="text-sm text-gray-500 mb-8">
						Explore a world with countless possibilities
					</p>
					<v-btn
						block
						variant="outlined"
						color="grey-darken"
						class="mb-4 text-none"
					>
						<template v-slot:prepend>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								width="16"
								height="16"
								fill="currentColor"
								class="bi bi-google"
								viewBox="0 0 16 16"
							>
								<path
									d="M15.545 6.558a9.4 9.4 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.7 7.7 0 0 1 5.352 2.082l-2.284 2.284A4.35 4.35 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.8 4.8 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.7 3.7 0 0 0 1.599-2.431H8v-3.08z"
								/>
							</svg>
						</template>
						Sign up with Google
					</v-btn>
					<div class="flex items-center mb-4">
						<div class="flex-grow border-t border-gray-300"></div>
						<span class="px-3 text-xs text-gray-200"
							>or sign up using email</span
						>
						<div class="flex-grow border-t border-gray-300"></div>
					</div>

					<v-text-field
						v-model="form.email"
						label="Email"
						type="email"
						density="comfortable"
						variant="outlined"
						class="mb-2"
					></v-text-field>

					<v-text-field
						v-model="form.password"
						label="Password"
						type="password"
						density="comfortable"
						variant="outlined"
						class="mb-2"
					></v-text-field>

					<v-text-field
						v-model="form.confirmPassword"
						label="Confirm Password"
						type="password"
						density="comfortable"
						variant="outlined"
						class="mb-6"
					></v-text-field>

					<v-btn block color="primary" class="mb-4" @click="onSubmit">
						Continue &#8594;
					</v-btn>

					<p class="text-xs text-gray-500 text-center">
						Already have an account?
						<router-link
							to="/signin"
							class="text-primary font-medium"
						>
							Sign in
						</router-link>
					</p>
				</div>
			</div>

			<div
				class="w-[60%] md:flex items-center justify-center bg-cover bg-center"
				style="background-image: url('/central-park.webp')"
			></div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const form = reactive({
	email: "",
	password: "",
	confirmPassword: "",
});

const onSubmit = () => {
	if (!form.email || !form.password || !form.confirmPassword) {
		alert("Please fill all fields");
		return;
	}
	if (form.password !== form.confirmPassword) {
		alert("Passwords do not match");
		return;
	}
};
</script>
