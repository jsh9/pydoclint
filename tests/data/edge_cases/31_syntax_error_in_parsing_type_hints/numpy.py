# Adapted from
# https://github.com/openai/openai-python/blob/a52463c93215a09f9a142e25c975935523d15c10/src/openai/resources/chat/completions/completions.py#L238

def create(
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel],
        audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[Metadata] | NotGiven = NOT_GIVEN,
        modalities: Optional[List[Literal['text', 'audio']]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        prompt_cache_key: str | NotGiven = NOT_GIVEN,
        reasoning_effort: Optional[ReasoningEffort] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        safety_identifier: str | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        service_tier: Optional[Literal['auto', 'default', 'flex', 'scale', 'priority']] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], SequenceNotStr[str], None] | NotGiven = NOT_GIVEN,
        store: Optional[bool] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolUnionParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        verbosity: Optional[Literal['low', 'medium', 'high']] | NotGiven = NOT_GIVEN,
        web_search_options: completion_create_params.WebSearchOptions | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
) -> ChatCompletion:
    """
    Create a model response for the given chat conversation.

    The docstring of the 3rd input arg, `audio`, has a comment "# noqa: LN002".
    For version 0.7.2 or older, this would trigger a false positive DOC105,
    because there would be SyntaxError wen parsing the whole type hint
    (Optional[ChatCompletionAudioParam] | NotGiven, default=NOT_GIVEN  # noqa: LN002)

    In version 0.7.3 or later, this bug is fixed.

    Parameters
    ----------
    messages : Iterable[ChatCompletionMessageParam]
        Placeholder text
    model : Union[str, ChatModel]
        Placeholder text
    audio : Optional[ChatCompletionAudioParam] | NotGiven, default=NOT_GIVEN  # noqa: LN002
        Placeholder text
    frequency_penalty : Optional[float] | NotGiven, default=NOT_GIVEN
        Placeholder text
    function_call : completion_create_params.FunctionCall | NotGiven, default=NOT_GIVEN
        Placeholder text
    functions : Iterable[completion_create_params.Function] | NotGiven, default=NOT_GIVEN
        Placeholder text
    logit_bias : Optional[Dict[str, int]] | NotGiven, default=NOT_GIVEN
        Placeholder text
    logprobs : Optional[bool] | NotGiven, default=NOT_GIVEN
        Placeholder text
    max_completion_tokens : Optional[int] | NotGiven, default=NOT_GIVEN
        Placeholder text
    max_tokens : Optional[int] | NotGiven, default=NOT_GIVEN
        Placeholder text
    metadata : Optional[Metadata] | NotGiven, default=NOT_GIVEN
        Placeholder text
    modalities : Optional[List[Literal["text", "audio"]]] | NotGiven, default=NOT_GIVEN
        Placeholder text
    n : Optional[int] | NotGiven, default=NOT_GIVEN
        Placeholder text
    parallel_tool_calls : bool | NotGiven, default=NOT_GIVEN
        Placeholder text
    prediction : Optional[ChatCompletionPredictionContentParam] | NotGiven, default=NOT_GIVEN
        Placeholder text
    presence_penalty : Optional[float] | NotGiven, default=NOT_GIVEN
        Placeholder text
    prompt_cache_key : str | NotGiven, default=NOT_GIVEN
        Placeholder text
    reasoning_effort : Optional[ReasoningEffort] | NotGiven, default=NOT_GIVEN
        Placeholder text
    response_format : completion_create_params.ResponseFormat | NotGiven, default=NOT_GIVEN
        Placeholder text
    safety_identifier : str | NotGiven, default=NOT_GIVEN
        Placeholder text
    seed : Optional[int] | NotGiven, default=NOT_GIVEN
        Placeholder text
    service_tier : Optional[Literal["auto", "default", "flex", "scale", "priority"]] | NotGiven, default=NOT_GIVEN
        Placeholder text
    stop : Union[Optional[str], SequenceNotStr[str], None] | NotGiven, default=NOT_GIVEN
        Placeholder text
    store : Optional[bool] | NotGiven, default=NOT_GIVEN
        Placeholder text
    stream : Optional[Literal[False]] | NotGiven, default=NOT_GIVEN
        Placeholder text
    stream_options : Optional[ChatCompletionStreamOptionsParam] | NotGiven, default=NOT_GIVEN
        Placeholder text
    temperature : Optional[float] | NotGiven, default=NOT_GIVEN
        Placeholder text
    tool_choice : ChatCompletionToolChoiceOptionParam | NotGiven, default=NOT_GIVEN
        Placeholder text
    tools : Iterable[ChatCompletionToolUnionParam] | NotGiven, default=NOT_GIVEN
        Placeholder text
    top_logprobs : Optional[int] | NotGiven, default=NOT_GIVEN
        Placeholder text
    top_p : Optional[float] | NotGiven, default=NOT_GIVEN
        Placeholder text
    user : str | NotGiven, default=NOT_GIVEN
        Placeholder text
    verbosity : Optional[Literal["low", "medium", "high"]] | NotGiven, default=NOT_GIVEN
        Placeholder text
    web_search_options : completion_create_params.WebSearchOptions | NotGiven, default=NOT_GIVEN
        Placeholder text
    extra_headers : Headers | None, default=None
        Placeholder text
    extra_query : Query | None, default=None
        Placeholder text
    extra_body : Body | None, default=None
        Placeholder text
    timeout : float | httpx.Timeout | None | NotGiven, default=NOT_GIVEN
        Placeholder text

    Returns
    -------
    ChatCompletion
        The chat completion response
    """
    pass
