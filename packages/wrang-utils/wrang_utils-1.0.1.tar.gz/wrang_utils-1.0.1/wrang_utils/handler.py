# """
# Handler for AWS Lambda events that come from dynamodb change streams.
# """
# import functools
# import logging
# import os
# from collections import defaultdict
# from typing import Any, Dict, Iterable, List, Optional, Protocol, Type, Union, cast

# import sentry_sdk

# from graphql_to_python.query import GraphqlObject

# # We have to load all models so we can dynamically register actions for them
# from taco_utils.models import *  # pylint: disable=unused-wildcard-import,wildcard-import
# from aws_utils import clean_dynamo_data

# GRAPHQL_ENDPOINT = os.environ.get("API_TACOTRADE_GRAPHQLAPI_ENDPOINT", "")
# GRAPHQL_API_KEY = os.environ.get("API_TACOTRADE_GRAPHQL_API_KEY", "")
# BASE_URL = os.environ.get("APEX_BASE_URL", "")

# # in minutes
# USER_PROFILE_TIMEOUT = int(os.environ.get("USER_PROFILE_TIMEOUT", 1440))

# class InsertHandlerFunction(Protocol):
#     """
#     Handler protocol for INSERT events.
#     """

#     def __call__(self, new_graphql_object: GraphqlObject, **kwargs) -> Dict[str, Any]:
#         ...


# class ModifyHandlerFunction(Protocol):
#     """
#     Handler protocol for MODIFY events.
#     """

#     def __call__(
#         self, new_graphql_object: GraphqlObject, old_graphql_object: GraphqlObject, **kwargs
#     ) -> Dict[str, Any]:
#         ...


# class RemoveHandlerFunction(Protocol):
#     """
#     Handler protocol for REMOVE events.
#     """

#     def __call__(self, old_graphql_object: GraphqlObject, **kwargs) -> Dict[str, Any]:
#         ...

# HandlerFunctionType = Union[InsertHandlerFunction, ModifyHandlerFunction, RemoveHandlerFunction]
# ACTIONS_REGISTRY: Dict[str, Dict[str, HandlerFunctionType]] = defaultdict(dict)

# def trigger(model: str, action: str):
#     """
#     Decorator to register actions.
#     """

#     @functools.wraps(model)
#     def decorator(func):
#         ACTIONS_REGISTRY[model][action] = func
#         return func

#     return decorator


# def common_action(
#     graphql_object: GraphqlObject, event: GraphqlObject = None, **kwargs  # pylint: disable=unused-argument
# ) -> Dict[str, Any]:
#     """
#     Common action for all models. Executed if no other action is registered.
#     """
#     if event is None:
#         event = graphql_object
#     logging.info(
#         "Received event for %s",
#         graphql_object.__class__.__name__,
#         extra={"event": graphql_object.to_dict()},
#     )
#     return {}


# # TODO: rewrite to use aws-lambda-powertools-python or just annotated function registry
# def route_gql_event_record(
#     event_record: Dict[str, Any],
#     registry: Dict[str, Dict[str, HandlerFunctionType]],
#     **kwargs,
# ) -> Optional[Dict[str, Any]]:
#     """
#     Choose the function to call based on the event type and GraphQL type.
#     """

#     event_type: str = event_record["eventName"]
#     new_image = event_record.get("dynamodb", {}).get("NewImage")
#     old_image = event_record.get("dynamodb", {}).get("OldImage")

#     new_item = None
#     if new_image is not None:
#         new_item = clean_dynamo_data(new_image)

#     old_item = None
#     if old_image is not None:
#         old_item = clean_dynamo_data(old_image)

#     item_type = None
#     if new_item is not None:
#         item_type = str(new_item.get("__typename"))
#         # If there's an owner field, set that as the user id in sentry
#         sentry_sdk.set_user({"id": new_item.get("owner")})
#     elif old_item is not None:
#         item_type = str(old_item.get("__typename"))
#         sentry_sdk.set_user({"id": old_item.get("owner")})
#     else:
#         logging.warning("No item type found in event")
#         return None

#     function_mappings = registry.get(item_type, {})
#     if not function_mappings:
#         logging.warning("No functions registered for %s", item_type)

#     process_function = function_mappings.get(event_type)
#     if process_function is None:
#         logging.warning("No function registered for %s %s", item_type, event_type)
#         process_function = cast(HandlerFunctionType, common_action)

#     logging.info(
#         "Event: Received %s event for %s", event_type, item_type, extra={"event": event_record}
#     )
#     class_object: Type[GraphqlObject] = eval(item_type)  # pylint: disable=eval-used

#     if new_item is not None:
#         new_class_inst: GraphqlObject = class_object.from_dict(new_item)
#         logging.info(new_class_inst)

#     if old_item is not None:
#         old_class_inst: GraphqlObject = class_object.from_dict(old_item)
#         logging.info(old_class_inst)

#     if event_type == "INSERT":
#         process_function = cast(InsertHandlerFunction, process_function)
#         return process_function(new_class_inst, **kwargs)
#     elif event_type == "MODIFY":
#         process_function = cast(ModifyHandlerFunction, process_function)
#         return process_function(new_class_inst, old_class_inst, **kwargs)
#     elif event_type == "REMOVE":
#         process_function = cast(RemoveHandlerFunction, process_function)
#         return process_function(old_class_inst, **kwargs)

#     # Should never get here
#     logging.warning("We don't handle this case yet.", extra={"event": event_record})

#     return None


# def process_lambda_records(
#     records: List[Dict[str, Any]],
#     registry: Dict[str, Dict[str, HandlerFunctionType]] = None,
#     **kwargs,
# ) -> Iterable[Optional[Dict[str, Any]]]:
#     """
#     Process the records from the lambda event. Passes the kwargs to the handler functions.
#     """
#     if registry is None:
#         registry = ACTIONS_REGISTRY

#     for record in records:
#         yield route_gql_event_record(event_record=record, registry=registry, **kwargs)
