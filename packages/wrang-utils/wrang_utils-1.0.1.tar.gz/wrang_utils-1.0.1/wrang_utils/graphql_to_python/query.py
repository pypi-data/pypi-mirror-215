"""
Utils for interacting with graphql objects
"""

import copy
import importlib
import json
import os
from dataclasses import Field, dataclass, fields, is_dataclass
from typing import (
    Any,
    AsyncIterable,
    Awaitable,
    Dict,
    ForwardRef,
    Iterable,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_origin,
)
from uuid import UUID

import graphql
import requests
from aiohttp import ClientSession
from dataclasses_json import DataClassJsonMixin

from graphql_to_python.utils.aws import clean_dynamodb_data
from graphql_to_python.utils.generic import camel_to_snake, snake_to_camel

QueryFieldInput = Union[str, Tuple[str, List[str]]]

T = TypeVar("T", bound="GraphqlObject")

GRAPHQL_ENDPOINT = os.environ.get("API_WRANGLED_GRAPHQL_ENDPOINT", "")
GRAPHQL_API_KEY = os.environ.get("API_WRANGLED_API_KEY", "")


def remove_nested_nones(data: Dict[str, Any], remove_nested: bool = True) -> Dict[str, Any]:
    """
    Remove nested None values from a dictionary
    """
    cleaned_dict = {}

    for key, value in data.items():
        if value is None:
            continue

        if isinstance(value, dict):
            if remove_nested:
                continue
            cleaned_dict[key] = remove_nested_nones(value, remove_nested=remove_nested)
        elif isinstance(value, list):
            cleaned_dict[key] = []
            for item in value:
                if isinstance(item, dict):
                    if remove_nested:
                        continue
                    temp_value = remove_nested_nones(item, remove_nested=remove_nested)
                else:
                    temp_value = item

                cleaned_dict[key].append(temp_value)
        else:
            cleaned_dict[key] = value
    return cleaned_dict


