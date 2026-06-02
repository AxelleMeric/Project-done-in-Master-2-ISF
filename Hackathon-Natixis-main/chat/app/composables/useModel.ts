export function formatModelName(modelId: string): string {
  const acronyms = ['gpt', 'glm'] // words that should be uppercase
  const modelName = modelId.split('/')[1] || modelId

  const cleanedName = modelName.replace(/-cloud$/, '').replace(/:cloud$/, '')

  return cleanedName
    .split('-')
    .map((word) => {
      const lowerWord = word.toLowerCase()
      return acronyms.includes(lowerWord)
        ? word.toUpperCase()
        : word.charAt(0).toUpperCase() + word.slice(1)
    })
    .join(' ')
}

export type ModelCostTier = 'low' | 'mid' | 'high'

export type ModelDescriptor = {
  name: string
  icon: string
  reasoning: boolean
  cloud: boolean
  cost: ModelCostTier
}

export function useModels() {
  const models: ModelDescriptor[] = [
    {
      name: 'deepseek-v3.1:671b-cloud',
      icon: 'i-hugeicons-deepseek',
      reasoning: true,
      cloud: true,
      cost: 'high'
    },
    {
      name: 'gpt-oss:20b-cloud',
      icon: 'i-simple-icons-openai',
      reasoning: true,
      cloud: true,
      cost: 'low'
    },
    {
      name: 'gpt-oss:120b-cloud',
      icon: 'i-simple-icons-openai',
      reasoning: true,
      cloud: true,
      cost: 'high'
    },
    {
      name: 'gemma3:4b',
      icon: 'i-hugeicons-google',
      reasoning: false,
      cloud: false,
      cost: 'low'
    },
    {
      name: 'ministral-3:14b-cloud',
      icon: 'i-hugeicons-mistral',
      reasoning: false,
      cloud: true,
      cost: 'low'
    },
    {
      name: 'kimi-k2.5:cloud',
      icon: 'i-lucide-sparkles',
      reasoning: true,
      cloud: true,
      cost: 'high'
    },
    {
      name: 'glm-5:cloud',
      icon: 'i-lucide-cpu',
      reasoning: true,
      cloud: true,
      cost: 'mid'
    },
    {
      name: 'qwen3.5:397b-cloud',
      icon: 'i-simple-icons-alibabacloud',
      reasoning: true,
      cloud: true,
      cost: 'mid'
    },
    {
      name: 'minimax-m2.5:cloud',
      icon: 'i-lucide-orbit',
      reasoning: true,
      cloud: true,
      cost: 'high'
    }
  ]

  function getModel(name: string) {
    return models.find(model => model.name === name)
  }

  const model = useCookie<string>('model', { default: () => models[0]!.name })

  return {
    models,
    model,
    formatModelName,
    getModel
  }
}
