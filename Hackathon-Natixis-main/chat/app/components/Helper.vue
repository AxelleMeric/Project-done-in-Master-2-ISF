<script lang="ts" setup>
const isOpen = ref(false)

const items = [
  {
    label: 'Getting Started',
    icon: 'i-lucide-rocket',
    slot: 'guide'
  },
  {
    label: 'Available Data',
    icon: 'i-lucide-database',
    slot: 'data'
  }
]

const steps = [
  {
    title: '1. Ask a Question',
    description: 'Type a natural language question like "Show me the top 5 applications with the most critical anomalies this quarter."',
    icon: 'i-lucide-message-circle-question',
    color: 'text-blue-500',
    bg: 'bg-blue-50 dark:bg-blue-950/30'
  },
  {
    title: '2. AI Reasoning',
    description: 'The assistant interprets your intent, selects the optimal SQL strategy, and determines the best visualization type.',
    icon: 'i-lucide-brain-circuit',
    color: 'text-violet-500',
    bg: 'bg-violet-50 dark:bg-violet-950/30'
  },
  {
    title: '3. Query & Visualize',
    description: 'The database is queried in real time and an interactive chart is rendered instantly — no manual work needed.',
    icon: 'i-lucide-chart-spline',
    color: 'text-emerald-500',
    bg: 'bg-emerald-50 dark:bg-emerald-950/30'
  },
  {
    title: '4. Insights Summary',
    description: 'A concise AI-generated narrative highlights key findings, trends, and actionable takeaways from the data.',
    icon: 'i-lucide-sparkles',
    color: 'text-amber-500',
    bg: 'bg-amber-50 dark:bg-amber-950/30'
  }
]

const metrics = [
  { label: 'Volume', value: 'Total anomaly count', icon: 'i-lucide-sigma', color: 'text-blue-500', bg: 'bg-blue-50 dark:bg-blue-950/30' },
  { label: 'Flow Analysis', value: 'Open vs Closed status', icon: 'i-lucide-arrow-right-left', color: 'text-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-950/30' },
  { label: 'Criticality', value: 'High Priority & CDE flags', icon: 'i-lucide-shield-alert', color: 'text-orange-500', bg: 'bg-orange-50 dark:bg-orange-950/30' },
  { label: 'Time Range', value: 'Rolling 3-month window', icon: 'i-lucide-calendar-range', color: 'text-neutral-500', bg: 'bg-neutral-50 dark:bg-neutral-800/50' }
]

const exampleQueries = [
  'What is the monthly trend of critical anomalies?',
  'Compare open vs closed anomalies by application',
  'Show the distribution of anomalies by severity'
]
</script>