@dataclass
class GraphqlObject(DataClassJsonMixin):
    @classmethod
    def iterate_items(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_function: str = None,
        query_input_name: str = None,
        debug: bool = False,
        shallow: bool = False,
        fail_on_item: bool = True,
        **kwargs,
    ) -> Iterable[T]:
        """
        Iterate over all items in a graphql query
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        cleaned_args = remove_nested_nones(kwargs, remove_nested=False)
        index_arguments = [snake_to_camel(key) for key in cleaned_args.keys()]

        query_name, query_node = form_graphql_from_graphql_object(
            cls,
            query_type="list",
            query_function=query_function,
            query_input_name=query_input_name,
            index_args=index_arguments,
            shallow=shallow,
        )

        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {
            "query": query,
            "variables": {snake_to_camel(key): value for key, value in kwargs.items()},
        }

        next_token = True
        while next_token:
            query_return = execute_graphql_query(json_data, url=url, api_key=api_key)

            errors = query_return.get("errors")
            if errors:
                raise Exception(errors)

            data = query_return.get("data", {}).get(query_name, {})
            if not data:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            for item in data.get("items", []):
                try:
                    yield cls.from_dict(deserialize_graphql_return(item))
                except ValueError as e:
                    print(f"Failed to parse {item}")
                    if fail_on_item:
                        raise e
                except Exception as e:
                    print(f"Failed to parse {item}")
                    if fail_on_item:
                        raise e

            next_token = data.get("nextToken")
            json_data["variables"]["nextToken"] = next_token

    @classmethod
    async def async_iterate_items(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_function: str = None,
        query_input_name: str = None,
        debug: bool = False,
        shallow: bool = False,
        fail_on_item: bool = True,
        session: ClientSession = None,
        **kwargs,
    ) -> AsyncIterable[T]:
        """
        Iterate over all items in a graphql query asynchronously
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        cleaned_args = remove_nested_nones(kwargs, remove_nested=False)
        index_arguments = [snake_to_camel(key) for key in cleaned_args.keys()]

        query_name, query_node = form_graphql_from_graphql_object(
            cls,
            query_type="list",
            query_function=query_function,
            query_input_name=query_input_name,
            index_args=index_arguments,
            shallow=shallow,
        )

        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {
            "query": query,
            "variables": {snake_to_camel(key): value for key, value in kwargs.items()},
        }

        next_token = True
        while next_token:
            query_return: dict = await async_execute_graphql_query(
                json_data, url=url, api_key=api_key, session=session
            )

            errors = query_return.get("errors")
            if errors:
                raise Exception(errors)

            data = query_return.get("data", {}).get(query_name, {})
            if not data:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            for item in data.get("items", []):
                try:
                    yield cls.from_dict(deserialize_graphql_return(item))
                except ValueError as e:
                    print(f"Failed to parse {item}")
                    if fail_on_item:
                        raise e
                except Exception as e:
                    print(f"Failed to parse {item}")
                    if fail_on_item:
                        raise e

            next_token = data.get("nextToken")
            json_data["variables"]["nextToken"] = next_token

    @classmethod
    def list_items(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_fields: Iterable[QueryFieldInput] = None,
        debug: bool = False,
        shallow: bool = False,
    ) -> Iterable[T]:
        """
        Queries graphql endpoint and returns list of 'object'
        """

        return cls.iterate_items(
            url=url,
            api_key=api_key,
            query_fields=query_fields,
            debug=debug,
            shallow=shallow,
        )

    @classmethod
    async def async_list_items(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_fields: Iterable[QueryFieldInput] = None,
        debug: bool = False,
        shallow: bool = False,
        session: ClientSession = None,
    ) -> AsyncIterable[T]:
        """
        Queries graphql endpoint and returns list of 'object'
        """

        async for item in cls.async_iterate_items(
            url=url,
            api_key=api_key,
            query_fields=query_fields,
            debug=debug,
            shallow=shallow,
            session=session,
        ):
            yield item

    @classmethod
    def get_entry(
        cls: Type[T],
        object_id: UUID,
        url: str = None,
        api_key: str = None,
        debug: bool = False,
        shallow=False,
    ) -> T:
        """
        Gets an entry in the graphql endpoint
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        query_name, query_node = form_graphql_from_graphql_object(
            cls, query_type="get", shallow=shallow
        )

        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {"query": query, "variables": {"id": str(object_id)}}
        query_return = execute_graphql_query(json_data, url=url, api_key=api_key)

        errors = query_return.get("errors")
        if errors is None:
            data = query_return.get("data", {}).get(query_name)
            if data is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            return cls.from_dict(
                deserialize_graphql_return(query_return.get("data", {}).get(query_name, {}))
            )
        else:
            raise Exception(errors)

    @classmethod
    async def async_get_entry(
        cls: Type[T],
        object_id: UUID,
        url: str = None,
        api_key: str = None,
        debug: bool = False,
        shallow=False,
        session: ClientSession = None,
    ) -> T:
        """
        Gets an entry in the graphql endpoint
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        query_name, query_node = form_graphql_from_graphql_object(
            cls, query_type="get", shallow=shallow
        )

        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {"query": query, "variables": {"id": str(object_id)}}
        query_return: dict = await async_execute_graphql_query(
            json_data, url=url, api_key=api_key, session=session
        )

        errors = query_return.get("errors")
        if errors is None:
            data = query_return.get("data", {}).get(query_name)
            if data is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            return cls.from_dict(
                deserialize_graphql_return(query_return.get("data", {}).get(query_name, {}))
            )
        else:
            raise Exception(errors)

    @classmethod
    def fetch_by_index(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_function: str = None,
        query_input_name: str = None,
        debug: bool = False,
        shallow: bool = False,
        **kwargs,
    ) -> Iterable[T]:
        """
        Fetches object by index
        """
        return cls.iterate_items(
            url=url,
            api_key=api_key,
            query_function=query_function,
            query_input_name=query_input_name,
            debug=debug,
            shallow=shallow,
            **kwargs,
        )

    @classmethod
    async def async_fetch_by_index(
        cls: Type[T],
        url: str = None,
        api_key: str = None,
        query_function: str = None,
        query_input_name: str = None,
        debug: bool = False,
        shallow: bool = False,
        session: ClientSession = None,
        **kwargs,
    ) -> AsyncIterable[T]:
        """
        Fetches object by index
        """
        async for item in cls.async_iterate_items(
            url=url,
            api_key=api_key,
            query_function=query_function,
            query_input_name=query_input_name,
            debug=debug,
            shallow=shallow,
            session=session,
            **kwargs,
        ):
            yield item

    def get_query_input(self: T, remove_nested=True) -> Dict[str, Any]:
        """
        Fetches object's fields and returns a dict of the form {field_name: field_value}
        """
        # simple way to format to camelCase
        data: Dict[str, Any] = json.loads(self.to_json())
        return remove_nested_nones(data, remove_nested=remove_nested)

    def change_entry(
        self: T,
        change_type: str,
        url: str = None,
        api_key: str = None,
        debug: bool = False,
        remove_nested: bool = True,
        shallow: bool = False,
        variables: Optional[Dict[str, Any]] = None,
    ) -> T:
        """
        Changes an entry in the graphql endpoint
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        var_input = self.get_query_input(remove_nested=remove_nested)

        query_name, query_node = form_graphql_from_graphql_object(
            self.__class__, query_type=change_type, shallow=shallow
        )
        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        if variables is None:
            variables = {"input": var_input}

        json_data = {"query": query, "variables": variables}

        if debug:
            print(json.dumps(json_data, indent=4))

        query_return = execute_graphql_query(json_data, url=url, api_key=api_key)
        errors = query_return.get("errors")
        if errors is None:
            item = query_return.get("data", {}).get(query_name)
            if item is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            return self.__class__.from_dict(deserialize_graphql_return(item))

        raise Exception(errors)

    async def async_change_entry(
        self: T,
        change_type: str,
        url: str = None,
        api_key: str = None,
        debug: bool = False,
        remove_nested: bool = True,
        shallow: bool = False,
        session: ClientSession = None,
    ) -> T:
        """
        Changes an entry in the graphql endpoint asynchronously
        """
        if not url:
            url = GRAPHQL_ENDPOINT
        if not api_key:
            api_key = GRAPHQL_API_KEY
        var_input = self.get_query_input(remove_nested=remove_nested)

        query_name, query_node = form_graphql_from_graphql_object(
            self.__class__, query_type=change_type, shallow=shallow
        )
        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        variables = {"input": var_input}
        json_data = {"query": query, "variables": variables}

        if debug:
            print(json.dumps(json_data, indent=4))

        query_return: dict = await async_execute_graphql_query(
            json_data, url=url, api_key=api_key, session=session
        )
        errors = query_return.get("errors")
        if errors is None:
            item = query_return.get("data", {}).get(query_name)
            if item is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            return self.__class__.from_dict(deserialize_graphql_return(item))

        raise Exception(errors)

    def create_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
    ) -> T:
        """
        Creates a new entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self, nested=not remove_nested)
        new_graphql_object: T = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        # if hasattr(new_graphql_object, "id_value"):
        #     new_graphql_object.id_value = None

        return new_graphql_object.change_entry(
            "create",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
        )

    async def async_create_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
        session: ClientSession = None,
    ) -> T:
        """
        Creates a new entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self, nested=not remove_nested)
        new_graphql_object: T = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        # if hasattr(new_graphql_object, "id_value"):
        #     new_graphql_object.id_value = None

        return await new_graphql_object.async_change_entry(
            "create",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
            session=session,
        )

    def update_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
    ) -> T:
        """
        Updates an entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self, nested=not remove_nested)
        new_graphql_object: T = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        return new_graphql_object.change_entry(
            "update",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
        )

    async def async_update_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
        session: ClientSession = None,
    ) -> T:
        """
        Updates an entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self, nested=not remove_nested)
        new_graphql_object: T = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        return await new_graphql_object.async_change_entry(
            "update",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
            session=session,
        )

    def delete_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
    ) -> T:
        """
        Updates an entry in the graphql endpoint
        """
        if not hasattr(self, "id_value"):
            raise Exception("id_value not found in object")

        new_graphql_object: T = self.__class__(id_value=self.id_value)

        return new_graphql_object.change_entry(
            "delete",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
        )

    async def async_delete_entry(
        self: T,
        url: str = None,
        api_key: str = None,
        remove_nested: bool = True,
        debug: bool = False,
        shallow: bool = False,
        session: ClientSession = None,
    ) -> T:
        """
        Updates an entry in the graphql endpoint
        """
        if not hasattr(self, "id_value"):
            raise Exception("id_value not found in object")

        new_graphql_object: T = self.__class__(id_value=self.id_value)

        return await new_graphql_object.async_change_entry(
            "delete",
            url=url,
            api_key=api_key,
            debug=debug,
            remove_nested=remove_nested,
            shallow=shallow,
            session=session,
        )

    @classmethod
    def from_dynamo_event_record(cls: Type[T], record: Dict[str, Any]) -> Union[T, Tuple[T, T]]:
        """
        Returns a graphql object from a dynamo record
        """
        event_type: str = record["eventName"]
        if event_type == "INSERT":
            return cls.from_dict(clean_dynamodb_data(record["dynamodb"]["NewImage"]))
        elif event_type == "MODIFY":
            return (
                cls.from_dict(clean_dynamodb_data(record["dynamodb"]["NewImage"])),
                cls.from_dict(clean_dynamodb_data(record["dynamodb"]["OldImage"])),
            )

    @classmethod
    def items_needed(cls: Type[T]) -> List[str]:
        return []


def remove_nested_items_needed(
    node: GraphqlObject, nested: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Returns a nested dictionary from a graphql object, removing fields with items_needed
    """
    cleaned_dict = {}
    for item in fields(node):
        item_value = getattr(node, item.name)
        if item.name in node.items_needed():
            continue
        if is_dataclass(item.type):
            if nested:
                nested_return = remove_nested_items_needed(item_value)
                if nested_return:
                    cleaned_dict[item.name] = nested_return
        else:
            cleaned_dict[item.name] = item_value

    return cleaned_dict


