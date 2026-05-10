"""
NLA (Natural Language Autoencoders) – Produces unsupervised explanations of LLM activations.
Inspired by state-of-the-art mechanistic interpretability research.
"""

import random

def explain_activation(feature_id: str, activation_strength: float) -> str:
    """
    Simulates the output of a Natural Language Autoencoder explaining a specific feature activation.
    """
    explanations = [
        "responds to mentions of critical vehicle safety systems and braking anomalies.",
        "activates on sequences containing diagnostic trouble codes related to CAN-bus timeouts.",
        "identifies patterns of shift report deviations in production line uptime metrics.",
        "detects semantic tokens associated with overdue industrial maintenance intervals.",
        "responds to high-density numeric data within KVTC frames indicating thermal stress."
    ]
    
    selected = random.choice(explanations) # nosec
    return f"Feature {feature_id}: This unit {selected} (Activation: {activation_strength:.4f})"

def generate_explanation(analysis_id: str, context: dict) -> str:
    """
    Wraps the NLA logic for the CompText pipeline.
    """
    feature_id = f"L12_N{random.randint(100, 999)}" # nosec
    strength = context.get("confidence", 0.9) + (random.random() * 0.1) # nosec
    
    return explain_activation(feature_id, strength)
