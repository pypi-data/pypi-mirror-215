import math
import typing as t
from multiprocessing import Pool
from pathlib import Path

import cloudpickle as cp
import httpx

from pipeline.objects import Graph, PipelineFile
from pipeline.util.logging import _print
from pipeline.v3 import http
from pipeline.v3.schemas.runs import Run, RunCreate, RunInput, RunIOType, RunOutput


def upload_pipeline(
    graph: Graph,
    environment_id_or_name: t.Union[str, int],
):
    if graph._has_run_startup:
        raise Exception("Graph has already been run, cannot upload")

    for variable in graph.variables:
        if isinstance(variable, PipelineFile):
            variable_path = Path(variable.path)
            if not variable_path.exists():
                raise FileNotFoundError(
                    f"File not found for variable (path={variable.path}, "
                    f"variable={variable.name})"
                )

            variable_file = variable_path.open("rb")
            try:
                res = http.post_files(
                    "/v3/pipeline_files",
                    files=dict(pfile=variable_file),
                    progress=True,
                )

                new_path = res.json()["path"]
                variable.path = new_path
                variable.remote_id = res.json()["id"]
            finally:
                variable_file.close()

    with open("graph.tmp", "wb") as tmp:
        tmp.write(cp.dumps(graph))

    graph_file = open("graph.tmp", "rb")

    params = dict()
    if graph.min_gpu_vram_mb is not None:
        params["gpu_memory_min"] = graph.min_gpu_vram_mb

    if minimum_cache_number := getattr(graph, "minimum_cache_number", None):
        params["minimum_cache_number"] = minimum_cache_number

    if isinstance(environment_id_or_name, int):
        params["environment_id"] = environment_id_or_name
    elif isinstance(environment_id_or_name, str):
        params["environment_name"] = environment_id_or_name

    res = http.post_files(
        "/v3/pipelines",
        files=dict(graph=graph_file),
        params=params,
    )

    graph_file.close()

    return res


def _data_to_run_input(data: t.Any) -> t.List[RunInput]:
    input_array = []

    for item in data:
        input_type = RunIOType.from_object(item)
        if input_type == RunIOType.file:
            raise NotImplementedError("File input not yet supported")
        elif input_type == RunIOType.pkl:
            raise NotImplementedError("Python object input not yet supported")

        input_schema = RunInput(
            type=input_type,
            value=item,
        )
        input_array.append(input_schema)

    return input_array


def run_pipeline(
    pipeline_id_or_tag: t.Union[str, int],
    *data,
    async_run: bool = False,
    return_response: bool = False,
) -> t.Union[Run, httpx.Response]:
    run_create_schema = RunCreate(
        pipeline_id_or_tag=pipeline_id_or_tag,
        input_data=_data_to_run_input(data),
        async_run=async_run,
    )

    res = http.post(
        "/v3/runs",
        json_data=run_create_schema.dict(),
        raise_for_status=False,
    )

    if return_response:
        return res

    if res.status_code == 500:
        _print(
            f"Failed run (status={res.status_code}, text={res.text}, "
            f"headers={res.headers})",
            level="ERROR",
        )
        raise Exception(f"Error: {res.status_code}, {res.text}", res.status_code)
    elif res.status_code == 429:
        _print(
            f"Too many requests (status={res.status_code}, text={res.text})",
            level="ERROR",
        )
        raise Exception(
            "Too many requests, please try again later",
            res.status_code,
        )
    elif res.status_code == 404:
        _print(
            f"Pipeline not found (status={res.status_code}, text={res.text})",
            level="ERROR",
        )
        raise Exception("Pipeline not found", res.status_code)
    elif res.status_code == 503:
        _print(
            f"Environment not cached (status={res.status_code}, text={res.text})",
            level="ERROR",
        )
        raise Exception("Environment not cached", res.status_code)
    elif res.status_code == 502:
        _print(
            "Gateway error",
            level="ERROR",
        )
        raise Exception("Gateway error", res.status_code)

    # Everything is okay!
    run_get = Run.parse_obj(res.json())

    return run_get


def get_pipeline_run(run_id: int) -> Run:
    http_res = http.get(f"/v3/runs/{run_id}")

    run_get = Run.parse_obj(http_res.json())
    return run_get


def map_pipeline_mp(array: list, graph_id: str, *, pool_size=8):
    results = []

    num_batches = math.ceil(len(array) / pool_size)
    for b in range(num_batches):
        start_index = b * pool_size
        end_index = min(len(array), start_index + pool_size)

        inputs = [[graph_id, item] for item in array[start_index:end_index]]

        with Pool(pool_size) as p:
            batch_res = p.starmap(run_pipeline, inputs)
            results.extend(batch_res)

    return results


def stream_pipeline(
    pipeline_id_or_tag: t.Union[str, int],
    *data,
) -> t.Iterable[RunOutput]:
    run_create_schema = RunCreate(
        pipeline_id_or_tag=pipeline_id_or_tag,
        input_data=_data_to_run_input(data),
        async_run=False,
    )

    return http.stream_post(
        "/v3/runs/stream",
        json_data=run_create_schema.dict(),
    )
