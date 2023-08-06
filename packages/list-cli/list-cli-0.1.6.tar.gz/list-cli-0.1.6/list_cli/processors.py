from abc import ABC, abstractmethod
from getpass import getuser
from os import linesep, makedirs
from os.path import (
    dirname,
    isdir,
    isfile
)
from re import match
from time import time
from uuid import UUID, uuid1

from list_cli.results import (
    ErrorResult,
    Result,
    SuccessResult
)


class BaseProcessor(ABC):
    @abstractmethod
    def process(self, *args) -> Result:
        pass


class Processor(BaseProcessor):
    ADDED_BUCKET = 'a'
    ADD_OPERATIONS = {'a', 'add'}
    BUCKET_PATTERN = r'^(a|added|d|done|h|handed_off|m|moved|r|removed)$'
    DEFAULT_PARENT_ID = UUID('00000000-0000-0000-0000-000000000000')
    DONE_BUCKET = 'd'
    DONE_OPERATIONS = {'d', 'done'}
    EDIT_OPERATIONS = {'e', 'edit'}
    HANDED_OFF_BUCKET = 'h'
    HANDOFF_OPERATIONS = {'h', 'handoff'}
    INDEX_PATTERN = r'^[0-9]+$'
    MOVE_OPERATIONS = {'m', 'move'}
    MOVED_BUCKET = 'm'
    OPERATION_PATTERN = r'^(a|add|d|done|e|edit|h|handoff|m|move|r|remove|t|touch)$'
    REMOVED_BUCKET = 'r'
    REMOVE_OPERATIONS = {'r', 'remove'}
    TOUCH_OPERATIONS = {'t', 'touch'}
    VALID_BUCKETS = {
        ADDED_BUCKET,
        DONE_BUCKET,
        HANDED_OFF_BUCKET,
        MOVED_BUCKET,
        REMOVED_BUCKET
    }

    def __init__(
        self,
        database_file_path,
        output_file_path=False
    ):
        self._database_file_path = database_file_path
        self._ensure_database_exists()
        self._output_file_path = output_file_path

    @property
    def _database(self) -> dict:
        if not hasattr(self, '_database_'):
            self._database_ = self._get_database()
        return self._database_

    @property
    def _timestamp(self) -> int:
        if not hasattr(self, '_timestamp_'):
            self._timestamp_ = self._get_timestamp()
        return self._timestamp_

    @property
    def _user(self) -> str:
        if not hasattr(self, '_user_'):
            self._user_ = self._get_user()
        return self._user_

    def process(self, *args) -> Result:
        if not args:
            return self._render(self.ADDED_BUCKET)
        elif match(self.BUCKET_PATTERN, args[0]):
            return self._render(args[0][0])
        elif not match(self.INDEX_PATTERN, args[0]):
            return self._add(message=' '.join(args))
        index = int(args[0]) - 1
        if (
            index < 0 or
            not args[1:] or
            not match(self.OPERATION_PATTERN, args[1])
        ):
            return ErrorResult()
        operation = args[1]
        if operation in self.ADD_OPERATIONS:
            return self._add(message=' '.join(args[1:]))
        elif operation in self.DONE_OPERATIONS:
            return self._done(index)
        elif operation in self.EDIT_OPERATIONS:
            return self._edit(index, ' '.join(args[2:]))
        elif operation in self.HANDOFF_OPERATIONS:
            return self._handoff(index)
        elif operation in self.MOVE_OPERATIONS:
            return self._move(index)
        elif operation in self.REMOVE_OPERATIONS:
            return self._remove(index)
        elif operation in self.TOUCH_OPERATIONS:
            return self._touch(index)
        return ErrorResult()

    def _add(
        self,
        parent_id=None,
        message=None
    ) -> Result:
        if not message:
            return ErrorResult()
        datum = {
            'id': uuid1(),
            'parent_id': parent_id or self.DEFAULT_PARENT_ID,
            'created_by_user': self._user,
            'updated_by_user': self._user,
            'created_timestamp': self._timestamp,
            'updated_timestamp': self._timestamp,
            'bucket': self.ADDED_BUCKET,
            'message': message
        }
        self._database.append(datum)
        return SuccessResult() if self._write_database() else ErrorResult()

    def _done(self, index=None) -> Result:
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket:
            return ErrorResult()
        if index is None or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index != index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
            datum['bucket'] = self.DONE_BUCKET
            break
        return SuccessResult() if self._write_database() else ErrorResult()

    def _edit(
        self,
        index=None,
        message=None
    ) -> Result:
        if not message:
            return ErrorResult()
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket:
            return ErrorResult()
        if index is None or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index != index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
            datum['message'] = message
            break
        return SuccessResult() if self._write_database() else ErrorResult()

    def _ensure_database_exists(self) -> bool:
        database_file_path = self._database_file_path
        database_dirname = dirname(database_file_path)
        if database_dirname and not isdir(database_dirname):
            makedirs(database_dirname)
        if not isfile(database_file_path):
            open(database_file_path, 'w').close()
        return True

    def _get_bucket(self, bucket_id) -> list:
        return sorted(
            (
                datum
                for datum in self._database
                if datum['bucket'] == bucket_id
            ),
            key=lambda datum: datum['updated_timestamp']
        )

    def _get_database(self) -> dict:
        database = []
        with open(self._database_file_path) as database_file:
            for line in database_file:
                line_parts = line.rstrip("\r\n").split("\t")
                if not line_parts:
                    continue
                id_ = line_parts[0]
                if not id_:
                    continue
                parent_id = line_parts[1]
                if not parent_id:
                    continue
                created_by_user = line_parts[2]
                if not created_by_user:
                    continue
                updated_by_user = line_parts[3]
                if not updated_by_user:
                    continue
                created_timestamp = line_parts[4]
                if not created_timestamp:
                    continue
                updated_timestamp = line_parts[5]
                if not updated_timestamp:
                    continue
                bucket = line_parts[6]
                if bucket not in self.VALID_BUCKETS:
                    continue
                message = line_parts[7]
                if not message:
                    continue
                database.append(
                    {
                        'id': UUID(id_),
                        'parent_id': UUID(parent_id),
                        'created_by_user': created_by_user,
                        'updated_by_user': updated_by_user,
                        'created_timestamp': int(created_timestamp),
                        'updated_timestamp': int(updated_timestamp),
                        'bucket': bucket,
                        'message': message
                    }
                )
        return database

    def _get_timestamp(self) -> int:
        return int(time())

    def _get_user(self) -> str:
        return getuser()

    def _handoff(self, index=None) -> Result:
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket:
            return ErrorResult()
        if index is None or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index != index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
            datum['bucket'] = self.HANDED_OFF_BUCKET
            break
        return SuccessResult() if self._write_database() else ErrorResult()

    def _move(self, index=None) -> Result:
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index != index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
            datum['bucket'] = self.MOVED_BUCKET
            break
        return SuccessResult() if self._write_database() else ErrorResult()

    def _remove(self, index=None) -> Result:
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket:
            return ErrorResult()
        if index is None or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index != index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
            datum['bucket'] = self.REMOVED_BUCKET
            break
        return SuccessResult() if self._write_database() else ErrorResult()

    def _render(self, bucket_id) -> Result:
        bucket = self._get_bucket(bucket_id)
        if not bucket:
            return Result(had_error=bucket_id != self.ADDED_BUCKET, had_output=False)
        if self._output_file_path:
            print(f'{self._database_file_path}:{linesep}')
        for datum_index, datum in enumerate(bucket):
            print('%3d. %s' % (datum_index + 1, datum['message']))
        return SuccessResult(had_output=True)

    def _touch(self, index=None) -> Result:
        bucket = self._get_bucket(self.ADDED_BUCKET)
        if not bucket:
            return ErrorResult()
        if index is None or index >= len(bucket):
            return ErrorResult()
        for datum_index, datum in enumerate(bucket):
            if datum_index == index:
                continue
            datum['updated_by_user'] = self._user
            datum['updated_timestamp'] = self._timestamp
        return SuccessResult() if self._write_database() else ErrorResult()

    def _write_database(self) -> bool:
        with open(self._database_file_path, 'w') as database_file:
            for datum in self._database:
                database_file.write(
                    "%s\t%s\t%s\t%s\t%d\t%d\t%s\t%s%s" % (
                        datum['id'],
                        datum['parent_id'],
                        datum['created_by_user'],
                        datum['updated_by_user'],
                        datum['created_timestamp'],
                        datum['updated_timestamp'],
                        datum['bucket'],
                        datum['message'],
                        linesep
                    )
                )
        return True


class MultiProcessor(BaseProcessor):
    def __init__(
        self,
        database_file_paths,
        output_file_paths=True
    ):
        self._database_file_paths = database_file_paths
        self._output_file_paths = output_file_paths
        self._had_error = False
        self._had_output = False

    def process(self, *args) -> Result:
        for database_file_index, database_file_path in enumerate(self._database_file_paths):
            process_result = self._process_one(
                database_file_index,
                database_file_path,
                *args
            )
            if (
                self._output_file_paths and
                process_result.had_output and
                database_file_index != len(self._database_file_paths) - 1
            ):
                print()
        return Result(had_error=self._had_error, had_output=self._had_output)

    def _get_processor(self, database_file_path) -> Processor:
        return Processor(database_file_path, output_file_path=self._output_file_paths)

    def _process_one(
        self,
        database_file_index,
        database_file_path,
        *args
    ) -> Result:
        process_result = self._get_processor(database_file_path).process(*args)
        if process_result.had_error:
            self._had_error = True
        if process_result.had_output:
            self._had_output = True
        return process_result
