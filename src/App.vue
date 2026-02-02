<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface Solution {
  date: string;
  word: string;
}

const solutions = ref<Solution[]>([]);
const validWords = ref<string[]>([]);
const searchInput = ref('');
const isLoading = ref(true);

onMounted(async () => {
  try {
    const base = import.meta.env.BASE_URL;
    const [solRes, validRes] = await Promise.all([
      fetch(`${base}solutions.txt`),
      fetch(`${base}valid.txt`)
    ]);

    const solText = await solRes.text();
    const validText = await validRes.text();

    solutions.value = solText
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [date, word] = line.split(' ');
        return { date, word: word.toUpperCase() };
      });

    validWords.value = validText
      .split('\n')
      .filter(line => line.trim())
      .map(word => word.trim().toUpperCase());

  } catch (error) {
    console.error('Error loading data:', error);
  } finally {
    isLoading.value = false;
  }
});

const cleanInput = computed(() => searchInput.value.trim().toUpperCase().slice(0, 5));

const results = computed(() => {
  if (!cleanInput.value) return [];
  return solutions.value.filter(s => s.word.startsWith(cleanInput.value));
});

const exactMatchSolution = computed(() => {
  if (cleanInput.value.length !== 5) return null;
  return solutions.value.find(s => s.word === cleanInput.value);
});

const isPlayableWord = computed(() => {
  if (cleanInput.value.length !== 5) return true; // Don't show error while typing
  return validWords.value.includes(cleanInput.value) || !!exactMatchSolution.value;
});

const showNotPlayableError = computed(() => {
  return cleanInput.value.length === 5 && !isPlayableWord.value;
});

</script>

<template>
  <div class="min-h-screen bg-white dark:bg-zinc-950 text-zinc-900 dark:text-zinc-100 flex flex-col items-center pt-12 px-4 font-sans transition-colors duration-200">
    <div class="w-full max-w-[300px]">
      <h1 class="text-xl font-bold text-zinc-800 dark:text-zinc-100 text-center mb-2 uppercase font-clear-sans">Wordle Answers</h1>
      <p class="text-center text-zinc-500 mb-8 text-xs">Search the past Wordle solutions—updated daily through&nbsp;yesterday.</p>

      <div v-if="isLoading" class="text-center text-zinc-500 animate-pulse">
        Loading archive...
      </div>

      <div v-else class="space-y-6">
        <div class="relative">
          <input
            v-model="searchInput"
            type="text"
            maxlength="5"
            placeholder="Search"
            autofocus
            class="w-full px-4 pt-[7px] pb-[9px] bg-transparent border-2 border-zinc-200 dark:border-zinc-800 rounded-lg outline-none uppercase text-center text-xl tracking-widest transition-all font-clear-sans"
            :class="[
              showNotPlayableError 
                ? 'text-rose-600 dark:text-rose-400 bg-rose-50/30 dark:bg-rose-950/10' 
                : 'focus:border-zinc-500 dark:focus:border-zinc-400'
            ]"
          />
        </div>

        <div v-if="showNotPlayableError" class="text-rose-600 dark:text-rose-400 text-center font-medium font-sans normal-case">
          Not a playable word.
        </div>

        <div v-else-if="cleanInput && results.length === 0" class="text-zinc-500 text-center">
          No matches
        </div>

        <div v-else-if="cleanInput" class="overflow-y-auto max-h-[60vh]">
          <div 
            v-for="(result, index) in results" 
            :key="result.date"
            class="py-3 flex justify-between items-center"
            :class="{ 'border-b border-zinc-100 dark:border-zinc-900': index !== results.length - 1 }"
          >
            <span class="text-lg font-semibold tracking-wider font-clear-sans">{{ result.word }}</span>
            <span class="text-sm text-zinc-500 font-sans normal-case">{{ result.date }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Global styles for dark mode transition */
html {
  color-scheme: light dark;
}
</style>
