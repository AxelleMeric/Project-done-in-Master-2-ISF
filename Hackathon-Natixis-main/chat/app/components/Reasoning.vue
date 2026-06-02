<script setup lang="ts">
const { isStreaming } = defineProps<{
  text: string
  isStreaming?: boolean
}>()

const open = ref(false)

function cleanMarkdown(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, '$1') // Remove bold
    .replace(/\*(.+?)\*/g, '$1') // Remove italic
    .replace(/`(.+?)`/g, '$1') // Remove inline code
    .replace(/^#+\s+/gm, '') // Remove headers
}
</script>

<template>
  <UCollapsible v-model:open="open" class="flex flex-col gap-1 my-5">
    <UButton
      class="p-0 group mt-2"
      color="neutral"
      variant="link"
      trailing-icon="i-lucide-chevron-down"
      :ui="{
        trailingIcon: text.length > 0 ? 'group-data-[state=open]:rotate-180 transition-transform duration-200' : 'hidden'
      }"
    >
      <span
        :class="isStreaming
          ? 'relative inline-block overflow-hidden animate-shine italic bg-[linear-gradient(110deg,#bfbfbf,35%,#000,50%,#bfbfbf,75%,#bfbfbf)] dark:bg-[linear-gradient(110deg,#404040,35%,#fff,50%,#404040,75%,#404040)] bg-size-[200%_100%] bg-clip-text text-transparent'
          : ''"
      >
        {{ isStreaming ? '🧠 Thinking...' : 'Thoughts' }}
      </span>
    </UButton>

    <template #content>
      <div v-for="(value, index) in cleanMarkdown(text).split('\n').filter(Boolean)" :key="index">
        <span class="whitespace-pre-wrap text-sm italic text-muted font-normal">{{ value }}</span>
      </div>
    </template>
  </UCollapsible>
</template>
