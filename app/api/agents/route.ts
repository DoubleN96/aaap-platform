import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { z } from 'zod'

const CreateAgentSchema = z.object({
  name: z.string().min(3, 'Name must be at least 3 characters'),
  description: z.string().optional(),
  role: z.enum([
    'email_assistant',
    'crm_manager',
    'scheduler',
    'analyst',
    'custom',
  ]),
  personality: z
    .object({
      tone: z.string(),
      language: z.string(),
      verbosity: z.string(),
      formality: z.string(),
    })
    .optional(),
  capabilities: z.array(z.string()).optional(),
  system_prompt: z.string().optional(),
})

export async function GET(request: NextRequest) {
  try {
    const supabase = createClient()

    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { data, error } = await supabase
      .from('ai_agents')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Error fetching agents:', error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ agents: data })
  } catch (error) {
    console.error('Unexpected error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const supabase = createClient()

    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const body = await request.json()
    const validated = CreateAgentSchema.parse(body)

    const { data: agent, error } = await supabase
      .from('ai_agents')
      .insert({
        user_id: user.id,
        name: validated.name,
        description: validated.description || null,
        role: validated.role,
        personality: validated.personality || {
          tone: 'professional',
          language: 'es',
          verbosity: 'balanced',
          formality: 'medium',
        },
        capabilities: validated.capabilities || [],
        system_prompt:
          validated.system_prompt || `You are a helpful ${validated.role} assistant.`,
        is_active: true,
        settings: {},
        training_examples: [],
        statistics: {
          total_tasks: 0,
          successful_tasks: 0,
          failed_tasks: 0,
          avg_completion_time_ms: 0,
        },
      })
      .select()
      .single()

    if (error) {
      console.error('Error creating agent:', error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    await supabase.from('system_logs').insert({
      level: 'info',
      message: 'Agent created',
      context: 'agents',
      user_id: user.id,
      agent_id: agent.id,
      metadata: { name: validated.name, role: validated.role },
    })

    return NextResponse.json({ agent }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation error', details: error.errors },
        { status: 400 }
      )
    }

    console.error('Unexpected error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