<template>
  <UModal v-model:open="isOpen" :ui="{ content: 'bg-default divide-y divide-default flex flex-col focus:outline-none sm:max-w-3xl' }">
    <UButton
      icon="i-lucide-circle-help"
      color="primary"
      variant="ghost"
      label="Help & Guide"
    />
    <template #header>
      <div class="flex items-center justify-between w-full">
        <div class="flex items-center gap-3">
          <div class="p-2.5 bg-linear-to-br from-primary-100 to-primary-50 dark:from-primary-950/60 dark:to-primary-900/30 rounded-xl flex items-center justify-center ring-1 ring-primary-200 dark:ring-primary-800">
            <UIcon name="i-lucide-bot" class="w-6 h-6 text-primary-500" />
          </div>
          <div>
            <h3 class="text-base font-bold leading-6 text-neutral-900 dark:text-white">
              Data Quality Assistant
            </h3>
            <p class="text-xs text-neutral-400 dark:text-neutral-500 mt-0.5">
              Natural language → SQL → Charts — powered by AI
            </p>
          </div>
        </div>
        <UButton
          color="neutral"
          variant="ghost"
          icon="i-lucide-x"
          size="sm"
          @click.prevent="isOpen = false"
        />
      </div>
    </template>

    <template #footer>
      <div class="flex items-center gap-3 w-full justify-center">
        <UButton
          color="primary"
          label="Got it, let's explore!"
          trailing-icon="i-lucide-arrow-right"
          @click.prevent="isOpen = false"
        />
      </div>
    </template>

    <template #body>
      <UTabs :items="items" class="w-full">
        <template #guide>
          <div class="p-5 space-y-6">
            <div class="p-4 rounded-xl bg-linear-to-r from-primary-50 to-blue-50 dark:from-primary-950/20 dark:to-blue-950/20 border border-primary-100 dark:border-primary-900/50">
              <p class="text-sm text-neutral-700 dark:text-neutral-200 leading-relaxed">
                Ask questions about your data quality in <strong>your language</strong>. The assistant automatically writes SQL queries,
                executes them against your database, and generates interactive visualizations — all in seconds.
              </p>
            </div>

            <div>
              <h4 class="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                How it works
              </h4>
              <div class="grid grid-cols-2 gap-2">
                <div
                  v-for="(step, index) in steps"
                  :key="index"
                  class="flex items-start gap-4 p-3.5 rounded-xl border border-neutral-200 dark:border-neutral-800"
                >
                  <div class="p-2 rounded-lg shrink-0 flex items-center justify-center" :class="step.bg">
                    <UIcon :name="step.icon" class="w-5 h-5" :class="step.color" />
                  </div>
                  <div class="min-w-0">
                    <h4 class="font-semibold text-sm text-neutral-900 dark:text-white">
                      {{ step.title }}
                    </h4>
                    <p class="text-xs text-neutral-500 dark:text-neutral-400 leading-relaxed mt-0.5">
                      {{ step.description }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h4 class="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                Try these prompts
              </h4>
              <div class="flex flex-col gap-2">
                <div
                  v-for="query in exampleQueries"
                  :key="query"
                  class="flex items-center gap-2.5 px-3.5 py-2.5 rounded-lg bg-neutral-50 dark:bg-neutral-800/50 border border-neutral-100 dark:border-neutral-800 text-sm text-neutral-600 dark:text-neutral-300"
                >
                  <UIcon name="i-lucide-sparkles" class="w-3.5 h-3.5 text-primary-400 shrink-0" />
                  <span class="italic">"{{ query }}"</span>
                </div>
              </div>
            </div>

            <UAlert
              icon="i-lucide-lightbulb"
              color="primary"
              variant="subtle"
              title="Pro tips for better results"
            >
              <template #description>
                <ul class="text-sm mt-2 space-y-1.5">
                  <li class="flex items-start gap-2">
                    <UIcon name="i-lucide-filter" class="w-3.5 h-3.5 mt-0.5 text-primary-400 shrink-0" />
                    <span>Specify filters — e.g., <em>"Only for the Falcon application"</em></span>
                  </li>
                  <li class="flex items-start gap-2">
                    <UIcon name="i-lucide-bar-chart-3" class="w-3.5 h-3.5 mt-0.5 text-primary-400 shrink-0" />
                    <span>Ask for <strong>comparisons</strong> to get bar charts</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <UIcon name="i-lucide-pie-chart" class="w-3.5 h-3.5 mt-0.5 text-primary-400 shrink-0" />
                    <span>Ask for <strong>breakdowns</strong> or distributions to get donut charts</span>
                  </li>
                </ul>
              </template>
            </UAlert>
          </div>
        </template>

        <template #data>
          <div class="p-5 space-y-6">
            <div class="p-4 rounded-xl bg-linear-to-r from-neutral-50 to-blue-50 dark:from-neutral-900/50 dark:to-blue-950/20 border border-neutral-100 dark:border-neutral-800">
              <p class="text-sm text-neutral-700 dark:text-neutral-200 leading-relaxed">
                The assistant operates on a <strong>data quality anomaly dataset</strong> covering a rolling window.
                Below are the key dimensions and concepts you can explore.
              </p>
            </div>

            <div>
              <h4 class="text-xs font-semibold uppercase tracking-wider text-neutral-400 mb-3">
                Queryable Dimensions
              </h4>
              <div class="grid grid-cols-2 gap-3">
                <div
                  v-for="metric in metrics"
                  :key="metric.label"
                  class="flex items-center gap-3.5 p-4 rounded-xl border border-neutral-200 dark:border-neutral-800 hover:shadow-sm transition-shadow"
                >
                  <div class="p-2.5 rounded-lg shrink-0 flex items-center justify-center" :class="metric.bg">
                    <UIcon :name="metric.icon" class="w-5 h-5" :class="metric.color" />
                  </div>
                  <div>
                    <div class="text-[11px] text-neutral-400 font-semibold uppercase tracking-wide">
                      {{ metric.label }}
                    </div>
                    <div class="text-sm font-bold text-neutral-800 dark:text-white mt-0.5">
                      {{ metric.value }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/50 flex items-start gap-3">
              <UIcon name="i-lucide-info" class="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
              <div>
                <p class="text-xs font-semibold text-amber-700 dark:text-amber-400">
                  Demo Dataset Notice
                </p>
                <p class="text-xs text-amber-600 dark:text-amber-500 mt-1 leading-relaxed">
                  The reference date for "today" is <strong>November 21, 2025</strong>. All relative time expressions
                  (e.g., "last month", "this quarter") are computed from this date.
                </p>
              </div>
            </div>
          </div>
        </template>
      </UTabs>
    </template>
  </UModal>
</template>
