<script setup lang="ts">
type SeriesItem = { key: string, name: string, color?: string }
type ChartOutput = {
  chartType?: 'line' | 'area' | 'bar' | 'donut' | 'bubble' | 'gantt'
  data: Record<string, unknown>[]
  series: SeriesItem[]
  xKey?: string
  xKeyStart?: string
  xKeyEnd?: string
  radiusKey?: string
  title?: string
  showLegend?: boolean
  isStacked?: boolean
  xLabel?: string
  yLabel?: string
}
type ChartUIToolInvocation = {
  state: string
  output: ChartOutput | null
}

const props = defineProps<{ invocation: ChartUIToolInvocation, isStreaming?: boolean }>()

const output = computed(() => props.invocation.output)
const chartType = computed(() => output.value?.chartType || 'line')

const chartIcon = computed(() => {
  switch (chartType.value) {
    case 'bar': return 'i-lucide-bar-chart-3'
    case 'area': return 'i-lucide-area-chart'
    case 'donut': return 'i-lucide-pie-chart'
    case 'bubble': return 'i-lucide-scatter-chart'
    case 'gantt': return 'i-lucide-line-chart'
    default: return 'i-lucide-line-chart'
  }
})

const chartLabel = computed(() => {
  switch (chartType.value) {
    case 'bar': return 'Bar'
    case 'area': return 'Area'
    case 'donut': return 'Donut'
    case 'bubble': return 'Bubble'
    case 'gantt': return 'Gantt'
    default: return 'Line'
  }
})

const yAxisKeys = computed(() => {
  if (!output.value?.series) return []
  return output.value.series.map(s => s.key)
})

function toNumber(value: unknown): number {
  if (typeof value === 'number') return Number.isFinite(value) ? value : 0
  if (typeof value !== 'string') return 0

  const normalized = value
    .trim()
    .replace(/\s/g, '')
    .replace(',', '.')
    .replace(/[^0-9.-]/g, '')

  const parsed = Number(normalized)
  return Number.isFinite(parsed) ? parsed : 0
}

function formatNumber(value: unknown): string {
  const num = Number(value)
  if (isNaN(num)) return String(value)
  if (Math.abs(num) >= 1_000_000_000) return `${(num / 1_000_000_000).toFixed(2)} Md`
  if (Math.abs(num) >= 1_000_000) return `${(num / 1_000_000).toFixed(2)} M`
  if (Math.abs(num) >= 1_000) return `${(num / 1_000).toFixed(2)} k`
  if (Number.isInteger(num)) return num.toLocaleString('fr-FR')
  return num.toLocaleString('fr-FR', { maximumFractionDigits: 2 })
}

function getTooltipTitle(values: Record<string, unknown> | undefined): string {
  if (!output.value?.xKey || !values) return ''
  const raw = values[output.value.xKey]
  return raw != null ? String(raw) : ''
}

function getTooltipItems(values: Record<string, unknown> | undefined) {
  if (!output.value || !values) return []
  return output.value.series.map((series, index) => ({
    label: series.name,
    color: series.color || `var(--vis-color${index})`,
    value: formatNumber(values[series.key])
  }))
}

function getDonutTooltip(values: Record<string, unknown> | undefined) {
  if (!output.value || !values) return { label: '', value: 0, percent: 0 }
  const d = output.value
  const label = String(values.label || '')
  const value = Number(values[label] ?? 0)
  const seriesKey = d.series?.[0]?.key
  const total = seriesKey
    ? d.data.reduce((sum, item) => sum + (Number(item[seriesKey]) || 0), 0)
    : 0
  const percent = total > 0 ? (value / total) * 100 : 0
  return { label, value, percent }
}

function getBubbleTooltipItems(values: Record<string, unknown> | undefined) {
  if (!values) return []
  const result: Array<{ label: string, value: string, color?: string }> = []

  if (values.x != null) {
    result.push({ label: 'X', value: formatNumber(values.x) })
  }
  if (values.y != null) {
    result.push({ label: 'Y', value: formatNumber(values.y) })
  }
  if (values.size != null) {
    result.push({ label: 'Taille', value: formatNumber(values.size) })
  }

  return result
}

function getDonutTooltipItems(values: Record<string, unknown> | undefined) {
  const tooltip = getDonutTooltip(values)
  return [
    { label: 'Valeur', value: formatNumber(tooltip.value) },
    { label: 'Part', value: `${tooltip.percent.toFixed(1)}%` }
  ]
}

