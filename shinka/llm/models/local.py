import logging

import backoff
import openai

from .result import QueryResult

logger = logging.getLogger(__name__)


def backoff_handler(details):
    exc = details.get("exception")
    if exc:
        logger.warning(
            f"Local vLLM - Retry {details['tries']} due to error: {exc}. Waiting {details['wait']:0.1f}s..."
        )


@backoff.on_exception(
    backoff.expo,
    (
        openai.APIConnectionError,
        openai.APIStatusError,
        openai.RateLimitError,
        openai.APITimeoutError,
    ),
    max_tries=5,
    max_value=10,
    on_backoff=backoff_handler,
)
def query_local(
    client,
    model: str,
    msg: str,
    system_msg: str,
    msg_history,
    output_model,
    model_posteriors=None,
    **kwargs,
) -> QueryResult:
    """Query a locally hosted vLLM server using the OpenAI compatible API."""
    if output_model is not None:
        raise NotImplementedError("Structured output not supported for local vLLM.")

    new_msg_history = msg_history + [{"role": "user", "content": msg}]
    call_kwargs = kwargs.copy()
    if "max_output_tokens" in call_kwargs and "max_tokens" not in call_kwargs:
        max_model_len = call_kwargs.pop("max_output_tokens")
        sum_context_len = sum(len(x["content"]) for x in new_msg_history)
        call_kwargs["max_tokens"] = int(max_model_len - sum_context_len / 1.5)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            *new_msg_history,
        ],
        **call_kwargs,
    )

    content = response.choices[0].message.content
    thought = getattr(response.choices[0].message, "reasoning_content", "") or ""

    new_msg_history.append({"role": "assistant", "content": content})

    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0

    return QueryResult(
        content=content,
        msg=msg,
        system_msg=system_msg,
        new_msg_history=new_msg_history,
        model_name=model,
        kwargs=call_kwargs,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=0.0,
        input_cost=0.0,
        output_cost=0.0,
        thought=thought,
        model_posteriors=model_posteriors,
    )
