import { tool, type UIToolInvocation } from 'ai'
import { log } from 'node:console'
import { z } from 'zod'

export type ChartUIToolInvocation = UIToolInvocation<typeof chartTool>

export const chartTool = tool({
  description: 'Génère une visualisation de données (Line, Bar, Area, Donut, Bubble, Gantt).',
  inputSchema: z.object({
    title: z.string().optional(),
    chartType: z.preprocess(
      val => (typeof val === 'string' ? val.toLowerCase() : val),
      z.enum(['line', 'bar', 'area', 'donut', 'bubble', 'gantt']).default('line')
    ),
    data: z.array(z.record(z.string(), z.union([z.string(), z.number()]))),
    xKey: z.string(),
    xKeyStart: z.string().optional(),
    xKeyEnd: z.string().optional(),
    radiusKey: z.string().optional(),
    series: z.array(
      z.preprocess(
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        (val: any) => {
          if (val && typeof val === 'object' && !val.name && val.label) {
            return { ...val, name: val.label }
          }
          return val
        },
        z.object({
          key: z.string(),
          name: z.string()
        })
      )
    ),

    showMarkers: z.boolean().optional().default(false),
    showLegend: z.boolean().optional().default(true),
    xLabel: z.string().optional(),
    yLabel: z.string().optional(),
    isStacked: z.boolean().optional().default(false)
  }),
  execute: async (input) => {
    await new Promise(resolve => setTimeout(resolve, 300))
    log('📈 Chart tool successfully executed')
    return input
  }
})
