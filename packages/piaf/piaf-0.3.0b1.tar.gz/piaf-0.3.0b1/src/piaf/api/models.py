# coding: utf-8
"""
The :mod:`piaf.api.models` contains all `pydantic` models used to describe input and output data.
"""
from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field, conlist, validator

from piaf.agent import AgentState
from piaf.audit import Event, EventRecord, Topic
from piaf.comm import AID, ACLMessage, Performative
from piaf.service import AgentCreationDescription, AMSAgentDescription


class AgentCreationDescriptionModel(BaseModel):
    """
    Describe an incoming agent description.

    It should be supplied by the user in order to create an invoke an agent into a platform. The model contains four fields:

    - class_name: the fully qualified name of the agent's type
    - agent_name: the shortname of the agent to create
    - args: Optional, a sequence of arguments used to instantiate the agent
    - is_service: Default `True`, tells if the agent has a full access to the platform
    """

    class_name: str = Field(description="The fully qualified agent's class name")
    agent_name: str = Field(description="The desired shortname of the agent")
    args: Optional[List[Any]] = Field(
        default=None,
        description="A list of arguments passed to the agent's constructor",
    )
    is_service: bool = Field(
        default=True, description="Tell if the agent is a service or not"
    )

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {
            "example": {
                "class_name": "custom.agents.MyCustomAgent",
                "agent_name": "Custom-1",
                "args": ["a-star", 3],
                "is_service": False,
            }
        }

    def to_agent_creation_description(self) -> AgentCreationDescription:
        """
        Convert the model into an :class:`AgentCreationDescription`.

        :return: the agent creation description
        """
        return AgentCreationDescription(
            class_name=self.class_name,
            agent_name=self.agent_name,
            args=self.args,
            is_service=self.is_service,
        )


class AIDModel(BaseModel):
    """
    Describe an agent identifier.

    The model contains four fields:

    - name: the full name of the agent, including the platform's name
    - addresses: a list of addresses used to reach the agent
    - resolvers: a list of naming resolvers
    """

    name: str = Field(
        description="The full name of the agent (format: shortname@ptf_name)",
        regex=r".*@.*",
    )
    addresses: conlist(str, unique_items=True) = Field(  # type: ignore
        default=[],
        description="A set of addresses with which the agent can be reached.",
    )
    resolvers: conlist(AIDModel, unique_items=True) = Field(  # type: ignore
        default=[],
        description="A set of agents that can resolve this agent's name.",
    )

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {
            "example": {
                "name": "Custom-1@my-awesome-platform",
                "addresses": ["amqp://my-awesome-platform/acc"],
                "resolvers": [
                    {
                        "name": "ams@my-awesome-platform",
                        "addresses": ["amqp://my-awesome-platform/acc"],
                        "resolvers": [],
                    }
                ],
            }
        }

    def to_aid(self) -> AID:
        return AID(self.name, self.addresses, [r.to_aid() for r in self.resolvers])


AIDModel.update_forward_refs()


class AMSAgentDescriptionModel(BaseModel):
    """
    Describe an agent when requested using the AMS.

    The model contains three fields:

    - aid: the agent's identifier
    - state: the state of the agent
    - owner: an optional owner of the agent
    """

    aid: AIDModel = Field(description="The AID of the described agent.")
    state: AgentState = Field(description="The state of the agent.")
    owner: Optional[str] = Field(default=None, description="The owner of the agent.")

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {
            "example": {
                "aid": {
                    "name": "Custom-1@my-awesome-platform",
                    "addresses": [],
                    "resolvers": [],
                },
                "state": "active",
                "owner": None,
            }
        }


class ExceptionModel(BaseModel):
    """
    Describe an internal error to give clues about what went wrong.

    The model contains one field named `detail`, which describes the error.
    """

    detail: str = Field(
        description="An explanation text describing why the error happened."
    )

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {"example": {"detail": "Unknown platform 'my-awesome-platform'"}}


