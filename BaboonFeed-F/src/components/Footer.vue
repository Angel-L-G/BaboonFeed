<template>
  <footer class="bd-footer py-4 py-md-5 mt-5 bg-dark">
    <div class="container py-4 py-md-5 px-4 px-md-3 text-body-secondary">
      <div class="row text-light">
        <div class="col-lg-4 mb-3">
          <h5>Links</h5>
          <ul class="list-group list-group-flush ">
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'youtube']" class="link-danger" />
              Youtube
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'instagram']" style="color: pink;" />
              Instagram
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'github']" />
              Github
            </li>
          </ul>
        </div>
        <div class="col-lg-4 mb-3">
          <h5>Creators</h5>
          <ul class="list-group list-group-flush">
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fas', 'user']" class="link-danger" />
              Owen
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fas', 'user']" class="link-primary" />
              Moises
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fas', 'user']" class="link-warning" />
              Angel
            </li>
          </ul>
        </div>
        <div class="col-lg-4 mb-3">
          <h5>Documentation</h5>
          <ul class="list-group list-group-flush">
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'vuejs']" class="link-success" />
              Vue
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'python']" class="link-warning" />
              Django
            </li>
            <li class="text-light list-group-item bg-dark">
              <font-awesome-icon :icon="['fab', 'bootstrap']" style="color: blueviolet;" />
              Bootstrap
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>