class IsDataclass(Protocol):
    # as already noted in comments, checking for this attribute is currently
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: Dict


def clean_dataclass_field(item: Field) -> str:
    """
    Returns a cleaned field name for a dataclass field
    """
    filter_function = item.metadata.get("dataclasses_json", {}).get(
        "letter_case", lambda x: snake_to_camel(x)
    )

    return filter_function(item.name)


def _resolve_field_type(item_type: Type) -> Type:
    """
    Recursively step through field types to get a base type
    """
    if get_origin(item_type) is Union or get_origin(item_type) is list:
        return _resolve_field_type(item_type.__args__[0])

    if isinstance(item_type, ForwardRef):
        return _resolve_field_type(item_type.__forward_arg__)

    if isinstance(item_type, str):
        try:
            return eval(item_type)
        except NameError:
            print("could not resolve type", item_type)

    return item_type


def resolve_check_fields(cls: GraphqlObject) -> Iterable[QueryFieldInput]:
    """
    Get list of fields in a nested fashion from dataclasses
    """
    class_fields = fields(cls)

    for item in class_fields:
        nested_field_type = _resolve_field_type(item.type)

        if is_dataclass(nested_field_type):
            yield clean_dataclass_field(item), [
                item for item in resolve_check_fields(nested_field_type)
            ]
        else:
            yield clean_dataclass_field(item)


