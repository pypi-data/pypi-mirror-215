import json
import logging
import time
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Optional, Generator, Any, cast

import anthropic  # type: ignore
import openai

from . import api_support
from .errors import TemplateNotFoundError, APIKeyMissingError, AuthorizationError, FreeplayError

JsonDom = dict[str, Any]

logger = logging.getLogger(__name__)
default_tag = 'latest'


@dataclass
class CompletionResponse:
    content: str
    is_complete: bool


@dataclass
class PromptTemplate:
    name: str
    content: str


@dataclass
class PromptTemplateWithMetadata:
    project_version_id: str
    prompt_template_id: str
    name: str
    content: str


@dataclass
class PromptTemplates:
    templates: list[PromptTemplateWithMetadata]


@dataclass
class CompletionChunk:
    text: str
    is_complete: bool


class Flavor(ABC):
    @property
    @abstractmethod
    def record_format_type(self) -> str:
        raise NotImplementedError()

    @property
    def _model_params_with_defaults(self) -> dict[str, str]:
        return {}

    @abstractmethod
    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        pass

    @abstractmethod
    def call_service(self, formatted_prompt: str, **kwargs: str) -> Optional[CompletionResponse]:
        pass

    @abstractmethod
    def call_service_stream(self, formatted_prompt: str, **kwargs: str) -> Generator[CompletionChunk, None, None]:
        pass

    def _get_model_params(self, **kwargs: str) -> dict[str, str]:
        model_params = {}
        for parameter_key, default_value in self._model_params_with_defaults.items():
            if parameter_key in kwargs:
                model_params[parameter_key] = kwargs[parameter_key]
            else:
                model_params[parameter_key] = default_value
        return model_params


class OpenAI(Flavor, ABC):
    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__()
        if openai_api_base:
            openai.api_base = openai_api_base

        if not openai_api_key or not openai_api_key.strip():
            raise APIKeyMissingError("OpenAI API key not set. It must be set to make calls to the service.")

        openai.api_key = openai_api_key


class OpenAIText(OpenAI):
    record_format_type = "openai_text"
    _model_params_with_defaults = {
        "model": "text-davinci-003"
    }

    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__(openai_api_key, openai_api_base)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        return prompt_template.content.format(**variables)

    def call_service(self, formatted_prompt: str, **kwargs: str) -> Optional[CompletionResponse]:
        completion = openai.Completion.create(
            prompt=formatted_prompt,
            **self._get_model_params(**kwargs)
        )  # type: ignore
        return CompletionResponse(
            content=completion.choices[0].text,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            **kwargs: str
    ) -> Generator[CompletionChunk, None, None]:
        completion = openai.Completion.create(
            prompt=formatted_prompt,
            stream=True,
            **self._get_model_params(**kwargs)
        )  # type: ignore

        for chunk in completion:
            yield CompletionChunk(
                text=chunk.choices[0].text,
                is_complete=chunk.choices[0].finish_reason == "stop"
            )


class OpenAIChat(OpenAI):
    record_format_type = "openai_chat"
    _model_params_with_defaults = {
        "model": "gpt-3.5-turbo"
    }

    def __init__(self, openai_api_key: str, openai_api_base: Optional[str] = None):
        super().__init__(openai_api_key, openai_api_base)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        # Extract messages JSON to enable formatting of individual content fields of each message. If we do not
        # extract the JSON, current variable interpolation will fail on JSON curly braces.
        messages_as_json = json.loads(prompt_template.content)
        formatted_messages = [
            {"content": message['content'].format(**variables), "role": message['role']} for message in
            messages_as_json]
        return json.dumps(formatted_messages)

    def call_service(self, formatted_prompt: str, **kwargs: str) -> Optional[CompletionResponse]:
        messages = json.loads(formatted_prompt)
        completion = openai.ChatCompletion.create(
            messages=messages,
            **self._get_model_params(**kwargs)
        )  # type: ignore
        return CompletionResponse(
            content=completion.choices[0].message.content,
            is_complete=completion.choices[0].finish_reason == "stop"
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            **kwargs: str
    ) -> Generator[CompletionChunk, None, None]:
        messages = json.loads(formatted_prompt)
        completion = openai.ChatCompletion.create(
            messages=messages,
            stream=True,
            **self._get_model_params(**kwargs)
        )  # type: ignore
        for chunk in completion:
            # Not all chunks have a "content" field -- if they don't, keep chunking.
            yield CompletionChunk(
                text=chunk.choices[0].delta.get('content', ""),
                is_complete=chunk.choices[0].finish_reason == "stop"
            )


