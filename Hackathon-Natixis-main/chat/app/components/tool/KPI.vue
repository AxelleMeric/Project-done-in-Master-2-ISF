<script setup lang="ts">
const props = defineProps<{
  invocation: KPIUIToolInvocation
  isStreaming?: boolean
}>()

const output = computed(() => props.invocation.output)

const trendConfig = {
  up: { icon: 'i-lucide-trending-up', color: 'text-emerald-500' },
  down: { icon: 'i-lucide-trending-down', color: 'text-red-500' },
  stable: { icon: 'i-lucide-minus', color: 'text-gray-400' }
} as const

function formatValue(value: string | number): string {
  if (typeof value === 'string') return value
  if (Math.abs(value) >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(2)} Md`
  if (Math.abs(value) >= 1_000_000) return `${(value / 1_000_000).toFixed(2)} M`
  if (Math.abs(value) >= 1_000) return `${(value / 1_000).toFixed(2)} k`
  if (Number.isInteger(value)) return value.toLocaleString('fr-FR')
  return value.toLocaleString('fr-FR', { maximumFractionDigits: 2 })
}
</script>

<template>
  <div
    v-if="invocation.state === 'output-available' && output?.length"
    class="my-6 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 shadow-sm overflow-hidden"
  >
    <div class="flex items-center gap-3 px-5 py-3.5 border-b border-gray-100 dark:border-gray-800/80">
      <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
        <UIcon name="i-lucide-gauge" class="text-primary text-lg" />
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">
          KPI
        </p>
      </div>
      <UBadge
        :label="`${output.length} KPI${output.length > 1 ? 's' : ''}`"
        variant="subtle"
        color="neutral"
        size="xs"
      />
    </div>

    <div class="grid gap-4 p-5" :class="[output.length === 1 ? 'grid-cols-1' : output.length === 2 ? 'grid-cols-2' : output.length === 3 ? 'grid-cols-3' : 'grid-cols-2 lg:grid-cols-4']">
      <div
        v-for="(kpi, index) in output"
        :key="index"
        class="relative flex flex-col gap-2 rounded-lg border border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 p-4"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon :name="kpi.icon || 'i-lucide-activity'" class="text-primary size-4" />
            <span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              {{ kpi.label }}
            </span>
          </div>
          <div v-if="kpi.trend" class="flex items-center gap-1">
            <UIcon
              :name="trendConfig[kpi.trend].icon"
              :class="trendConfig[kpi.trend].color"
              class="size-3.5"
            />
            <span
              v-if="kpi.trendValue"
              :class="trendConfig[kpi.trend].color"
              class="text-xs font-medium"
            >
              {{ kpi.trendValue }}
            </span>
          </div>
        </div>

        <p class="text-2xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          {{ formatValue(kpi.value) }}
        </p>

        <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
          {{ kpi.description }}
        </p>
      </div>
    </div>
  </div>

  <div
    v-else-if="invocation.state !== 'output-available'"
    class="my-6 flex items-center gap-3 px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50"
  >
    <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
      <UIcon name="i-lucide-loader-2" class="text-primary animate-spin" />
    </div>
    <span class="text-sm text-gray-500 dark:text-gray-400 italic">
      Computing the KPI...
    </span>
  </div>
</template>
