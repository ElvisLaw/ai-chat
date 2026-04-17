from src.ai_chat.conversation import ChatService, InMemoryConversationStore


class FakeStreamingClient:
    def stream_message(self, messages: list[dict], **kwargs):
        yield "hello"
        yield " world"


def test_stream_persists_full_response_after_iteration() -> None:
    store = InMemoryConversationStore()
    service = ChatService(store=store, llm_client_factory=lambda provider: FakeStreamingClient())

    generator, conversation_id = service.stream(message="hi")
    chunks = list(generator)
    conversation = store.get(conversation_id)

    assert chunks == ["hello", " world"]
    assert conversation is not None
    assert conversation.messages[-1].role.value == "assistant"
    assert conversation.messages[-1].content == "hello world"