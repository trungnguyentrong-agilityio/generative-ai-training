from typing import Any, Union
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.messages import BaseMessage, get_buffer_string, trim_messages, HumanMessage


class ConversationMemory(BaseChatMemory):
    """
    A memory class that stores the conversation history.
    """

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:
    k: int = 5 # number of messages to keep in the memory

    @property
    def buffer(self) -> Union[str, list[BaseMessage]]:
        """String buffer of memory."""
        return self.buffer_as_messages if self.return_messages else self.buffer_as_str

    @property
    def buffer_as_str(self) -> str:
        """Exposes the buffer as a string in case return_messages is False."""
        return get_buffer_string(
            self.buffer_as_messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    @property
    def buffer_as_messages(self) -> list[BaseMessage]:
        """Exposes the buffer as a list of messages in case return_messages is True."""
        return trim_messages(
            self.chat_memory.messages,
            token_counter=len,
            max_tokens=self.k,
            strategy="last",
            start_on=HumanMessage,
            include_system=True,
        )

    @property
    def memory_variables(self) -> list[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}
