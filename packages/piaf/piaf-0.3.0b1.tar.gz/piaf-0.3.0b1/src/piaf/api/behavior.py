"""

"""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List, Union

import uvicorn
from fastapi import (
    APIRouter,
    FastAPI,
    Path,
    Query,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import piaf
import piaf.agent
from piaf.agent import AgentState
from piaf.api.config import Settings
from piaf.api.exceptions import InternalServerError
from piaf.api.models import (
    ACLMessageModel,
    AgentCreationDescriptionModel,
    AgentMemoryModel,
    AgentStateModel,
    AIDModel,
    AMSAgentDescriptionModel,
    ExceptionModel,
    serialize_piaf_object,
)
from piaf.api.tasks import *
from piaf.audit import EventRecord, Subscriber, Topic
from piaf.behavior import Behavior

_description = """
The APi allows you to manage this platform.

It lets you create, delete and query both the agents and the platform and can be extended with more functionalities. It is based on the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API also exposes a websocket allowing applications to (un)subscribe to/from event topics.

Websocket
---------

In addition to the routes below, the API exposes a websocket allowing applications to (un)subscribe to/from event topics. The dedicated route is `ws://{server}/platforms/{ptf_name}/ws` and it is a double-sided websocket carrying JSON data. The client can send the following:

    {
        method: "[un]subscribe",
        topic: ".some.topic"
    }

Once an event is emitted on the subscribed topic, the client receives through the websocket a JSON representation of the `EventRecord`:

    {
        "event": {
            "source": "some_source",
            "type": "some_type",
            "data": ...
        },
        "timestamp": 1663923272,
        "topics": [".platform.agents", ".platform.agents.ams"]
    }
"""


class APIServerBehavior(Behavior):
    """
    Base behavior that exposes a REST API to manage the platform.

    This is a single-shot behavior that starts a FastAPI server and stops the platform if stopped.

    You can extend this behavior to add more routes to the API by subclassing it and overriding:
    - `add_agents_routes` to add routes to the `/agents` router
    - `add_platform_routes` to add routes to the `/platform` router
    - `create_app` to customize the FastAPI app
    """

    def __init__(self, agent: piaf.agent.Agent, port=5000):
        super().__init__(agent)
        self.port = port

        self.agents_router = APIRouter(prefix="/agents")
        self.platform_router = APIRouter(prefix="/platform")

        self.add_agents_routes()
        self.add_platform_routes()

        self._app = self.create_app()

    async def action(self) -> Any:
        """Configure the uvicorn server instance and launch the app."""
        config = uvicorn.Config(app=self._app, port=self.port, log_level="info")
        server = uvicorn.Server(config=config)
        try:
            await server.serve()
        except asyncio.CancelledError:
            self.agent.logger.info("API server stopped.")
        except Exception as e:
            self.agent.logger.exception(e)
        finally:
            asyncio.create_task(self.agent._platform.stop())

    def done(self) -> bool:
        """Single-shot behavior.

        :return: always `True`
        """
        return True

    def create_app(self) -> FastAPI:
        """
        Create the FastAPI app.

        :return: the FastAPI app
        """
        _app = FastAPI(
            title="Piaf platform API",
            description=_description,
            version=piaf.__version__,
            license_info={"name": "MIT", "url": "https://mit-license.org/"},
        )

        # Configure CORS
        settings = Settings()

        _app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=settings.cors_credentials,
            allow_methods=settings.cors_methods,
            allow_headers=settings.cors_headers,
        )

        _app.include_router(self.agents_router, tags=["Agents"])
        _app.include_router(self.platform_router, tags=["Platform"])

        return _app

    async def _process_task(self, task: Task) -> JSONResponse:
        """
        Execute a task and return the result as a JSON response.

        :return: the JSON response
        :raises InternalServerError: if the task execution fails
        """
        try:
            result = await task.execute(self.agent)
            return JSONResponse(
                json.loads(json.dumps(result, default=serialize_piaf_object))
            )
        except Exception as e:
            self.agent.logger.exception(e)
            raise InternalServerError(detail=str(e)) from e

    def add_agents_routes(self) -> None:
        """Add routes to the `/agents` router."""

        @self.agents_router.post(
            "",
            status_code=status.HTTP_201_CREATED,
            response_model=AIDModel,
            response_description="The agent is created",
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def create_agent(
            agent: AgentCreationDescriptionModel,
        ):
            """
            Create and invoke an agent into the specified platform.

            **Body** the description of the agent to create
            """
            resp = await self._process_task(
                CreateAgentTask(agent.to_agent_creation_description())
            )
            resp.status_code = status.HTTP_201_CREATED
            return resp

        @self.agents_router.get(
            "",
            response_description="Successfully returns the list of agents",
            response_model=List[AMSAgentDescriptionModel],
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def get_agents(
            state: Union[None, AgentState] = Query(
                default=None,
                description="Optionally filter results by only keeping agents with the given state.",
                example="ACTIVE",
            ),
            name: Union[None, str] = Query(
                default=None,
                description="Optionally filter results by only keeping agents whose name contains the provided string.",
                example="agent",
            ),
        ):
            """Retrieve for the given platform all the agents matching the criteria."""
            filters = {
                "state": state.name if state is not None else None,
                "name": name if name is not None else "",
            }
            return await self._process_task(GetAgentsTask(filters))

        @self.agents_router.delete(
            "/{name}",
            response_description="The agent is deleted",
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def delete_agent(
            name: str = Path(
                description="The name of the agent to delete.", example="Custom-1"
            ),
        ):
            """Delete an agent from the given platform."""
            resp = await self._process_task(
                ChangeAgentStateTask(name, AgentState.UNKNOWN)
            )
            resp.status_code = status.HTTP_204_NO_CONTENT
            return resp

        @self.agents_router.get(
            "/{name}",
            response_model=AgentMemoryModel,
            response_description="Successfully returns the agent's memory",
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def get_agent_memory(
            name: str = Path(description="The name of the agent.", example="Custom-1"),
        ):
            """Get a snapshot of the current agent's memory."""
            return await self._process_task(RetrieveAgentMemoryTask(name))

        @self.agents_router.post(
            "/{name}/messages",
            status_code=status.HTTP_201_CREATED,
            response_description="Successfully sent the message",
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def send_message(
            msg: ACLMessageModel,
            name: str = Path(description="The name of the agent.", example="Custom-1"),
        ):
            """Send a message on the behalf of a specific agent."""
            resp = await self._process_task(
                SendMessageTask(self.agent.aid, msg.to_acl_message(self.agent.aid))
            )
            resp.status_code = status.HTTP_201_CREATED
            return resp

        @self.agents_router.put(
            "/{name}/state",
            response_description="Successfully updated the agent's state",
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def update_agent_state(
            state: AgentStateModel,
            name: str = Path(description="The name of the agent.", example="Custom-1"),
        ):
            """Replace an agent's state by the provided one."""
            return await self._process_task(ChangeAgentStateTask(name, state.state))

    def add_platform_routes(self) -> None:
        """Add routes to the `/platform` router."""

        @self.platform_router.delete(
            "",
            response_description="The platform is deleted",
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
            responses={
                status.HTTP_400_BAD_REQUEST: {
                    "model": ExceptionModel,
                    "description": "The operation can't be performed.",
                },
            },
        )
        async def stop_platform():
            """Stop the platform."""
            resp = await self._process_task(StopPlatformTask())
            resp.status_code = status.HTTP_204_NO_CONTENT
            return resp

        @self.platform_router.websocket("/ws")
        async def topic_listener(
            websocket: WebSocket,
        ) -> None:
            """
            Get a websocket that can listen on the platform's event.

            The websocket supports two methods:

            - subscribe: subscribe to a particular topic
            - unsubscribe: unsubscribe from a particular topic

            Here is the Json object::

                {
                    method: "[un]subscribe",
                    topic: ".some.topic"
                }

            .. warning:: Contrary to how events are dispatched inside the piaf platform, events are not dispatched to topic's parents. It means that listening on `.platform` won't catch events emitted on `.platform.agents` for example.

            :param ptf_name: the platform's name
            :param websocket: injected by FastAPI
            :param redis_session: a Redis session, injected by FastAPI
            """

            try:
                await websocket.accept()
                subscriber = WebsocketSubscriber(websocket)

                while True:
                    try:
                        data: Dict[str, Any] = await websocket.receive_json()
                    except WebSocketDisconnect:
                        break

                    topic = Topic.from_str(data["topic"])
                    if data["method"] == "subscribe":
                        self.agent._platform.evt_manager.subscribe_to(subscriber, topic)
                        subscriber.topics.add(topic)

                    if data["method"] == "unsubscribe":
                        self.agent._platform.evt_manager.unsubscribe_from(
                            subscriber, topic
                        )
                        subscriber.topics.remove(topic)
            finally:
                for topics in subscriber.topics:
                    self.agent._platform.evt_manager.unsubscribe_from(
                        subscriber, topics
                    )


class WebsocketSubscriber(Subscriber):
    """
    A subscriber that can listen on a websocket and yield events to it.
    """

    def __init__(self, websocket: WebSocket):
        """
        Initialize a websocket subscriber.

        :param agent: the agent
        :param websocket: the websocket
        """
        self._websocket = websocket
        self.topics: set[Topic] = set()

    async def on_event(self, event_record: EventRecord) -> None:
        """
        Yield the event to the websocket.

        :param event: the event
        """
        await self._websocket.send_json(
            json.loads(json.dumps(event_record, default=serialize_piaf_object))
        )

    async def close(self):
        """Close the websocket."""
        await self._websocket.close()