function getGanttTooltipItems(values: Record<string, unknown> | undefined) {
  if (!values) return []
  const start = toNumber(values.start)
  const end = start + toNumber(values.length)
  return [
    {
      label: 'Période',
      value: `${new Date(start).toLocaleDateString('fr-FR')} - ${new Date(end).toLocaleDateString('fr-FR')}`
    },
    {
      label: 'Durée',
      value: getGanttDuration(start, end)
    }
  ]
}

function getGanttDuration(startDate: unknown, endDate: unknown): string {
  const start = Number(startDate)
  const end = Number(endDate)
  if (!Number.isFinite(start) || !Number.isFinite(end)) return ''
  const days = Math.max(1, Math.ceil((end - start) / (1000 * 60 * 60 * 24)))
  return `${days} jour${days > 1 ? 's' : ''}`
}

/**
 * Ensures all series values in data are actual numbers.
 * Keeps xKey as string (label), converts series keys to Number.
 */
const normalizedData = computed(() => {
  if (!output.value) return []
  const d = output.value
  return d.data.map((item) => {
    const row: Record<string, unknown> = {}
    // Copy xKey as-is (label/date string)
    if (d.xKey) row[d.xKey] = item[d.xKey]
    // Convert all series values to numbers
    for (const s of d.series) {
      row[s.key] = toNumber(item[s.key])
    }
    return row
  })
})

const transformedData = computed(() => {
  if (!output.value) return []
  const d = output.value

  switch (d.chartType) {
    case 'donut': {
      const s0 = d.series?.[0]
      return d.data.map(item => s0 ? toNumber(item[s0.key]) : 0)
    }

    case 'gantt':
      return d.data.map((item) => {
        const s0 = d.series?.[0]
        const start = new Date(String(item[d.xKeyStart!])).getTime()
        const end = new Date(String(item[d.xKeyEnd!])).getTime()
        return {
          label: String(item[d.xKey!]),
          start,
          length: Math.max(1, end - start),
          type: s0?.key ?? 'series0',
          raw: item
        }
      })

    case 'bubble':
      return d.data.map((item, index) => {
        const s0 = d.series?.[0]
        const x = toNumber(item[d.xKey!])
        const y = s0 ? toNumber(item[s0.key]) : 0
        const size = d.radiusKey ? toNumber(item[d.radiusKey]) : 1
        return {
          id: `${index}`,
          title: String(item[d.xKey!]),
          x,
          y,
          size,
          group: s0?.key ?? 'series0',
          ...item
        }
      })

    default:
      // line, area, bar — use normalizedData with proper number types
      return normalizedData.value
  }
})

const transformedCategories = computed(() => {
  if (!output.value) return {}
  const d = output.value

  const createCats = () => d.series.reduce<Record<string, { name: string, color?: string }>>((acc, s) => {
    acc[s.key] = { name: s.name, color: s.color }
    return acc
  }, {})

  switch (d.chartType) {
    case 'donut': {
      const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']
      return d.data.reduce<Record<string, { name: string, color: string }>>((acc, item, index) => {
        acc[index.toString()] = {
          name: String(item[d.xKey!]),
          color: colors[index % colors.length]!
        }
        return acc
      }, {})
    }
    case 'gantt': {
      const s0 = d.series?.[0]
      return { [s0?.key ?? 'series0']: { name: s0?.name ?? 'Series 1', color: s0?.color } }
    }
    case 'bubble': {
      const s0 = d.series?.[0]
      return { [s0?.key ?? 'series0']: { name: s0?.name ?? 'Series 1', color: s0?.color } }
    }
    default:
      return createCats()
  }
})

