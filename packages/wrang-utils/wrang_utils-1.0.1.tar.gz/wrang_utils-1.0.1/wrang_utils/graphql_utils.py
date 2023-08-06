"""
Utils for interacting with graphql objects
"""

from dataclasses import Field, dataclass, fields, is_dataclass
from functools import partial
import json
import graphql
import requests
from typing import (
    Callable,
    Iterable,
    NamedTuple,
    Optional,
    Any,
    Dict,
    List,
    Tuple,
    Type,
    Union,
    get_origin,
    TypeVar,
)
from typing_extensions import Protocol

from utils.dynamo_utils import clean_dynamo_data
from utils.python_utils import camel_to_snake, snake_to_camel

QueryFieldInput = Union[str, Tuple[str, List[str]]]

T = TypeVar("T")


class GraphqlType(Protocol):
    # the most reliable way to ascertain that something is a dataclass
    __dataclass_fields__: Dict

    def list_items(
        cls: Type[T],
        url: str,
        api_key: str,
        query_fields: Iterable[QueryFieldInput] = None,
    ) -> Iterable[T]:
        pass

    def change_entry(self, change_type: str, url: str, api_key: str) -> Dict[str, Any]:
        pass

    def create_entry(self, url: str, api_key: str) -> Dict[str, Any]:
        pass

    def update_entry(self, url: str, api_key: str, fields: Dict[str, str]) -> Dict[str, Any]:
        pass

    @classmethod
    def items_needed(cls: Type[T]) -> List[str]:
        pass

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        pass

    def to_json(self) -> str:
        pass

    def to_dict(self) -> Dict[str, Any]:
        pass


Q = TypeVar("Q", bound=GraphqlType)


def remove_nested_nones(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove nested None values from a dictionary
    """
    cleaned_dict = {}

    for key, value in data.items():
        if isinstance(value, dict):
            cleaned_dict[key] = remove_nested_nones(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    cleaned_dict[key] = remove_nested_nones(item)
                else:
                    cleaned_dict[key] = item
        elif value is None:
            continue
        else:
            cleaned_dict[key] = value
    return cleaned_dict


@dataclass
class GraphqlObject:
    @classmethod
    def list_items(
        cls: Type[Q],
        url: str = None,
        api_key: str = None,
        query_fields: Iterable[QueryFieldInput] = None,
        debug: bool = False,
    ) -> Iterable[Q]:
        """
        Queries graphql endpoint and returns list of 'object'
        """

        query_name, query_node = form_graphql_from_graphql_object(cls, query_type="list")

        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {"query": query, "variables": {"input": {}}}
        query_return = execute_graphql_query(json_data, url=url, api_key=api_key)

        errors = query_return.get("errors")
        if errors is None:
            data = query_return.get("data", {}).get(query_name)
            if data is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            for item in query_return.get("data", {}).get(query_name, {}).get("items", []):
                yield cls.from_dict(deserialize_graphql_return(item))
        else:
            raise Exception(errors)

    def fetch_by_index(
        cls: Type[Q], url: str = None, api_key: str = None, query_function: str = None, query_input_name: str = None, debug: bool = False, **kwargs
    ) -> Iterable[Q]:
        """
        Fetches object by index
        """
        query_name, query_node = form_graphql_from_graphql_object(
            cls, query_type="list", query_function=query_function, query_input_name=query_input_name
        )
        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        json_data = {"query": query, "variables": {"input": kwargs}}

        query_return = execute_graphql_query(json_data, url=url, api_key=api_key)
        errors = query_return.get("errors")
        if errors is None:
            data = query_return.get("data", {}).get(query_name)
            if data is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            for item in query_return.get("data", {}).get(query_name, {}).get("items", []):
                yield cls.from_dict(deserialize_graphql_return(item))
        else:
            raise Exception(errors)

    def get_query_input(self: GraphqlType) -> Dict[str, Any]:
        """
        Fetches object's fields and returns a dict of the form {field_name: field_value}
        """
        # simple way to format to camelCase
        data: Dict[str, Any] = json.loads(self.to_json())
        return remove_nested_nones(data)

    def change_entry(
        self: Q, change_type: str, url: str = None, api_key: str = None, debug: bool = False
    ) -> Q:
        var_input = self.get_query_input()

        query_name, query_node = form_graphql_from_graphql_object(
            self.__class__, query_type=change_type
        )
        query = graphql.language.print_ast(query_node)
        if debug:
            print(query)

        variables = {"input": var_input}
        json_data = {"query": query, "variables": variables}

        query_return = execute_graphql_query(json_data, url=url, api_key=api_key)
        errors = query_return.get("errors")
        if errors is None:
            item = query_return.get("data", {}).get(query_name)
            if item is None:
                print(query_return)
                raise Exception(f"{query_name} not found in query_return")

            return self.__class__.from_dict(deserialize_graphql_return(item))

        raise Exception(errors)

    def create_entry(self: Q, url: str = None, api_key: str = None, debug: bool = False) -> Q:
        """
        Creates a new entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self)
        new_graphql_object = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        if hasattr(new_graphql_object, "id_value"):
            new_graphql_object.id_value = None

        return new_graphql_object.change_entry("create", url=url, api_key=api_key, debug=debug)

    def update_entry(self: Q, url: str = None, api_key: str = None, debug: bool = False) -> Q:
        """
        Updates an entry in the graphql endpoint
        """
        cleaned = remove_nested_items_needed(self)
        new_graphql_object = self.__class__.from_dict(cleaned)
        new_graphql_object.created_at = None
        new_graphql_object.updated_at = None

        return new_graphql_object.change_entry("update", url=url, api_key=api_key, debug=debug)

    @classmethod
    def from_dynamo_event_record(cls: Type[Q], record: Dict[str, Any]) -> Union[Q, Tuple[Q, Q]]:
        """
        Returns a graphql object from a dynamo record
        """
        event_type: str = record["eventName"]
        if event_type == "INSERT":
            return cls.from_dict(clean_dynamo_data(record["dynamodb"]["NewImage"]))
        elif event_type == "MODIFY":
            return (
                cls.from_dict(clean_dynamo_data(record["dynamodb"]["NewImage"])),
                cls.from_dict(clean_dynamo_data(record["dynamodb"]["OldImage"])),
            )

    @classmethod
    def items_needed(cls: Type[Q]) -> List[str]:
        return []