class AgentStateModel(BaseModel):
    """
    Describe the state of an agent.

    It contains one field named `state` which must be either ACTIVE or SUSPENDED.
    """

    state: AgentState = Field("The state of the agent.")

    @validator("state")
    def restrict_state_values(cls, v):
        """
        Ensure the given value is either `AgentState.ACTIVE` or `AgentState.SUSPENDED`.

        :param cls: model class
        :param v: the value of the 'state' field
        :return: `v` if the value is valid
        :raise ValueError: v is not valid
        """
        if v not in (AgentState.ACTIVE, AgentState.SUSPENDED):
            raise ValueError("Must be either ACTIVE or SUSPENDED")
        return v

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {"example": {"state": "ACTIVE"}}


class ACLMessageModel(BaseModel):
    """
    Describe an ACLMessage.

    It contains four fields:

    - `receivers`: a non-empty list of :class:`AIDModel` objects
    - `performative`: the message's performative
    - `conversation_id`: an optional conversation ID to track the conversation
    - `content`: a JSON-serializable message's content

    """

    receivers: conlist(AIDModel, min_items=1, unique_items=True) = Field(  # type: ignore
        description="A set of AIDs, each one being the identity of a recipient."
    )
    performative: Union[Performative, str] = Field(
        description="The performative of the message."
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="A unique conversation ID shared by messages inside a conversation.",
    )
    content: Any = Field(
        description="The message's content, which must be a JSON-compatible one."
    )

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {
            "example": {
                "receivers": [
                    {
                        "name": "Custom-2@my-awesome-platform",
                        "addresses": [],
                        "resolvers": [],
                    }
                ],
                "performative": "request",
                "conversation_id": "talk#3",
                "content": {"title": "Hello!", "repeat": 3},
            }
        }

    def to_acl_message(self, sender: AID) -> ACLMessage:
        return (
            ACLMessage.Builder()
            .performative(self.performative)
            .receiver([r.to_aid() for r in self.receivers])
            .conversation_id(
                self.conversation_id
                if self.conversation_id is not None
                else str(uuid4())
            )
            .content(self.content)
            .build()
        )


class AgentMemoryModel(BaseModel):
    """
    The response model used when the client asks for a snapshot of an agent's memory.

    This model contains two fields:

    - `target`, which is the AID of the targeted agent
    - `memory`, which contains the memory snapshot
    """

    target: AIDModel
    memory: Dict[str, Any]

    class Config:
        """Extra configuration added to the model."""

        schema_extra = {
            "example": {
                "target": {
                    "name": "ams@localhost",
                    "shortname": "ams",
                    "addresses": [],
                    "resolvers": [],
                },
                "memory": {
                    "CLEANUP_DELAY": 1,
                    "CREATE_AGENT_FUNC": "create_agent",
                    "MODIFY_FUNC": "modify",
                    "SEARCH_FUNC": "search",
                    "aid": {
                        "name": "ams@localhost",
                        "shortname": "ams",
                        "addresses": [],
                        "resolvers": [],
                    },
                    "state": "ACTIVE",
                },
            }
        }


#: A type that represents all JSON-compatible types
JSONType = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]


def serialize_piaf_object(
    o: Any,
) -> JSONType:
    """
    Given a `piaf` object, convert it into a JSON-compatible object.

    :param o: the piaf object to serialize
    :return: a JSON-compatible object
    :raise TypeError: the object can't be serialized
    """
    if isinstance(o, AID):
        return {
            "name": o.name,
            "shortname": o.short_name,
            "addresses": o.addresses,
            "resolvers": [serialize_piaf_object(r) for r in o.resolvers],
        }
    if isinstance(o, Enum):
        return o.name
    if isinstance(o, AMSAgentDescription):
        return {
            "aid": serialize_piaf_object(o.name),
            "state": serialize_piaf_object(o.state),
            "owner": o.ownership,
        }
    if isinstance(o, EventRecord):
        return {
            "event": serialize_piaf_object(o.event),
            "topics": [serialize_piaf_object(topic) for topic in o.topics],
            "timestamp": o.timestamp,
        }
    if isinstance(o, Event):
        return {
            "source": o.source,
            "type": o.type,
            "data": json.loads(json.dumps(o.data, default=serialize_piaf_object)),
        }
    if isinstance(o, Topic):
        return str(o)
    if isinstance(o, ACLMessage):
        return {
            k: json.loads(json.dumps(v, default=serialize_piaf_object))
            for k, v in o.__dict__.items()
        }
    return f"Unserializable object: {type(o)}"
