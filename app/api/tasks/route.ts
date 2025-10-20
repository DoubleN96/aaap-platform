import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { z } from 'zod'

const CreateTaskSchema = z.object({
  instruction: z.string().min(10, 'Instruction must be at least 10 characters'),
  agent_id: z.string().uuid().optional(),
  priority: z.number().min(1).max(10).optional(),
  requires_approval: z.boolean().optional(),
  scheduled_at: z.string().datetime().optional(),
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

    const searchParams = request.nextUrl.searchParams
    const status = searchParams.get('status')
    const agent_id = searchParams.get('agent_id')

    let query = supabase
      .from('tasks')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })

    if (status) {
      query = query.eq('status', status)
    }

    if (agent_id) {
      query = query.eq('agent_id', agent_id)
    }

    const { data, error } = await query

    if (error) {
      console.error('Error fetching tasks:', error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ tasks: data })
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
    const validated = CreateTaskSchema.parse(body)

    // Call AI Engine to parse instruction
    const aiEngineUrl = process.env.NEXT_PUBLIC_AI_ENGINE_URL || 'http://localhost:8000'

    const parseResponse = await fetch(`${aiEngineUrl}/ai/parse-instruction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        instruction: validated.instruction,
        user_id: user.id,
        agent_id: validated.agent_id,
      }),
    })

    if (!parseResponse.ok) {
      throw new Error('Failed to parse instruction')
    }

    const parsedIntent = await parseResponse.json()

    // Generate execution plan
    const planResponse = await fetch(`${aiEngineUrl}/ai/generate-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        instruction: validated.instruction,
        user_id: user.id,
        context: { parsed_intent: parsedIntent },
      }),
    })

    if (!planResponse.ok) {
      throw new Error('Failed to generate execution plan')
    }

    const executionPlan = await planResponse.json()

    // Create task in database
    const { data: task, error } = await supabase
      .from('tasks')
      .insert({
        user_id: user.id,
        agent_id: validated.agent_id || null,
        instruction: validated.instruction,
        parsed_intent: parsedIntent,
        execution_plan: executionPlan,
        status: validated.requires_approval ? 'requires_approval' : 'pending',
        requires_approval: validated.requires_approval || false,
        priority: validated.priority || 5,
        scheduled_at: validated.scheduled_at || null,
        metadata: {},
      })
      .select()
      .single()

    if (error) {
      console.error('Error creating task:', error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    // Log creation
    await supabase.from('system_logs').insert({
      level: 'info',
      message: 'Task created',
      context: 'tasks',
      user_id: user.id,
      task_id: task.id,
      metadata: { instruction: validated.instruction },
    })

    return NextResponse.json({ task }, { status: 201 })
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
