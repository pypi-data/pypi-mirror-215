from botocore.exceptions import ClientError

from localstack.aws.api.stepfunctions import HistoryEventType, TaskFailedEventDetails
from localstack.aws.protocol.service_router import get_service_catalog
from localstack.services.stepfunctions.asl.component.common.error_name.failure_event import (
    FailureEvent,
)
from localstack.services.stepfunctions.asl.component.common.error_name.states_error_name import (
    StatesErrorName,
)
from localstack.services.stepfunctions.asl.component.common.error_name.states_error_name_type import (
    StatesErrorNameType,
)
from localstack.services.stepfunctions.asl.component.state.state_execution.state_task.service.state_task_service_callback import (
    StateTaskServiceCallback,
)
from localstack.services.stepfunctions.asl.eval.environment import Environment
from localstack.services.stepfunctions.asl.eval.event.event_detail import EventDetails
from localstack.utils.aws import aws_stack
from localstack.utils.common import camel_to_snake_case


class StateTaskServiceAwsSdk(StateTaskServiceCallback):
    _API_NAMES: dict[str, str] = {"sfn": "stepfunctions"}
    _SFN_TO_BOTO_PARAM_NORMALISERS = {
        "stepfunctions": {"send_task_success": {"Output": "output", "TaskToken": "taskToken"}}
    }

    def _get_sfn_resource_type(self) -> str:
        return f"{self.resource.service_name}:{self.resource.api_name}"

    def _normalise_api_name(self, api_name: str) -> str:
        return self._API_NAMES.get(api_name, api_name)

    def _boto_normalise_parameters(self, api_name: str, api_action: str, parameters: dict) -> None:
        api_normalisers = self._SFN_TO_BOTO_PARAM_NORMALISERS.get(api_name)
        if not api_normalisers:
            return

        action_normalisers = api_normalisers.get(api_action)
        if not action_normalisers:
            return None

        parameter_keys = list(parameters.keys())
        for parameter_key in parameter_keys:
            norm_parameter_key = action_normalisers.get(parameter_key)
            if norm_parameter_key:
                tmp = parameters[parameter_key]
                del parameters[parameter_key]
                parameters[norm_parameter_key] = tmp

    @staticmethod
    def _normalise_service_name(service_name: str) -> str:
        return get_service_catalog().get(service_name).service_id.replace(" ", "")

    @staticmethod
    def _normalise_exception_name(norm_service_name: str, ex: Exception) -> str:
        ex_name = ex.__class__.__name__
        return f"{norm_service_name}.{norm_service_name if ex_name == 'ClientError' else ex_name}Exception"

    def _get_task_failure_event(self, error: str, cause: str) -> FailureEvent:
        return FailureEvent(
            error_name=StatesErrorName(typ=StatesErrorNameType.StatesTaskFailed),
            event_type=HistoryEventType.TaskFailed,
            event_details=EventDetails(
                taskFailedEventDetails=TaskFailedEventDetails(
                    resource=self._get_sfn_resource(),
                    resourceType=self._get_sfn_resource_type(),
                    error=error,
                    cause=cause,
                )
            ),
        )

    def _from_error(self, env: Environment, ex: Exception) -> FailureEvent:
        norm_service_name: str = self._normalise_service_name(self.resource.api_name)
        error: str = self._normalise_exception_name(norm_service_name, ex)
        if isinstance(ex, ClientError):
            error_message: str = ex.response["Error"]["Message"]
            cause_details = [
                f"Service: {norm_service_name}",
                f"Status Code: {ex.response['ResponseMetadata']['HTTPStatusCode']}",
                f"Request ID: {ex.response['ResponseMetadata']['RequestId']}",
            ]
            if "HostId" in ex.response["ResponseMetadata"]:
                cause_details.append(
                    f'Extended Request ID: {ex.response["ResponseMetadata"]["HostId"]}'
                )

            cause: str = f"{error_message} ({', '.join(cause_details)})"
            failure_event = self._get_task_failure_event(error=error, cause=cause)
            return failure_event

        failure_event = self._get_task_failure_event(
            error=error, cause=str(ex)  # TODO: update cause decoration.
        )
        return failure_event

    def _eval_service_task(self, env: Environment, parameters: dict) -> None:
        api_name = self.resource.api_name
        api_name = self._normalise_api_name(api_name)
        api_action = camel_to_snake_case(self.resource.api_action)

        self._boto_normalise_parameters(
            api_name=api_name, api_action=api_action, parameters=parameters
        )

        api_client = aws_stack.create_external_boto_client(service_name=api_name)

        response = getattr(api_client, api_action)(**parameters) or dict()
        if response:
            response.pop("ResponseMetadata", None)

        env.stack.append(response)
