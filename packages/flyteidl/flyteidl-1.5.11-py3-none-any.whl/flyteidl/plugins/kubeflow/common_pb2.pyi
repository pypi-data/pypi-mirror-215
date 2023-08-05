from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RestartPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RESTART_POLICY_NEVER: _ClassVar[RestartPolicy]
    RESTART_POLICY_ON_FAILURE: _ClassVar[RestartPolicy]
    RESTART_POLICY_ALWAYS: _ClassVar[RestartPolicy]

class CleanPodPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CLEANPOD_POLICY_NONE: _ClassVar[CleanPodPolicy]
    CLEANPOD_POLICY_RUNNING: _ClassVar[CleanPodPolicy]
    CLEANPOD_POLICY_ALL: _ClassVar[CleanPodPolicy]
RESTART_POLICY_NEVER: RestartPolicy
RESTART_POLICY_ON_FAILURE: RestartPolicy
RESTART_POLICY_ALWAYS: RestartPolicy
CLEANPOD_POLICY_NONE: CleanPodPolicy
CLEANPOD_POLICY_RUNNING: CleanPodPolicy
CLEANPOD_POLICY_ALL: CleanPodPolicy

class RunPolicy(_message.Message):
    __slots__ = ["clean_pod_policy", "ttl_seconds_after_finished", "active_deadline_seconds", "backoff_limit"]
    CLEAN_POD_POLICY_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_AFTER_FINISHED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DEADLINE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BACKOFF_LIMIT_FIELD_NUMBER: _ClassVar[int]
    clean_pod_policy: CleanPodPolicy
    ttl_seconds_after_finished: int
    active_deadline_seconds: int
    backoff_limit: int
    def __init__(self, clean_pod_policy: _Optional[_Union[CleanPodPolicy, str]] = ..., ttl_seconds_after_finished: _Optional[int] = ..., active_deadline_seconds: _Optional[int] = ..., backoff_limit: _Optional[int] = ...) -> None: ...
