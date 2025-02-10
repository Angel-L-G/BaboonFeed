<script setup lang="ts">
/*
No esta acabado
 */
import type {User} from "@/types/User.ts";

const user: User = {
    "id": 1,
    "email": "user1@example.com",
    "username": "user1",
    "created_at": "2024-01-01T12:00:00Z",
    "bio": "Hola, soy user1!",
    "file": {
    "id": 1,
        "name": "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        "type": "image"
},
    "followers": 10,
    "follows": 5
};
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