PYTHON_TYPE_TO_GQL_TYPE = {
    "str": "ModelStringKeyConditionInput",
    "int": "ModelIntKeyConditionInput",
    "float": "ModelFloatKeyConditionInput",
    "datetime": "ModelStringKeyConditionInput",
}


def form_index_arguments(
    cls: GraphqlObject, index_args: Dict[str, Any], first_arg_required: bool = True
) -> List[QueryFieldInput]:
    """
    Returns a list of fields needed for an index
    """
    first_arg = index_args[0]

    first_arg_variable_type = graphql.language.NamedTypeNode(
        name=graphql.language.NameNode(value="String")
    )
    if first_arg_required:
        first_arg_variable_type = graphql.language.NonNullTypeNode(
            type=graphql.language.NamedTypeNode(name=graphql.language.NameNode(value="String"))
        )

    # index primary keys have to be a string
    variable_definitions = [
        graphql.language.VariableDefinitionNode(
            variable=graphql.language.VariableNode(name=graphql.language.NameNode(value=first_arg)),
            type=first_arg_variable_type,
        )
    ]
    arguments = [
        graphql.language.ArgumentNode(
            name=graphql.language.NameNode(value=first_arg),
            value=graphql.language.VariableNode(name=graphql.language.NameNode(value=first_arg)),
        )
    ]

    arg_mappings = {
        snake_to_camel(item.name): PYTHON_TYPE_TO_GQL_TYPE.get(
            getattr(_resolve_field_type(item.type), "__name__", ""), "String"
        )
        for item in fields(cls)
    }

    for arg in index_args[1:]:
        variable_definitions.append(
            graphql.language.VariableDefinitionNode(
                variable=graphql.language.VariableNode(name=graphql.language.NameNode(value=arg)),
                type=graphql.language.NamedTypeNode(
                    name=graphql.language.NameNode(value=arg_mappings.get(arg, "String"))
                ),
            )
        )

        arguments.append(
            graphql.language.ArgumentNode(
                name=graphql.language.NameNode(value=arg),
                value=graphql.language.VariableNode(name=graphql.language.NameNode(value=arg)),
            )
        )

    return variable_definitions, arguments


