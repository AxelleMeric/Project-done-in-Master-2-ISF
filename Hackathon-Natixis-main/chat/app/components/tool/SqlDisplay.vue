<script setup lang="ts">
defineProps<{
  invocation: SQLUIToolInvocation
  isStreaming?: boolean
}>()

const open = ref(false)
</script>

<template>
  <div class="my-5">
    <UCollapsible v-model:open="open" class="flex flex-col gap-1">
      <UButton
        class="p-0 group w-fit"
        color="neutral"
        variant="link"
        :trailing-icon="invocation.state === 'input-streaming' ? 'i-lucide-loader-2 animate-spin' : 'i-lucide-chevron-down'"
        :ui="{
          trailingIcon: invocation.state !== 'input-streaming' ? 'group-data-[state=open]:rotate-180 transition-transform duration-200' : ''
        }"
      >
        <span
          :class="isStreaming
            ? 'relative inline-block overflow-hidden animate-shine italic bg-[linear-gradient(110deg,#bfbfbf,35%,#000,50%,#bfbfbf,75%,#bfbfbf)] dark:bg-[linear-gradient(110deg,#404040,35%,#fff,50%,#404040,75%,#404040)] bg-size-[200%_100%] bg-clip-text text-transparent'
            : ''"
        >
          {{ isStreaming ? '⚡ Executing SQL query...' : 'SQL Query executed' }}
        </span>
      </UButton>

      <template #content>
        <div v-if="invocation.input" class="mt-2 rounded-xl bg-gray-50 dark:bg-gray-900/80 border border-gray-200 dark:border-gray-800 overflow-hidden shadow-sm">
          <div class="p-4 bg-gray-100/50 dark:bg-gray-950/50">
            <div class="flex items-center gap-2 mb-2">
              <UIcon name="i-lucide-database" class="text-blue-500 size-3.5" />
              <span class="text-[10px] text-gray-500 dark:text-gray-400 uppercase tracking-widest font-semibold">Query</span>
            </div>
            <pre class="text-xs text-blue-600 dark:text-blue-400 whitespace-pre-wrap leading-relaxed font-mono selection:bg-blue-200 dark:selection:bg-blue-900">{{ invocation.input.query }}</pre>
          </div>

          <div class="px-4 py-3 border-t border-gray-200 dark:border-gray-800">
            <div class="flex items-center gap-2 mb-1.5">
              <UIcon name="i-lucide-message-circle" class="text-gray-400 size-3.5" />
              <span class="text-[10px] text-gray-500 dark:text-gray-400 uppercase tracking-widest font-semibold">Context</span>
            </div>
            <p class="text-xs text-gray-600 dark:text-gray-400 italic leading-relaxed">
              {{ invocation.input.reason }}
            </p>
          </div>

          <div v-if="invocation.state === 'output-available' && invocation.output?.description" class="px-4 py-3 border-t border-emerald-200 dark:border-emerald-900/50 bg-emerald-50/50 dark:bg-emerald-950/20">
            <div class="flex items-start gap-2">
              <UIcon name="i-lucide-check-circle" class="text-emerald-500 size-3.5 mt-0.5 shrink-0" />
              <p class="text-xs text-emerald-700 dark:text-emerald-400 leading-relaxed">
                {{ invocation.output.description }}
              </p>
            </div>
          </div>
        </div>
      </template>
    </UCollapsible>
  </div>
</template>
