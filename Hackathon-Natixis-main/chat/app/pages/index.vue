<script setup lang="ts">
import { Chat } from '@ai-sdk/vue'
import { useFocus } from '@vueuse/core'

const focusElement = shallowRef<HTMLElement | null>(null)
const input = ref('')
const loading = ref(false)

const { focused } = useFocus(focusElement)
const { model } = useModels()

function prepareChat(prompt: string) {
  input.value = prompt
  focused.value = true
}

const chat = new Chat({})
async function onSubmit() {
  loading.value = true

  const questionState = useState('question', () => '')
  questionState.value = input.value

  loading.value = false
  input.value = ''

  await navigateTo('/chat', { replace: true })
}

const quickChats: { label: string, prompt: string, icon: string }[] = [
  {
    label: 'My open anomalies',
    prompt: 'Show me all anomalies currently assigned to me that are still open, grouped by priority level.',
    icon: 'i-lucide-user-check'
  },
  {
    label: 'Anomaly trends & statistics',
    prompt: 'Provide a detailed breakdown of anomaly statistics over the last quarter, including trends, top categories, and severity distribution.',
    icon: 'i-lucide-bar-chart-3'
  },
  {
    label: 'Contract anomalies',
    prompt: 'List all anomalies linked to my contracts, including their current status, severity, and assigned remediation owner.',
    icon: 'i-lucide-file-search'
  },
  {
    label: 'Remediation ownership',
    prompt: 'Who is responsible for remediating the currently open critical and high-severity anomalies, and what is their progress?',
    icon: 'i-lucide-shield-question'
  },
  {
    label: 'Recent anomalies summary',
    prompt: 'Give me an executive summary of all anomalies detected in the last 30 days, highlighting any recurring patterns or escalations.',
    icon: 'i-lucide-notebook-text'
  },
  {
    label: 'Resolution time analysis',
    prompt: 'What are the average and median resolution times for anomalies broken down by type and severity? Highlight any that exceed SLA targets.',
    icon: 'i-lucide-clock'
  },
  {
    label: 'Critical anomalies overview',
    prompt: 'How many critical anomalies were detected last month? List the top 5 by impact and their current remediation status.',
    icon: 'i-lucide-shield-alert'
  },
  {
    label: 'Overdue anomalies',
    prompt: 'Which anomalies have exceeded their expected resolution date and are still unresolved? Sort them by days overdue.',
    icon: 'i-lucide-alarm-clock-off'
  },
  {
    label: 'Root cause analysis',
    prompt: 'What are the most common root causes for anomalies detected this quarter? Suggest preventive measures for the top 3.',
    icon: 'i-lucide-search'
  },
  {
    label: 'Team workload',
    prompt: 'Show me the current anomaly workload distribution across team members, including open count and average age of assigned anomalies.',
    icon: 'i-lucide-users'
  },
  {
    label: 'Recurring anomalies',
    prompt: 'Identify any anomalies that have recurred more than once in the past 6 months and suggest actions to prevent future occurrences.',
    icon: 'i-lucide-repeat'
  },
  {
    label: 'Anomaly risk forecast',
    prompt: 'Based on historical data, which areas or contract types are most likely to generate new anomalies in the coming month?',
    icon: 'i-lucide-trending-up'
  }
]
</script>

<template>
  <UContainer class="flex-1 flex flex-col justify-center gap-6 sm:gap-10 h-full max-w-4xl">
    <div class="text-center flex flex-col items-center gap-3">
      <div class="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-semibold text-primary mb-2">
        <UIcon name="i-lucide-sparkles" class="text-base" />
        <span>AI-powered anomaly assistant</span>
      </div>
      <h1 class="text-4xl sm:text-5xl font-bold tracking-tight">
        Natixis <span class="text-primary">Chat</span>
      </h1>
      <p class="text-lg text-muted max-w-lg text-pretty leading-relaxed">
        Get real-time anomaly detection, insights, and resolution guidance powered by AI.
      </p>
    </div>

    <UCard class="[view-transition-name:chat-prompt] shadow-lg ring-1 ring-neutral-200 dark:ring-neutral-700" variant="outline" :ui="{ body: 'p-2 sm:p-2', root: 'rounded-2xl overflow-hidden' }">
      <ClientOnly>
        <UChatPrompt
          ref="focusElement"
          v-model="input"
          :error="chat.error"
          variant="subtle"
          placeholder="Ask me anything about anomalies..."
          :ui="{ base: 'px-1.5' }"
          :maxrows="5"
          @submit="onSubmit"
        >
          <template #footer>
            <div class="flex items-center justify-end w-full gap-4">
              <div class="flex items-center gap-1">
                <ModelSelect v-model="model" />
              </div>

              <UChatPromptSubmit
                :status="chat.status"
                color="primary"
                variant="solid"
                submitted-color="error"
                submitted-variant="solid"
                streaming-color="error"
                streaming-variant="solid"
                error-color="error"
                error-variant="soft"
                error-icon="i-lucide-rotate-ccw"
                size="md"
                @stop="chat.stop()"
                @reload="chat.regenerate()"
              />
            </div>
          </template>
        </UChatPrompt>
      </ClientOnly>
    </UCard>

    <div class="space-y-3">
      <p class="text-xs font-semibold uppercase tracking-widest text-muted text-center">
        Quick prompts
      </p>
      <div class="flex flex-wrap justify-center gap-2">
        <button
          v-for="quickChat in quickChats"
          :key="quickChat.label"
          class="group inline-flex items-center gap-2 rounded-full border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-900 px-4 py-2 text-sm transition-all duration-200 hover:border-primary hover:shadow-md hover:shadow-primary/5 hover:-translate-y-0.5 active:translate-y-0"
          @click.prevent="prepareChat(quickChat.prompt)"
        >
          <UIcon :name="quickChat.icon" class="text-base text-muted group-hover:text-primary transition-colors" />
          <span class="font-medium text-neutral-700 dark:text-neutral-300 group-hover:text-primary transition-colors">{{ quickChat.label }}</span>
        </button>
      </div>
    </div>
  </UContainer>
</template>