def form_graphql_from_graphql_object(
    cls: GraphqlObject,
    query_type: str,
    query_function: str = None,
    query_input_name: str = None,
    index_args: List[str] = None,
    shallow: bool = False,
) -> Tuple[str, graphql.language.OperationDefinitionNode]:
    """
    Returns a fully formed graphql query definition from a graphql object
    """
    if query_type == "list":
        query_function = query_function or (query_type + cls.__name__ + "s")
    else:
        query_function = query_function or (query_type + cls.__name__)

    # TODO: generalize input name for multiple inputs
    query_input_name = query_input_name or query_type.capitalize() + cls.__name__ + "Input"
    if query_type == "get":
        query_name = query_type.capitalize() + cls.__name__ + "Query"
        operation = graphql.language.OperationType.QUERY
        arguments = []
        selection_set = graphql_selection_from_graphql_object(cls, shallow=shallow)
        variable_definitions = [
            graphql.language.VariableDefinitionNode(
                variable=graphql.language.VariableNode(name=graphql.language.NameNode(value="id")),
                type=graphql.language.NonNullTypeNode(
                    type=graphql.language.NamedTypeNode(name=graphql.language.NameNode(value="ID"))
                ),
            ),
        ]
        arguments = [
            graphql.language.ArgumentNode(
                name=graphql.language.NameNode(value="id"),
                value=graphql.language.VariableNode(name=graphql.language.NameNode(value="id")),
            ),
        ]

    elif query_type == "list":
        query_name = query_type.capitalize() + cls.__name__ + "Query"
        operation = graphql.language.OperationType.QUERY

        first_arg_required = False
        if index_args:
            first_arg_required = True
            index_args.append("nextToken")
        else:
            index_args = ["nextToken"]

        variable_definitions, arguments = form_index_arguments(
            cls, index_args, first_arg_required=first_arg_required
        )

        selection_set = graphql.language.SelectionSetNode(
            selections=[
                graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value="items"),
                    arguments=[],
                    directives=[],
                    selection_set=graphql_selection_from_graphql_object(cls, shallow=shallow),
                ),
                graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value="nextToken"),
                    arguments=[],
                    directives=[],
                    selection_set=None,
                ),
            ]
        )
    elif query_type == "create" or query_type == "update" or query_type == "delete":
        query_name = query_type.capitalize() + cls.__name__ + "Mutation"
        operation = graphql.language.OperationType.MUTATION
        variable_definitions = [
            graphql.language.VariableDefinitionNode(
                variable=graphql.language.VariableNode(
                    name=graphql.language.NameNode(value="input")
                ),
                type=graphql.language.NonNullTypeNode(
                    type=graphql.language.NamedTypeNode(
                        name=graphql.language.NameNode(value=query_input_name)
                    )
                ),
            ),
        ]
        arguments = [
            graphql.language.ArgumentNode(
                name=graphql.language.NameNode(value="input"),
                value=graphql.language.VariableNode(name=graphql.language.NameNode(value="input")),
            ),
        ]
        selection_set = graphql_selection_from_graphql_object(cls, shallow=shallow)
    if query_type == "delete":
        selection_set = graphql.language.SelectionSetNode(
            selections=[
                graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value="id"),
                    arguments=[],
                    directives=[],
                    selection_set=None,
                )
            ]
        )

    operation_definition = graphql.language.OperationDefinitionNode(
        name=graphql.language.NameNode(value=query_name),
        operation=operation,
        variable_definitions=variable_definitions,
        selection_set=graphql.language.SelectionSetNode(
            selections=[
                graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value=query_function),
                    arguments=arguments,
                    selection_set=selection_set,
                )
            ]
        ),
    )

    return query_function, operation_definition


