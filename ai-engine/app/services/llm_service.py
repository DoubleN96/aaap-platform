"""
LLM Service - Handles all AI/LLM operations
"""

import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from anthropic import Anthropic

class LLMService:
    """Service for interacting with Language Models"""

    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None

        if self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
        else:
            self.anthropic_client = None

    async def parse_instruction(
        self,
        instruction: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Parse natural language instruction into structured data

        Args:
            instruction: User's natural language instruction
            user_context: Additional context about the user

        Returns:
            Structured intent with action, entities, and metadata
        """

        system_prompt = """Eres un asistente experto en analizar instrucciones en lenguaje natural para automatización de tareas.

Tu trabajo es analizar la instrucción del usuario y extraer:
1. La acción principal a realizar
2. Entidades relevantes (emails, fechas, nombres, etc.)
3. Capacidades requeridas (email, calendar, crm, etc.)
4. Nivel de confianza en tu análisis

Responde SOLO en formato JSON válido con esta estructura:
{
  "action": "acción principal",
  "entities": {
    "clave": "valor"
  },
  "confidence": 0.95,
  "capabilities_required": ["capability1", "capability2"],
  "suggested_agent_role": "email_assistant|crm_manager|scheduler|analyst"
}"""

        user_prompt = f"""Analiza esta instrucción:

"{instruction}"

Contexto adicional: {user_context or 'N/A'}"""

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )

                import json
                result = json.loads(response.choices[0].message.content)
                return result

            else:
                # Fallback to rule-based parsing
                return self._fallback_parse(instruction)

        except Exception as e:
            print(f"Error parsing instruction: {e}")
            return self._fallback_parse(instruction)

    async def generate_execution_plan(
        self,
        instruction: str,
        parsed_intent: Dict[str, Any],
        available_capabilities: List[str]
    ) -> Dict[str, Any]:
        """
        Generate a detailed execution plan with steps

        Args:
            instruction: Original instruction
            parsed_intent: Parsed intent from parse_instruction
            available_capabilities: Available capabilities/integrations

        Returns:
            Execution plan with steps
        """

        system_prompt = """Eres un planificador experto de automatización de tareas.

Tu trabajo es generar un plan de ejecución detallado con pasos concretos.

Cada paso debe tener:
- step_index: número del paso
- step_name: nombre descriptivo
- step_type: tipo (data_retrieval, data_transform, api_call, condition, approval)
- action: acción específica a realizar
- parameters: parámetros necesarios
- dependencies: índices de pasos previos necesarios

Responde en formato JSON válido."""

        user_prompt = f"""Genera un plan de ejecución para:

Instrucción: "{instruction}"

Intent analizado:
{parsed_intent}

Capacidades disponibles: {available_capabilities}

El plan debe ser ejecutable paso a paso."""

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )

                import json
                result = json.loads(response.choices[0].message.content)
                return result

            else:
                return self._fallback_plan(parsed_intent)

        except Exception as e:
            print(f"Error generating plan: {e}")
            return self._fallback_plan(parsed_intent)

    async def suggest_clarifications(
        self,
        instruction: str,
        parsed_intent: Dict[str, Any]
    ) -> List[str]:
        """
        Suggest clarifying questions if instruction is ambiguous

        Returns:
            List of questions to ask the user
        """

        if parsed_intent.get("confidence", 1.0) < 0.7:
            return [
                "¿Puedes especificar más detalles sobre esta tarea?",
                "¿Cuál es el resultado esperado?"
            ]

        return []

    def _fallback_parse(self, instruction: str) -> Dict[str, Any]:
        """Fallback rule-based parsing when LLM is not available"""

        instruction_lower = instruction.lower()

        # Simple rule-based classification
        if any(word in instruction_lower for word in ["email", "correo", "enviar", "responder"]):
            return {
                "action": "email_operation",
                "entities": {},
                "confidence": 0.6,
                "capabilities_required": ["email"],
                "suggested_agent_role": "email_assistant"
            }
        elif any(word in instruction_lower for word in ["reunión", "meeting", "agendar", "calendario"]):
            return {
                "action": "calendar_operation",
                "entities": {},
                "confidence": 0.6,
                "capabilities_required": ["calendar"],
                "suggested_agent_role": "scheduler"
            }
        elif any(word in instruction_lower for word in ["crm", "contacto", "lead", "cliente"]):
            return {
                "action": "crm_operation",
                "entities": {},
                "confidence": 0.6,
                "capabilities_required": ["crm"],
                "suggested_agent_role": "crm_manager"
            }
        else:
            return {
                "action": "unknown",
                "entities": {},
                "confidence": 0.3,
                "capabilities_required": [],
                "suggested_agent_role": None
            }

    def _fallback_plan(self, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback plan generation"""

        return {
            "steps": [
                {
                    "step_index": 0,
                    "step_name": "Execute task",
                    "step_type": "api_call",
                    "action": parsed_intent.get("action", "unknown"),
                    "parameters": parsed_intent.get("entities", {}),
                    "dependencies": []
                }
            ],
            "total_steps": 1,
            "estimated_duration_ms": 3000,
            "requires_approval": True
        }


# Singleton instance
llm_service = LLMService()
