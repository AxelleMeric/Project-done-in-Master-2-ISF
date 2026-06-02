import { tool, type UIToolInvocation } from 'ai'
import { z } from 'zod'
import { db } from 'hub:db'

export type SQLUIToolInvocation = UIToolInvocation<typeof executeSqlTool>

export const executeSqlTool = tool({
  description: 'INDISPENSABLE. Execute OBLIGATOIREMENT a SELECT SQL query against the database to fetch data. Always use LIMIT to avoid large datasets unless necessary.',
  inputSchema: z.object({
    query: z.string().describe('The SQL SELECT query to execute. Must be valid MySQL syntax.'),
    reason: z.string().describe('The reason why you are running this query (for debugging context).')
  }),
  outputSchema: z.object({
    description: z.string().describe('The JSON stringified result of the SQL query execution or an error message.'),
    result: z.string().describe('The JSON stringified result of the SQL query execution or an error message.').optional()
  }),
  execute: async ({ query }) => {
    try {
      console.log('⚡ executing SQL:', query)

      // Sécurité basique : Interdire les modifications
      if (!/^\s*SELECT/i.test(query)) {
        return {
          description: 'ERROR: Only SELECT queries are allowed.',
          result: undefined
        }
      }

      const rows = await db.execute(query)

      // Protection contexte : On coupe si trop de résultats
      if (Array.isArray(rows) && rows.length > 50) {
        return {
          description: 'Result truncated to 50 rows to save context.',
          result: JSON.stringify({
            warning: 'Result truncated to 50 rows to save context.',
            data: rows.slice(0, 50)
          })
        }
      }

      return {
        description: 'Query executed successfully',
        result: JSON.stringify(rows)
      }
    } catch (error: unknown) {
      return {
        description: `SQL ERROR: ${error}. Please check your query syntax and table names.`,
        result: undefined
      }
    }
  }
})