def remove_nested_items_needed(node: GraphqlType) -> Optional[Dict[str, Any]]:
    """
    Returns a nested dictionary from a graphql object, removing fields with items_needed
    """
    cleaned_dict = {}
    for item in fields(node):
        item_value = getattr(node, item.name)
        if item.name in node.items_needed():
            continue
        if is_dataclass(item.type):
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

    if isinstance(item_type, str):
        return eval(item_type)

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


def form_graphql_from_graphql_object(
    cls: GraphqlObject, query_type: str, query_function: str = None, query_input_name: str = None
) -> Tuple[str, graphql.language.OperationDefinitionNode]:
    """
    Returns a fully formed graphql query definition from a graphql object
    """
    if query_type == "list":
        query_function = query_function or (query_type + cls.__name__ + "s")
    else:
        query_function = query_function or (query_type + cls.__name__)

    query_input_name = query_input_name or query_type.capitalize() + cls.__name__ + "Input"
    if query_type == "list":
        query_name = query_type.capitalize() + cls.__name__ + "Query"
        operation = graphql.language.OperationType.QUERY
        variable_definitions = []
        arguments = []
        selection_set = graphql.language.SelectionSetNode(
            selections=[
                graphql.language.FieldNode(
                    alias=None,
                    name=graphql.language.NameNode(value="items"),
                    arguments=[],
                    directives=[],
                    selection_set=graphql_selection_from_graphql_object(cls),
                )
            ]
        )
    else:
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
                value=graphql.language.VariableNode(
                    name=graphql.language.NameNode(value="input")
                ),
            ),
        ]
        selection_set = graphql_selection_from_graphql_object(cls)


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
                    selection_set=selection_set
                )
            ]
        ),
    )

    return query_function, operation_definition


def graphql_selection_from_graphql_object(cls: GraphqlObject) -> graphql.SelectionSetNode:
    """
    Form nested query string from a graphql object
    """
    class_fields = fields(cls)
    items_needed = cls.items_needed() if hasattr(cls, "items_needed") else []
    selections = []
    print(cls.__name__)
    # print(class_fields)

    for item in class_fields:
        nested_field_type = _resolve_field_type(item.type)
        nested_field_name = clean_dataclass_field(item)
        print(nested_field_type)
        if is_dataclass(nested_field_type):

            nested_selection = graphql_selection_from_graphql_object(nested_field_type)

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


def choose_gql_type(raw_item: Dict[str, Any]) -> Callable[[str], Dict[str, Any]]:
    print(raw_item)

    new_item = clean_dynamo_data(raw_item["dynamodb"]["NewImage"])
    item_type = new_item.get("__typename")
    owner = new_item.get("owner", None)
    new_class_inst: GraphqlObject = eval(item_type).from_dict(new_item)
    event_type: str = raw_item["eventName"]
    process_func_name = f"{event_type.lower()}_{camel_to_snake(item_type)}"

    if event_type == "INSERT":
        process_function: Callable[[GraphqlObject, str, str], Dict[str, Any]] = eval(
            process_func_name
        )

        return partial(process_function, new_class_inst, owner)
    elif event_type == "MODIFY":
        old_item = clean_dynamo_data(raw_item["dynamodb"]["OldImage"])
        old_class_inst: GraphqlObject = eval(item_type).from_dict(old_item)

        process_function: Callable[[GraphqlObject, str, str], Dict[str, Any]] = eval(
            process_func_name
        )

        return partial(process_function, new_class_inst, old_class_inst, owner)

    else:
        print("we don't handle this case yet")
        print(raw_item)