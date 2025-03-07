# prompt_templates.py

ELEVATOR_PITCH_PROMPT = """
You are an expert startup strategist specializing in crafting compelling elevator pitches.

Generate a persuasive elevator pitch for a startup named "{startup_name}".

Details:
- **Business Model**: {business_model}
- **Competitive Advantages**: {competitive_advantages}
- **Tone**: {tone}

### Requirements:
1. The pitch should be concise (under 75 words).
2. Clearly convey the startup's value proposition.
3. Make it engaging and persuasive.
4. Ensure it resonates with potential investors or customers.

### Format:
- A compelling opening hook.
- A strong one-liner about what the startup does.
- A clear explanation of the value proposition.
- A closing statement that leaves an impact.

RESPOND ONLY WITH THE ELEVATOR PITCH AND NO OTHER TEXT.
"""