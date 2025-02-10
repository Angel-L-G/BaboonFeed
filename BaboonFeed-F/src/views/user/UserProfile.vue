<script setup lang="ts">
import type {User} from "@/types/User.ts";
import { onMounted, ref } from "vue";
import { API_URL } from "@/globals";
import { useRouter } from "vue-router";

const router = useRouter()
const username = router.currentRoute.value.params.username
const user = ref<User>({} as User)

onMounted(async () => {
  await fetch(`${API_URL}users/${username}`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
  })
  .then(async (response) => {
    user.value = await response.json() 
    console.log(user.value)
  })
  .catch(error => {
    console.log(error)
  })
})

</script>

<template>
  <div class="container">
    <div class="row">
      <div class="card bg-primary text-light" style="height: 13rem">
        <div class="row my-3">
          <div class="col-md-4">
            <img :src="user.file?.name" class="img-fluid rounded-start w-50" alt="Profile Picture">
          </div>

          <div class="col-md-6">
            <div class="card-title">
              <h3 class="text-decoration-underline">Username: {{user.username}}</h3>
            </div>

            <div class="card-body">
              Bio: {{user.bio}}
            </div>

            <div class="display-flex justify-content-center">
              <span class="card-text m-2">
                <small class="text-body-light">
                  Followers: {{user.followers}}
                </small>
              </span>

              <span class="card-text">
                <small class="text-body-light">
                  Following: {{user.follows}}
                </small>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
