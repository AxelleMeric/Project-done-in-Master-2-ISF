import { tool, type UIToolInvocation } from 'ai'
import { log } from 'node:console'
import { z } from 'zod'

export type KPIUIToolInvocation = UIToolInvocation<typeof kpiTool>

export const kpiTool = tool({
  description: 'Affiche un ensemble de KPIs avec chiffres, descriptions et icônes.',
  inputSchema: z.object({
    kpis: z.array(
      z.object({
        label: z.string().describe('Nom du KPI'),
        value: z.string().or(z.number()).describe('Valeur du KPI'),
        description: z.string().describe('Description de la valeur'),
        icon: z.string().describe('Nom de l\'icône SimpleIcon'),
        trend: z.enum(['up', 'down', 'stable']).optional().describe('Tendance'),
        trendValue: z.string().optional().describe('Pourcentage de variation')
      })
    )
  }),
  execute: async (input) => {
    await new Promise(resolve => setTimeout(resolve, 300))
    log(`📊 ${input.kpis.length} KPI(s) affichés`)
    return input.kpis
  }
})
