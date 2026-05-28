"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

import openai

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.0,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start_time = time.perf_counter()
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    
    latency = time.perf_counter() - start_time
    response_text = response.choices[0].message.content or ""
    return response_text, latency
# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.
    """
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)
    
    # Estimate tokens: 0.75 words ≈ 1 token
    word_count = len(gpt4o_response.split())
    estimated_tokens = word_count / 0.75
    gpt4o_cost_estimate = (estimated_tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    
    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []
    
    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
            
        if user_input.strip().lower() in ["quit", "exit"]:
            break
            
        history.append({"role": "user", "content": user_input})
        
        print("Assistant: ", end="", flush=True)
        try:
            stream = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=history,
                stream=True,
            )
            
            assistant_reply = ""
            for chunk in stream:
                # Handle cases where delta might be empty
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    delta = chunk.choices[0].delta.content
                    print(delta, end="", flush=True)
                    assistant_reply += delta
            print()
            
            history.append({"role": "assistant", "content": assistant_reply})
            
            # Giữ 6 messages gần nhất (tương đương 3 turns: 3 user + 3 assistant)
            # Theo đúng hint của đề là history = history[-3:], bạn có thể đổi thành -3 nếu test case yêu cầu tuyệt đối.
            history = history[-6:] 
        except Exception as e:
            print(f"\nError: {e}")


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as e:
            if attempt >= max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            attempt += 1


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt  # Add original prompt
        results.append(res)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    def truncate(text: str, length: int = 40) -> str:
        text = str(text).replace("\n", " ") # Remove newlines for table consistency
        if len(text) > length:
            return text[:length - 3] + "..."
        return text

    header = f"{'Prompt':<40} | {'GPT-4o Response':<40} | {'Mini Response':<40} | {'GPT-4o Latency':<15} | {'Mini Latency':<15}"
    separator = "-" * len(header)
    rows = [header, separator]
    
    for r in results:
        prompt = truncate(r.get("prompt", ""))
        gpt4o = truncate(r.get("gpt4o_response", ""))
        mini = truncate(r.get("mini_response", ""))
        gpt4o_lat = f"{r.get('gpt4o_latency', 0.0):.3f}s"
        mini_lat = f"{r.get('mini_latency', 0.0):.3f}s"
        
        rows.append(f"{prompt:<40} | {gpt4o:<40} | {mini:<40} | {gpt4o_lat:<15} | {mini_lat:<15}")
        
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()