def graphql_selection_from_graphql_object(
    cls: GraphqlObject, symbols_seen: Set[str] = None, shallow: bool = False
) -> graphql.SelectionSetNode:
    """
    Form nested query string from a graphql object
    """
    if symbols_seen is None:
        symbols_seen = set()
    else:
        symbols_seen = copy.deepcopy(symbols_seen)

    if cls.__name__ in symbols_seen:
        return None

    if is_dataclass(cls):
        symbols_seen.add(cls.__name__)

    # Here we have to dynamically resolve nested classes that might not be loaded globally
    class_fields = fields(cls)
    module = importlib.import_module(cls.__module__)

    globals().update(
        {n: getattr(module, n) for n in module.__all__}
        if hasattr(module, "__all__")
        else {k: v for (k, v) in module.__dict__.items() if not k.startswith("_")}
    )
    items_needed = cls.items_needed() if hasattr(cls, "items_needed") else []
    selections = []

    for item in class_fields:
        nested_field_type = _resolve_field_type(item.type)
        nested_field_name = clean_dataclass_field(item)

        if is_dataclass(nested_field_type):
            if shallow:
                continue

            nested_selection = graphql_selection_from_graphql_object(
                nested_field_type, symbols_seen=symbols_seen
            )
            # if we've already seen this type, don't add it again
            if nested_selection is None:
                continue

            field_node = graphql.language.FieldNode(
                alias=None,
                name=graphql.language.NameNode(value=nested_field_name),
                arguments=[],
                directives=[],
                selection_set=nested_selection,
            )
            # nested_field_name is transformed to camel case above and doesn't work here
            if item.name in items_needed:
                field_node = graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value=nested_field_name),
                    arguments=[],
                    directives=[],
                    selection_set=graphql.language.SelectionSetNode(
                        selections=[
                            graphql.language.FieldNode(
                                alias=None,
                                name=graphql.language.NameNode(value="items"),
                                arguments=[],
                                directives=[],
                                selection_set=nested_selection,
                            )
                        ]
                    ),
                )
        else:
            field_node = graphql.language.FieldNode(
                alias=None,
                name=graphql.language.NameNode(value=nested_field_name),
                arguments=[],
                directives=[],
                selection_set=None,
            )

        selections.append(field_node)

    return graphql.language.SelectionSetNode(selections=selections)


def deserialize_graphql_return(response_data: Dict[str, Any]) -> Dict[str, Any]:

    if isinstance(response_data, list):
        return [deserialize_graphql_return(item) for item in response_data]

    if not isinstance(response_data, dict):
        return response_data

    if "items" in response_data:
        return deserialize_graphql_return(response_data=response_data["items"])

    return {
        camel_to_snake(key): deserialize_graphql_return(value)
        for key, value in response_data.items()
    }


def execute_graphql_query(
    raw_data: Dict[str, Any], url: str = None, api_key: str = None
) -> Dict[str, Any]:
    """
    execute graphql request
    """
    # print(raw_data)
    if url is None or api_key is None:
        url = "http://localhost:8080/graphql"
        response = requests.post(
            url,
            data=json.dumps(raw_data),
            headers={"Content-Type": "application/json"},
        )
    else:
        response = requests.post(
            url,
            data=json.dumps(raw_data),
            headers={"Content-Type": "application/json", "x-api-key": api_key},
        )
    return response.json()


async def async_execute_graphql_query(
    raw_data: Dict[str, Any], url: str = None, api_key: str = None, session: ClientSession = None
) -> Awaitable[Dict[str, Any]]:
    """
    Execute graphql request asynchronously
    """
    headers = {"Content-Type": "application/json"}
    if url is None or api_key is None:
        url = "http://localhost:8080/graphql"
    else:
        headers["x-api-key"] = api_key

    if session is None:
        async with ClientSession() as session:
            async with session.post(
                url,
                data=json.dumps(raw_data),
                headers=headers,
            ) as response:
                return await response.json()
    else:
        async with session.post(
            url,
            data=json.dumps(raw_data),
            headers=headers,
        ) as response:
            return await response.json()