class AnthropicClaudeText(Flavor):
    record_format_type = "anthropic_text"
    _model_params_with_defaults = {
        "model": "claude-v1",
        "max_tokens_to_sample": "100"
    }

    def __init__(self, anthropic_api_key: str):
        self.client = anthropic.Client(anthropic_api_key)

    def format(self, prompt_template: PromptTemplateWithMetadata, variables: dict[str, str]) -> str:
        interpolated_prompt = prompt_template.content.format(**variables)
        # Anthropic expects a specific Chat format "Human: $PROMPT_TEXT\n\nAssistant:". We add the wrapping for Text.
        chat_formatted_prompt = f"{anthropic.HUMAN_PROMPT} {interpolated_prompt} {anthropic.AI_PROMPT}"
        return chat_formatted_prompt

    def call_service(self, formatted_prompt: str, **kwargs: str) -> Optional[CompletionResponse]:
        anthropic_response = self.client.completion(
            prompt=formatted_prompt,
            **self._get_model_params(**kwargs)
        )
        return CompletionResponse(
            content=anthropic_response['completion'],
            is_complete=anthropic_response['stop_reason'] == 'stop_sequence'
        )

    def call_service_stream(
            self,
            formatted_prompt: str,
            **kwargs: str
    ) -> Generator[CompletionChunk, None, None]:
        anthropic_response = self.client.completion_stream(
            prompt=formatted_prompt,
            **self._get_model_params(**kwargs)
        )

        # Yield incremental text completions. Claude returns the full text output in every chunk.
        # We want to predictably return a stream like we do for OpenAI.
        prev_chunk = ''
        for chunk in anthropic_response:
            if len(prev_chunk) != 0:
                incremental_new_text = chunk['completion'].split(prev_chunk)[1]
            else:
                incremental_new_text = chunk['completion']

            prev_chunk = chunk['completion']
            yield CompletionChunk(
                text=incremental_new_text,
                is_complete=chunk['stop_reason'] == 'stop_sequence'
            )


class CallSupport:
    def __init__(
            self,
            flavor: Flavor,
            freeplay_api_key: str,
            api_base: str,
            **kwargs: str
    ) -> None:
        self.api_base = api_base
        self.freeplay_api_key = freeplay_api_key
        self.flavor = flavor
        self.extra_init_args = kwargs

    def create_session(self, project_id: str, tag: str, test_run_id: Optional[str] = None) -> JsonDom:
        request_body = {'test_run_id': test_run_id} if test_run_id is not None else None
        response = api_support.post_raw(api_key=self.freeplay_api_key,
                                        url=f'{self.api_base}/projects/{project_id}/sessions/tag/{tag}',
                                        payload=request_body)

        if response.status_code == 201:
            return cast(dict[str, Any], json.loads(response.content))
        elif response.status_code == 401:
            raise AuthorizationError()
        else:
            raise FreeplayError(f'Unknown response while creating a session. Response code: {response.status_code}')

    def get_prompts(self, project_id: str, tag: str) -> PromptTemplates:
        prompts = api_support.get(
            target_type=PromptTemplates,
            api_key=self.freeplay_api_key,
            url=f'{self.api_base}/projects/{project_id}/templates/all/{tag}'
        )
        return prompts

    def prepare_and_make_call(
            self,
            session_id: str,
            prompts: PromptTemplates,
            template_name: str,
            variables: dict[str, str],
            tag: str,
            test_run_id: Optional[str] = None
    ) -> Optional[CompletionResponse]:
        # format prompt
        templates = [t for t in prompts.templates if t.name == template_name]
        if len(templates) == 0:
            raise TemplateNotFoundError(f'Could not find template with name "{template_name}"')
        target_template = templates[0]
        formatted_prompt = self.flavor.format(target_template, variables)

        # make call
        start = int(time.time())
        try:
            completion_response = self.flavor.call_service(formatted_prompt=formatted_prompt, **self.extra_init_args)
        except Exception as e:
            raise FreeplayError("Error calling service") from e
        end = int(time.time())

        return_content = completion_response.content if completion_response else ""
        is_complete = completion_response.is_complete if completion_response else False

        # record data
        self.__record_call(
            return_content,
            is_complete,
            end,
            formatted_prompt,
            session_id,
            start,
            target_template,
            variables,
            tag,
            test_run_id
        )

        return completion_response

    def prepare_and_make_call_stream(
            self,
            session_id: str,
            prompts: PromptTemplates,
            template_name: str,
            variables: dict[str, str],
            tag: str,
            test_run_id: Optional[str] = None
    ) -> Generator[CompletionChunk, None, None]:
        # format prompt
        templates = [t for t in prompts.templates if t.name == template_name]
        if len(templates) == 0:
            raise TemplateNotFoundError(f'Could not find template with name "{template_name}"')
        target_template = templates[0]
        formatted_prompt = self.flavor.format(target_template, variables)

        # make call
        start = int(time.time())
        completion_response = self.flavor.call_service_stream(formatted_prompt=formatted_prompt,
                                                              **self.extra_init_args)
        text_chunks = []
        last_is_complete = False
        for chunk in completion_response:
            text_chunks.append(chunk.text)
            last_is_complete = chunk.is_complete
            yield chunk
        end = int(time.time())

        self.__record_call(''.join(text_chunks),
                           last_is_complete,
                           end,
                           formatted_prompt,
                           session_id,
                           start,
                           target_template,
                           variables,
                           tag,
                           test_run_id)

    def __record_call(
            self,
            completion_content: str,
            completion_is_complete: bool,
            end: int,
            formatted_prompt: str,
            session_id: str,
            start: int,
            target_template: PromptTemplateWithMetadata,
            variables: dict[str, str],
            tag: str,
            test_run_id: Optional[str]
    ) -> None:

        record_payload = {
            "session_id": session_id,
            "project_version_id": target_template.project_version_id,
            "prompt_template_id": target_template.prompt_template_id,
            "start_time": start,
            "end_time": end,
            "tag": tag,
            "inputs": variables,
            "prompt_content": formatted_prompt,
            "return_content": completion_content,
            "format_type": self.flavor.record_format_type,
            "is_complete": completion_is_complete
        }

        if test_run_id is not None:
            record_payload['test_run_id'] = test_run_id

        try:
            recorded_response = api_support.post_raw(
                api_key=self.freeplay_api_key,
                url=f'{self.api_base}/v1/record',
                payload=record_payload
            )
            recorded_response.raise_for_status()
        except Exception as e:
            status_code = -1
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                status_code = e.response.status_code
            logger.warning(f'There was an error recording to Freeplay. Call will not be logged. '
                           f'Status: {status_code}. {e.__class__}')


