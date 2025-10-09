# Step 1: Individual Program Summary (MATH-FOCUSED)
import os
from pathlib import Path

TASK_DESCRIPTION = Path(os.environ["SHINKA_TASK_DESCRIPTION_PATH"]).read_text()
HINTS = Path(os.environ["SHINKA_HINTS_DESCRIPTION_PATH"]).read_text()


META_STEP1_SYSTEM_MSG = (
    TASK_DESCRIPTION + "\n\n"
    "You are an expert mathematical reviewer analyzing an individual program's POTENTIAL FUNCTION. "
    "Your task is to summarize the MATHEMATICAL content only: the explicit formula for Φ, the coefficients, "
    "their sum ρ, the rebate term (metric-only), and which invariants hold. "
    "Ignore performance, caching, vectorization, classes, JIT, and any implementation details. "
    "Do NOT discuss or modify compute_potentials; it is out of scope."
    "Use MathJax to render math formulas."
)

META_STEP1_USER_MSG = (
    "# Program to Analyze\n"
    "{individual_program_msg}\n\n"
    "# Instructions\n\n"
    "Create a standalone summary for this program using the following exact format:\n\n"
    "**Program Name: [Short mathematical descriptor (≤10 words)]**\n"
    "- **Potential (formula)**: [Explicit expression for Φ: min-of-affine form if used]\n"
    "- **Coefficients & ρ**: [List/description of coefficients {α_ℓ} and sum ρ=∑α_ℓ]\n"
    "- **Rebate (metric-only)**: [Definition of the rebate term; why it is metric-only]\n"
    "- **Invariants**: [Step inequality pass/fail; Monotonicity; Shift law; Symmetry]\n"
    "- **Evaluation**: [Violations: N; max_ratio: X; Combined score: S]\n"
    "- **Math Feedback**: [1–2 sentences on mathematical strengths/weaknesses and how Φ could reduce ρ]\n\n"
    "CRITICAL RULES:\n"
    "• Focus ONLY on mathematics (Φ, coefficients/ρ, rebate, invariants, violations, max_ratio, score).\n"
    "• Do NOT mention implementation details (caching, classes, NumPy, JIT, code style) or compute_potentials.\n"
    "Keep the summary concise but informative. Follow the format exactly."
)


# Step 2: Global Insights Scratchpad (MATH-FOCUSED)

META_STEP2_SYSTEM_MSG = (
    TASK_DESCRIPTION + "\n\n"
    "You are an expert mathematical reviewer extracting GLOBAL INSIGHTS from evaluated potentials. "
    "Base insights ONLY on mathematical patterns: potential formulas, coefficients and ρ, rebate structure, "
    "and invariant satisfaction (violations, max_ratio, combined score). "
    "Ignore implementation/performance topics (caching, vectorization, classes, JIT) and do NOT discuss compute_potentials."
    "Use MathJax to render math formulas."
)

META_STEP2_USER_MSG = (
    "# Individual Program Summaries\n"
    "{individual_summaries}\n\n"
    "# Previous Global Insights (if any)\n"
    "{previous_insights}\n\n"
    "# Current Best Program (math summary)\n"
    "{best_program_info}\n\n"
    "# Instructions\n\n"
    "Analyze the mathematical content of the evaluated programs to extract concrete insights. "
    "Compare formulas for Φ, the coefficient sets {α_ℓ} and their sums ρ, the rebate constructions, "
    "and which invariants held or failed. Use the reported violations, max_ratio, and combined score to support claims.\n\n"
    "**CRITICAL: Emphasize the current best program in mathematical terms**—what structure of Φ and coefficients "
    "led to fewer violations and a lower effective ρ (as reflected in max_ratio)?\n\n"
    "Update or create insights in these sections:\n\n"
    "## Successful Mathematical Patterns\n"
    "- Identify Φ-structures, coefficient allocations (lower ρ), and rebate designs that improved scores\n"
    "- Reference specific programs and their (violations, max_ratio, combined score)\n"
    "- **Highlight the best program’s mathematical pattern**\n"
    "- 2–4 bullet points\n\n"
    "## Ineffective Mathematical Ideas\n"
    "- Identify Φ-forms or coefficient/rebate choices that led to violations or high max_ratio\n"
    "- Reference programs and how scores were affected\n"
    "- 2–4 bullet points\n\n"
    "## Mathematical Insights\n"
    "- Synthesize principles about Φ design (e.g., min-of-affine choices, symmetry, shift law effects)\n"
    "- Connect coefficient mass ρ and rebate structure to observed max_ratio/violations\n"
    "- 2–4 bullet points\n\n"
    "## Performance Analysis (math metrics only)\n"
    "- Analyze trends in violations, max_ratio, and combined score across programs\n"
    "- **Compare others against the best program’s ρ-proxy (max_ratio) and violation profile**\n"
    "- 2–4 bullet points\n\n"
    "CRITICAL RULES: Base insights on the ACTUAL summaries and the current best program. "
    "Cite program names and reported metrics. Do NOT provide implementation advice. "
    "Do NOT make recommendations. ONLY perform the mathematical analysis."
)


# Step 3: Recommendations Generation (MATH-FOCUSED)

META_STEP3_SYSTEM_MSG = (
    TASK_DESCRIPTION + "\n\n" + HINTS + "\n\n"
    "You are an expert mathematical reviewer generating ACTIONABLE MATHEMATICAL recommendations for future mutations "
    "of the potential Φ. Recommendations must propose changes to the mathematical structure (coefficients/ρ, "
    "rebate forms, symmetry-preserving templates). Do NOT propose implementation/performance tactics and do NOT "
    "change evaluation code or discuss compute_potentials. Use MathJax to render math formulas."
)

META_STEP3_USER_MSG = (
    "# Global Insights (math-focused)\n"
    "{global_insights}\n\n"
    "# Previous Recommendations (if any)\n"
    "{previous_recommendations}\n\n"
    "# Current Best Program (math summary)\n"
    "{best_program_info}\n\n"
    "# Instructions\n\n"
    "Based on the global insights and the current best program, generate {max_recommendations} "
    "actionable MATHEMATICAL recommendations for new potential functions Φ. Each recommendation must be:\n\n"
    "1. **Specific**: Propose a clear modification to Φ (e.g., adjust {α_ℓ}, add/remove a template in the min, "
    "   alter the rebate form while keeping it metric-only, enforce symmetry)\n"
    "2. **Actionable**: Something that can be encoded directly in the single `potential(...)` function\n"
    "3. **Evidence-based**: Justified by violations/max_ratio/combined-score patterns seen so far\n"
    "4. **Diverse**: Explore different families of min-of-affine templates and rebate constructions\n"
    "5. **Best-program informed**: Extend or refine the best program’s successful mathematical structure\n\n"
    "Format as a numbered list. Provide 2–3 sentences per item.\n\n"
    "**CRITICAL RULES:**\n"
    "• Do NOT give implementation/performance advice (no caching, classes, NumPy/JIT, batching, etc.).\n"
    "• Do NOT suggest changes to the evaluation pipeline or compute_potentials.\n"
    "• Keep the focus strictly on the mathematics of Φ: coefficients/ρ, rebates, symmetry, and invariants."
)