const chartProps = computed(() => {
  if (!output.value) return {}
  const d = output.value
  const data = transformedData.value
  const categories = transformedCategories.value

  switch (d.chartType) {
    case 'line':
    case 'area':
      return {
        height: 300,
        data,
        categories,
        hideLegend: d.showLegend === false,
        xFormatter: (_tick: number, i: number) => {
          const val = d.data[i]?.[d.xKey!]
          return val != null ? String(val) : ''
        },
        yFormatter: (value: number) => formatNumber(value),
        xLabel: d.xLabel,
        yLabel: d.yLabel,
        curveType: 'MonotoneX',
        yGridLine: true
      }

    case 'bar':
      return {
        height: 300,
        data,
        categories,
        xAxis: d.xKey,
        yAxis: yAxisKeys.value,
        hideLegend: d.showLegend === false,
        yGridLine: true,
        stacked: d.isStacked === true,
        yFormatter: (value: number) => formatNumber(value)
      }

    case 'donut':
      return {
        height: 300,
        data,
        categories
      }

    case 'bubble':
      return {
        height: 300,
        data,
        categories,
        categoryKey: 'group',
        xAccessor: (item: Record<string, unknown>) => toNumber(item.x),
        yAccessor: (item: Record<string, unknown>) => toNumber(item.y),
        sizeAccessor: (item: Record<string, unknown>) => toNumber(item.size),
        hideLegend: d.showLegend === false,
        xLabel: d.xLabel || 'X Axis',
        yLabel: d.yLabel || 'Y Axis',
        xGridLine: true,
        yGridLine: true
      }

    case 'gantt':
      return {
        height: 300,
        data,
        categories,
        x: (item: Record<string, unknown>) => toNumber(item.start),
        length: (item: Record<string, unknown>) => toNumber(item.length),
        type: (item: Record<string, unknown>) => String(item.type ?? 'series0'),
        showLabels: true,
        hideLegend: d.showLegend === false,
        xTickFormat: (date: number | Date) => new Date(Number(date)).toLocaleDateString('fr-FR', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        })
      }

    default:
      return {
        height: 300,
        data,
        categories,
        hideLegend: d.showLegend === false,
        xFormatter: (_tick: number, i: number) => {
          const val = d.data[i]?.[d.xKey!]
          return val != null ? String(val) : ''
        },
        yFormatter: (value: number) => formatNumber(value),
        yGridLine: true
      }
  }
})
</script>

<template>
  <div
    v-if="invocation.state === 'output-available' && output"
    class="my-6 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 shadow-sm overflow-hidden"
  >
    <div class="flex items-center gap-3 px-5 py-3.5 border-b border-gray-100 dark:border-gray-800/80">
      <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
        <UIcon :name="chartIcon" class="text-primary text-lg" />
      </div>
      <div class="flex-1 min-w-0">
        <p v-if="output.title" class="text-sm font-semibold text-gray-900 dark:text-gray-100 truncate">
          {{ output.title }}
        </p>
        <p v-else class="text-sm font-medium text-gray-500 dark:text-gray-400">
          Visualisation
        </p>
      </div>
      <UBadge
        :label="chartLabel"
        variant="subtle"
        color="neutral"
        size="xs"
      />
    </div>

    <div class="px-5 py-4">
      <div class="relative w-full">
        <ClientOnly>
          <LineChart v-if="chartType === 'line'" v-bind="(chartProps as any)">
            <template #tooltip="{ values }">
              <ChartTooltipContent
                :title="getTooltipTitle(values as Record<string, unknown>)"
                :items="getTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </LineChart>

          <AreaChart v-else-if="chartType === 'area'" v-bind="(chartProps as any)">
            <template #tooltip="{ values }">
              <ChartTooltipContent
                :title="getTooltipTitle(values as Record<string, unknown>)"
                :items="getTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </AreaChart>

          <BarChart v-else-if="chartType === 'bar'" v-bind="(chartProps as any)">
            <template #tooltip="{ values }">
              <ChartTooltipContent
                :title="getTooltipTitle(values as Record<string, unknown>)"
                :items="getTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </BarChart>

          <DonutChart v-else-if="chartType === 'donut'" v-bind="(chartProps as any)">
            <template #tooltip="{ values }">
              <ChartTooltipContent
                :title="getDonutTooltip(values as Record<string, unknown>).label"
                :items="getDonutTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </DonutChart>

          <BubbleChart v-else-if="chartType === 'bubble'" v-bind="(chartProps as any)">
            <template #tooltip="{ values }">
              <ChartTooltipContent
                :title="String((values as Record<string, unknown>)?.title || '')"
                :items="getBubbleTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </BubbleChart>

          <GanttChart v-else-if="chartType === 'gantt'" v-bind="(chartProps as any)">
            <template #labelTooltip="{ values }">
              <ChartTooltipContent
                :title="String((values as Record<string, unknown>)?.name || (values as Record<string, unknown>)?.label || '')"
                :items="getGanttTooltipItems(values as Record<string, unknown>)"
              />
            </template>
          </GanttChart>
          <LineChart v-else v-bind="(chartProps as any)" />
        </ClientOnly>
      </div>
    </div>

    <div class="px-5 py-2.5 border-t border-gray-100 dark:border-gray-800/80 flex items-center justify-between">
      <span class="text-[11px] text-gray-400 dark:text-gray-500">
        {{ output.data.length }} point{{ output.data.length > 1 ? 's' : '' }} de données
      </span>
      <span class="text-[11px] text-gray-400 dark:text-gray-500">
        {{ output.series.length }} série{{ output.series.length > 1 ? 's' : '' }}
      </span>
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
      Génération du graphique…
    </span>
  </div>
</template>
