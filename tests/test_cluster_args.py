from pathlib import Path

import dask
import pytest

from dask_chtc import CHTCCluster


@pytest.fixture
def default_modified_kwargs():
    return CHTCCluster._modify_kwargs({})


def test_entrypoint_is_in_transfer_input_files(default_modified_kwargs):
    assert "entrypoint.sh" in default_modified_kwargs["job_extra"]["transfer_input_files"]


def test_default_batch_name_is_dask_worker(default_modified_kwargs):
    assert default_modified_kwargs["job_extra"]["JobBatchName"] == '"dask-worker"'


def test_can_override_job_batch_name_via_job_extra():
    kwargs = CHTCCluster._modify_kwargs(dict(job_extra={"JobBatchName": '"foobar"'}))

    assert kwargs["job_extra"]["JobBatchName"] == '"foobar"'


def test_can_override_job_batch_name_via_kwarg():
    kwargs = CHTCCluster._modify_kwargs({}, batch_name="foobar")

    assert kwargs["job_extra"]["JobBatchName"] == '"foobar"'


def test_can_override_job_batch_name_via_dask_config():
    dask.config.set({f"jobqueue.{CHTCCluster.config_name}.batch-name": "foobar"})
    kwargs = CHTCCluster._modify_kwargs({})

    assert kwargs["job_extra"]["JobBatchName"] == '"foobar"'


def test_cannot_override_job_universe():
    kwargs = CHTCCluster._modify_kwargs(dict(job_extra={"universe": "foobar"}))

    assert kwargs["job_extra"]["universe"] == "docker"


def test_gpu_request_is_set_if_gpu_lab_not_set_but_request_gpus_is():
    kwargs = CHTCCluster._modify_kwargs({}, gpus=2)

    assert kwargs["job_extra"]["request_gpus"] == "2"


def test_gpu_request_is_1_if_gpu_lab_but_not_set():
    kwargs = CHTCCluster._modify_kwargs({}, gpu_lab=True)

    assert kwargs["job_extra"]["request_gpus"] == "1"


def test_gpu_request_is_not_set_if_no_gpu_options_set(default_modified_kwargs):
    assert "request_gpus" not in default_modified_kwargs["job_extra"]
