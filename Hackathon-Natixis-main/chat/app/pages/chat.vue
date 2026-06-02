<script setup lang="ts">
import { Chat } from '@ai-sdk/vue'
import { useClipboard } from '@vueuse/core'
import { DefaultChatTransport, type UIMessage } from 'ai'
import { getTextFromMessage } from '@nuxt/ui/utils/ai'

const input = ref('')
const loading = ref(false)
const { model } = useModels()

const toast = useToast()

const chat = new Chat({
  transport: new DefaultChatTransport({
    api: `/api/chat`,
    body: {
      model: model.value
    }
  }),
  onError(error) {
    const message = typeof error.message === 'string' && error.message[0] === '{'
      ? JSON.parse(error.message).message
      : error.message
    toast.add({
      description: message,
      icon: 'i-lucide-alert-circle',
      color: 'error',
      duration: 0
    })
  }
})

onMounted(async () => {
  const questionState = useState('question', () => '')
  if (questionState.value) {
    await createChat(questionState.value)
    questionState.value = ''
  } else {
    await navigateTo('/')
  }
})

async function createChat(prompt: string) {
  input.value = prompt
  loading.value = true
  chat.sendMessage({ text: input.value })
  loading.value = false
  input.value = ''
}

async function onSubmit() {
  await createChat(input.value)
}

const clipboard = useClipboard()
const copied = ref(false)

function copy(message: UIMessage) {
  clipboard.copy(getTextFromMessage(message))
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2000)
}

const assistant = computed(() => {
  const commonAvatar = { avatar: { icon: 'i-lucide-bot' } }
  if (chat.status !== 'streaming') {
    return {
      ...commonAvatar,
      actions: [
        {
          label: 'Copy',
          icon: copied.value ? 'i-lucide-copy-check' : 'i-lucide-copy',
          onClick: (_: unknown, message: UIMessage) => copy(message)
        }
      ]
    }
  }
  return {
    ...commonAvatar,
    actions: []
  }
})

type UIBlock
  = | { type: 'reasoning', text: string, isStreaming: boolean }
    | { type: 'text', text: string, isStreaming: boolean }
    | { type: 'tool', part: Part, isStreaming: boolean }

type Part
  = | { type: 'reasoning', text: string }
    | { type: 'text', text: string }
    | {
      type: 'tool-executeSqlTool' | 'tool-chartTool' | 'tool-kpiTool' | 'tool-invocation'
      state: string
      input: unknown
      output?: unknown
      toolCallId: string
    }

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function groupParts(parts: any[], status: string): UIBlock[] {
  const blocks: UIBlock[] = []

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i]

    if (part.type === 'reasoning' && !part.text?.trim() && i < parts.length - 1) continue

    const lastBlock = blocks[blocks.length - 1]
    const isStreaming = status === 'streaming' && i === parts.length - 1

    if (part.type === 'reasoning') {
      if (lastBlock?.type === 'reasoning') {
        lastBlock.text += part.text
        lastBlock.isStreaming = isStreaming
      } else {
        blocks.push({ type: 'reasoning', text: part.text, isStreaming })
      }
    } else if (part.type === 'text') {
      if (lastBlock?.type === 'text') {
        lastBlock.text += part.text
        lastBlock.isStreaming = isStreaming
      } else {
        blocks.push({ type: 'text', text: part.text, isStreaming })
      }
    } else if (part.type.startsWith('tool-')) {
      blocks.push({
        type: 'tool',
        part: part,
        isStreaming
      })
    }
  }
  return blocks
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function hasKpiToolPart(parts: any[]): boolean {
  return parts.some(part => part?.type === 'tool-kpiTool')
}

function removeMarkdownTables(text: string): string {
  const lines = text.split('\n')
  const filtered = lines.filter(line => !/^\s*\|.*\|\s*$/.test(line))

  return filtered
    .join('\n')
    .replace(/^\s*#+\s*KPIs?.*$/gim, '')
    .replace(/^\s*KPIs?\s*[-–].*$/gim, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function renderTextBlock(text: string, parts: any[]): string {
  if (!hasKpiToolPart(parts)) return text
  return removeMarkdownTables(text)
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function hasRenderableText(text: string, parts: any[]): boolean {
  return renderTextBlock(text, parts).trim().length > 0
}
</script>

<template>
  <UDashboardPanel class="relative" :ui="{ body: 'p-0 sm:p-0' }">
    <template #body>
      <UContainer class="flex flex-col h-full overflow-hidden mb-32">
        <UChatMessages
          should-auto-scroll
          :messages="chat.messages"
          :status="chat.status"
          :assistant="assistant"
          :user="{
            ui: {
              content: 'py-0'
            }
          }"
          class="flex-1 overflow-y-auto my-16"
        >
          <template #content="{ message }">
            <template v-for="(block, index) in groupParts(message.parts, chat.status)" :key="index">
              <Reasoning
                v-if="block.type === 'reasoning'"
                :text="block.text"
                :is-streaming="block.isStreaming"
              />

              <ToolSqlDisplay
                v-else-if="block.type === 'tool' && block.part.type === 'tool-executeSqlTool'"
                :invocation="(block.part as any).toolInvocation || block.part"
                :is-streaming="block.isStreaming"
              />

              <ToolChart
                v-else-if="block.type === 'tool' && block.part.type === 'tool-chartTool'"
                :invocation="(block.part as any).toolInvocation || block.part"
                :is-streaming="block.isStreaming"
              />

              <ToolKPI
                v-else-if="block.type === 'tool' && block.part.type === 'tool-kpiTool'"
                :invocation="(block.part as any).toolInvocation || block.part"
                :is-streaming="block.isStreaming"
              />

              <MDCCached
                v-else-if="block.type === 'text' && hasRenderableText(block.text, message.parts)"
                :value="renderTextBlock(block.text, message.parts)"
                :cache-key="`${message.id}-text-${index}`"
                class="prose dark:prose-invert max-w-none"
              />
            </template>
          </template>
        </UChatMessages>
      </UContainer>
    </template>

    <template #footer>
      <div class="fixed bottom-8 left-0 right-0 flex justify-center w-full">
        <UCard
          variant="outline"
          :ui="{ body: 'p-2 sm:p-2', root: 'rounded-xl overflow-hidden' }"
          class="[view-transition-name:chat-prompt] max-w-(--ui-container) w-full"
        >
          <div class="mx-auto w-full">
            <UChatPrompt
              v-model="input"
              :error="chat.error"
              variant="subtle"
              class="z-10 w-full"
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
          </div>
        </UCard>
      </div>
    </template>
  </UDashboardPanel>
</template>
