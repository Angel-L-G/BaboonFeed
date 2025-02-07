<script setup lang="ts">
import type {User} from "@/types/User.ts";
//import type { File } from "@/types/File";

const props = defineProps<{
  "user": User,
}>();

</script>

<template>
  <div class="container">
    <div class="row">
      <div class="card bg-primary text-light" style="height: 13rem">
        <div class="row my-3">
          <div class="col-md-4">
            <img src="..." class="img-fluid rounded-start" alt="Profile Picture">
          </div>

          <div class="col-md-6">
            <div class="card-title">
              <h3 class="text-decoration-underline">Username: {{props.user.username}}</h3>
            </div>

            <div class="card-body">
              Bio: {{props.user.bio}}
            </div>

            <div class="display-flex justify-content-center">
              <span class="card-text m-2">
                <small class="text-body-light">
                  Followers: {{props.user.followers}}
                </small>
              </span>

              <span class="card-text">
                <small class="text-body-light">
                  Following: {{props.user.follows}}
                </small>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row my-3">
      <ul class="list-group">
        <li class="list-group-item">A Post</li>
        <li class="list-group-item">A second Post</li>
        <li class="list-group-item">A third Post</li>
        <li class="list-group-item">A fourth Post</li>
        <li class="list-group-item">And a fifth Post</li>
      </ul>
    </div>
  </div>
</template>