class Session:
    def __init__(
            self,
            call_support: CallSupport,
            session_id: str,
            prompts: PromptTemplates,
            tag: str = default_tag,
            test_run_id: Optional[str] = None
    ) -> None:
        self.tag = tag
        self.call_support = call_support
        self.session_id = session_id
        self.prompts = prompts
        self.test_run_id = test_run_id

    def get_completion(
            self,
            template_name: str,
            variables: dict[str, str]
    ) -> Optional[CompletionResponse]:
        return self.call_support.prepare_and_make_call(self.session_id,
                                                       self.prompts,
                                                       template_name,
                                                       variables,
                                                       self.tag,
                                                       self.test_run_id)

    def get_completion_stream(
            self,
            template_name: str,
            variables: dict[str, str]
    ) -> Generator[CompletionChunk, None, None]:
        return self.call_support.prepare_and_make_call_stream(self.session_id,
                                                              self.prompts,
                                                              template_name,
                                                              variables,
                                                              self.tag,
                                                              self.test_run_id)


@dataclass()
class FreeplayTestRun:
    def __init__(
            self,
            call_support: CallSupport,
            test_run_id: str,
            inputs: list[dict[str, str]]
    ):
        self.call_support = call_support
        self.test_run_id = test_run_id
        self.inputs = inputs

    def get_inputs(self) -> list[dict[str, str]]:
        return self.inputs

    def create_session(self, project_id: str, tag: str = default_tag) -> Session:
        project_session = self.call_support.create_session(project_id, tag, self.test_run_id)
        prompts = self.call_support.get_prompts(project_id, tag)
        return Session(self.call_support, project_session['session_id'], prompts, tag, self.test_run_id)


# This SDK prototype does not support full functionality of either OpenAI's API or Freeplay's
# The simplifications are:
#  - Always assumes there is a single choice returned, does not support multiple
#  - Does not support an "escape hatch" to allow use of features we don't explicitly expose
class Freeplay:
    def __init__(
            self,
            flavor: Flavor,
            freeplay_api_key: str,
            api_base: str,
            **kwargs: str
    ) -> None:
        if not freeplay_api_key or not freeplay_api_key.strip():
            raise APIKeyMissingError("Freeplay API key not set. It must be set to the Freeplay API.")

        self.call_support = CallSupport(flavor, freeplay_api_key, api_base, **kwargs)
        self.freeplay_api_key = freeplay_api_key
        self.api_base = api_base

    def create_session(self, project_id: str, tag: str = default_tag) -> Session:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)
        return Session(self.call_support, project_session['session_id'], prompts, tag)

    def get_completion(
            self,
            project_id: str,
            template_name: str,
            variables: dict[str, str],
            tag: str = default_tag
    ) -> Optional[CompletionResponse]:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)

        return self.call_support.prepare_and_make_call(project_session['session_id'],
                                                       prompts,
                                                       template_name,
                                                       variables,
                                                       tag)

    def get_completion_stream(
            self,
            project_id: str,
            template_name: str,
            variables: dict[str, str],
            tag: str = default_tag
    ) -> Generator[CompletionChunk, None, None]:
        project_session = self.call_support.create_session(project_id, tag)
        prompts = self.call_support.get_prompts(project_id, tag)

        return self.call_support.prepare_and_make_call_stream(project_session['session_id'],
                                                              prompts,
                                                              template_name,
                                                              variables,
                                                              tag)

    def create_test_run(self, project_id: str, playlist: str) -> FreeplayTestRun:
        response = api_support.post_raw(
            api_key=self.freeplay_api_key,
            url=f'{self.api_base}/projects/{project_id}/test-runs',
            payload={'playlist_name': playlist},
        )

        json_dom = response.json()

        return FreeplayTestRun(self.call_support, json_dom['test_run_id'], json_dom['inputs'])
