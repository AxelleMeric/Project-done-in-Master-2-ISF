<script setup lang="ts">
const { model, models, formatModelName, getModel } = useModels()

const items = computed(() => models.map(modelItem => ({
  label: formatModelName(modelItem.name),
  value: modelItem.name,
  icon: modelItem.icon,
  reasoning: modelItem.reasoning,
  cloud: modelItem.cloud,
  cost: modelItem.cost,
  modelId: modelItem.name
})))

const selectedModel = computed(() => getModel(model.value))

const selectedLabel = computed(() => {
  if (!selectedModel.value) return 'Select model'
  return formatModelName(selectedModel.value.name)
})

function costSymbol(cost: 'low' | 'mid' | 'high') {
  if (cost === 'high') return '$$$'
  if (cost === 'mid') return '$$'
  return '$'
}

function costTooltip(cost: 'low' | 'mid' | 'high') {
  if (cost === 'high') return 'High cost model ($$$)'
  if (cost === 'mid') return 'Mid cost model ($$)'
  return 'Low cost model ($)'
}
</script>

<template>
  <USelectMenu
    v-model="model"
    :items="items"
    size="md"
    variant="soft"
    value-key="value"
    color="primary"
    class="min-w-72"
    :ui="{
      base: 'rounded-xl',
      leadingIcon: 'text-[--ui-text-muted]',
      content: 'min-w-96 rounded-xl',
      item: 'rounded-lg py-2',
      itemLeadingIcon: 'hidden',
      trailingIcon: 'group-data-[state=open]:rotate-180 transition-transform duration-200'
    }"
  >
    <template #leading>
      <UIcon :name="selectedModel?.icon || 'i-lucide-bot'" class="size-4 text-[--ui-text-muted]" />
    </template>

    <template #default>
      <div class="flex items-center gap-2 min-w-0">
        <span class="truncate font-medium">{{ selectedLabel }}</span>

        <template v-if="selectedModel">
          <UTooltip v-if="selectedModel.reasoning" text="Thinking mode enabled">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <UIcon name="i-lucide-brain" class="size-3.5 text-warning" />
            </span>
          </UTooltip>

          <UTooltip :text="selectedModel.cloud ? 'Cloud model' : 'Local model'">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <UIcon :name="selectedModel.cloud ? 'i-lucide-cloud' : 'i-lucide-hard-drive'" class="size-3.5 text-info" />
            </span>
          </UTooltip>

          <UTooltip :text="costTooltip(selectedModel.cost)">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <span class="text-[11px] leading-none font-semibold tracking-tight text-success">
                {{ costSymbol(selectedModel.cost) }}
              </span>
            </span>
          </UTooltip>
        </template>
      </div>
    </template>

    <template #item="{ item }">
      <div class="flex items-start justify-between w-full gap-3">
        <div class="flex items-start gap-3 min-w-0">
          <div class="mt-0.5 rounded-md border border-default p-1.5 bg-elevated/40">
            <UIcon :name="item.icon" class="size-4 text-[--ui-text]" />
          </div>

          <div class="min-w-0">
            <div class="font-semibold truncate">
              {{ item.label }}
            </div>
            <div class="text-xs text-muted truncate mt-0.5">
              {{ item.modelId }}
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1 shrink-0">
          <UTooltip v-if="item.reasoning" text="Thinking mode enabled">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <UIcon name="i-lucide-brain" class="size-3.5 text-warning" />
            </span>
          </UTooltip>

          <UTooltip :text="item.cloud ? 'Cloud model' : 'Local model'">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <UIcon :name="item.cloud ? 'i-lucide-cloud' : 'i-lucide-hard-drive'" class="size-3.5 text-info" />
            </span>
          </UTooltip>

          <UTooltip :text="costTooltip(item.cost)">
            <span class="inline-flex items-center justify-center rounded-md border border-default bg-elevated/60 p-1">
              <span class="text-[11px] leading-none font-semibold tracking-tight text-success">
                {{ costSymbol(item.cost) }}
              </span>
            </span>
          </UTooltip>
        </div>
      </div>
    </template>
  </USelectMenu>
</template>
