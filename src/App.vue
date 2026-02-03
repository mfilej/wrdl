<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface Solution {
  date: string;
  word: string;
}

const solutions = ref<Solution[]>([]);
const era1Solutions = ref<Solution[]>([]);
const showEra1 = ref(false);
const showNotice = ref(false);
const validWords = ref<string[]>([]);
const searchInput = ref('');
const isLoading = ref(true);

onMounted(async () => {
  try {
    const base = import.meta.env.BASE_URL;
    const [solRes, era1Res, validRes] = await Promise.all([
      fetch(`${base}solutions.txt`),
      fetch(`${base}solutions-era1.txt`),
      fetch(`${base}valid.txt`)
    ]);

    const solText = await solRes.text();
    const era1Text = await era1Res.text();
    const validText = await validRes.text();

    solutions.value = solText
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [date, word] = line.split(' ');
        return { date, word: word.toUpperCase() };
      });

    era1Solutions.value = era1Text
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

const activeSolutions = computed(() => showEra1.value ? era1Solutions.value : solutions.value);

const results = computed(() => {
  if (!cleanInput.value) return [];
  return activeSolutions.value.filter(s => s.word.startsWith(cleanInput.value));
});

const exactMatchSolution = computed(() => {
  if (cleanInput.value.length !== 5) return null;
  return activeSolutions.value.find(s => s.word === cleanInput.value);
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
    <div class="w-full max-w-[300px] flex flex-col gap-6">
      <heading class="flex flex-col gap-2 text-center">
        <h1 class="text-xl font-bold text-zinc-800 dark:text-zinc-100 uppercase font-clear-sans">Wordle Answers</h1>
        <p class="text-zinc-500 text-xs">Search the past Wordle solutions—updated daily through&nbsp;yesterday.</p>
      </heading>

      <div class="mb-1 p-3 bg-zinc-50 dark:bg-zinc-900/50 rounded-lg border border-zinc-100 dark:border-zinc-800 min-h-[70px] flex flex-col justify-center relative">
        <button 
          @click="showNotice = !showNotice"
          class="absolute top-2 right-2 p-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 transition-colors z-10"
          :title="showNotice ? 'Close notice' : 'Why are there two sets?'"
        >
          <svg v-if="showNotice" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          <svg v-else class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        </button>

        <div 
          class="absolute inset-x-3 text-[10px] leading-relaxed text-zinc-600 dark:text-zinc-400 pr-6 transition-opacity duration-300"
          :class="showNotice ? 'opacity-100' : 'opacity-0 pointer-events-none'"
        >
          <p class="text-center">
            Wordle has started reusing past solutions as of February 1st, 2026.
            <a href="https://www.tomsguide.com/gaming/wordle-just-confirmed-major-change-for-next-week-and-its-controversial" 
               target="_blank" 
               class="text-blue-500 hover:underline inline-flex items-center gap-0.5 font-medium"
            >Read more <svg class="w-2.5 h-2.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg></a>
          </p>
        </div>

        <div 
          class="flex flex-col gap-2 transition-opacity duration-300"
          :class="!showNotice ? 'opacity-100' : 'opacity-0 pointer-events-none'"
        >
          <div class="flex justify-center">
            <span class="text-zinc-500 text-xs uppercase font-semibold">Solution Set</span>
          </div>
          
          <div class="flex bg-zinc-100 dark:bg-zinc-800 p-0.5 rounded-md">
            <button 
              @click="showEra1 = true"
              class="flex-1 py-1 text-[10px] rounded-sm transition-all duration-200"
              :class="showEra1 ? 'bg-white dark:bg-zinc-700 shadow-sm text-zinc-900 dark:text-zinc-100 font-medium' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700'"
            >
              Jun '21–Jan '26
            </button>
            <button 
              @click="showEra1 = false"
              class="flex-1 py-1 text-[10px] rounded-sm transition-all duration-200"
              :class="!showEra1 ? 'bg-white dark:bg-zinc-700 shadow-sm text-zinc-900 dark:text-zinc-100 font-medium' : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-700'"
            >
              Feb '26–
            </button>
          </div>
        </div>
      </div>

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

        <div v-else-if="cleanInput" class="overflow-y-auto max-h-[60vh] flex flex-col divide-y divide-zinc-100 dark:divide-zinc-900">
          <div 
            v-for="(result, index) in results" 
            :key="result.date"
            class="flex justify-between items-center py-1"
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
