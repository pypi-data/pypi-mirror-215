import json
from io import BytesIO
import tarfile
from itertools import islice
from mailchimp_marketing.api import batches_api
import requests
from .decorators import no_batch
from .collections import BatchCollection, ResponseCollection


class Response:
    def __init__(self, **kwargs):
        self.operation_id = kwargs["operation_id"]
        self.status_code = kwargs["status_code"]
        self.body = json.loads(kwargs["response"])

    def __repr__(self):
        return "<{module}.{name}: {operation_id} ({status_code})>".format(
            module=self.__class__.__module__,
            name=self.__class__.__name__,
            operation_id=self.operation_id,
            status_code=self.status_code,
        )


class Batch:
    def __init__(self, batches_api, **kwargs):
        self._batches_api = batches_api
        self._operations = kwargs.get("operations")
        self.response = None
        self.update(**kwargs)

    def update(self, **kwargs):
        self.batch_id = kwargs.get("id")
        self.total_operations = kwargs.get("total_operations")
        self.finished_operations = kwargs.get("finished_operations")
        self.errored_operations = kwargs.get("errored_operations")
        self.submitted_at = kwargs.get("submitted_at")
        self.completed_at = kwargs.get("completed_at")
        self.response_body_url = kwargs.get("response_body_url")
        self._status = kwargs.get("status")

    def __repr__(self):
        return "<{module}.{name}: {finished}/{total} operation{s} ({status})>".format(
            module=self.__class__.__module__,
            name=self.__class__.__name__,
            finished=self.finished_operations,
            total=self.total_operations,
            s="s" if self.total_operations != 1 else "",
            status=self._status,
        )

    def status(self, refresh=False):
        if refresh:
            self._batches_api.status(self.batch_id, refresh=refresh)
        return self

    def response(self):
        if self.response:
            return self.response
        batch = self.status(refresh=True)
        if batch._status == "finished" and batch.response_body_url:
            content = requests.get(batch.response_body_url).content
            tf = tarfile.open(fileobj=BytesIO(content))
            output = []
            for member in tf.getmembers():
                file_content = tf.extractfile(member)
                if file_content is None:
                    continue
                output += json.load(file_content)
            self.response = ResponseCollection({
                o["operation_id"]: Response(**o)
                for o in output
            })
            return self.response

    def delete(self):
        return self._batches_api.delete_request(self.batch_id)


class BatchesApi(batches_api.BatchesApi):
    _max_operations = 1_000

    def __init__(self, api_client):
        super().__init__(api_client)
        self._batches = BatchCollection()

    def get(self, batch_id, **kwargs):
        try:
            return self.status(batch_id, **kwargs)
        except KeyError:
            ...

    def __getitem__(self, batch_id):
        return self.status(batch_id)

    @no_batch
    def run(self):
        operations = self.api_client.operations
        if len(operations) == 0:
            raise Exception("No operations to run")
        if len(operations) > self._max_operations:
            msg = f"More than {self._max_operations} operations. Use bulk_run"
            raise Exception(msg)
        batch_data = self.start({"operations": operations})
        batch = Batch(self, operations=operations, **batch_data)
        self._batches[batch.batch_id] = batch
        self.api_client.operations = []
        return batch

    @no_batch
    def bulk_run(self):
        if len(self.api_client.operations) == 0:
            raise Exception("No operations to run")
        operations = iter(self.api_client.operations)
        while operations_chunk := list(islice(operations, self._max_operations)):
            batch_data = self.start({"operations": operations_chunk})
            batch = Batch(self, operations=operations_chunk, **batch_data)
            self._batches[batch.batch_id] = batch
        return self._batches

    def delete_all(self, refresh=False, **kwargs):
        batches = self.list(refresh=refresh)
        batch_ids = [batch.batch_id for batch in batches]
        for batch_id in batch_ids:
            self.delete_request(batch_id)
        return self._batches

    def delete(self, batch_id, **kwargs):
        return self.delete_request(batch_id, **kwargs)

    @no_batch
    def delete_request(self, batch_id, **kwargs):
        resp = super().delete_request(batch_id, **kwargs)
        del self._batches[batch_id]
        return resp

    @no_batch
    def list(self, refresh=False, **kwargs):
        if refresh:
            results = super().list(**kwargs)
            for batch_data in results["batches"]:
                if batch_data["id"] in self._batches:
                    self._batches[batch_data["id"]].update(**batch_data)
                else:
                    self._batches[batch_data["id"]] = Batch(self, **batch_data)
        return self._batches

    @no_batch
    def status(self, batch_id, refresh=False, **kwargs):
        batch = self._batches.get(batch_id)
        if refresh:
            batch_data = super().status(batch_id, **kwargs)
            if batch:
                batch.update(**batch_data)
            else:
                batch = Batch(self, **batch_data)
                self._batches[batch_id] = batch
        return self._batches[batch_id]
