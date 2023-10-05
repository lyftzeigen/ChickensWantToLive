<template>
  <title>
    Система мониторинга уровня стреса птицы и прогнозирования продукции
  </title>

  <div class="prose max-w-none my-10">
    <h1>
      🐔 Система мониторинга уровня стреса птицы и прогнозирования продукции
    </h1>

    <h2 class="my-5">Видео</h2>
    <div class="flex flex-row">
      <div v-for="date in folders" class="btn btn-primary btn-sm m-1">
        📁 {{ date }}
      </div>
    </div>

    <h2 class="my-5">Данные</h2>
    <div class="grid grid-cols-2">
      <NuxtImg
        v-for="date in folders"
        :src="'/' + date + '/activity.jpg'"
        class="m-0"
      />
    </div>

    <h2 class="my-5">Прогноз</h2>
    <NuxtImg src="/forecast/forecast.png" />
  </div>
</template>

<script setup lang="ts">
// Папки с видео
const folders = ref([
  "30.07.2023",
  "31.07.2023",
  "01.08.2023",
  "02.08.2023",
  "03.08.2023",
]);
</script>
