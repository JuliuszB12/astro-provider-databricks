from datetime import datetime

from airflow.decorators import dag
from astro_databricks.operators.notebook import DatabricksNotebookOperator
from astro_databricks.operators.workflow import DatabricksWorkflowTaskGroup

job_clusters = [
    {
        "job_cluster_key": "Shared_job_cluster",
        "new_cluster": {
            "cluster_name": "",
            "spark_version": "11.3.x-scala2.12",
            "node_type_id": "Standard_DS3_v2",
            "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
            "enable_elastic_disk": False,
            "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
            "runtime_engine": "STANDARD",
            "num_workers": 8,
        },
    }
]


@dag(
    schedule_interval="@daily",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["astro-provider-databricks"],
)
def basic_notebooks():
    with DatabricksWorkflowTaskGroup(
        group_id="example_notebooks",
        databricks_conn_id="databricks_default",
        job_clusters=job_clusters,
        notebook_packages=[{"pypi": {"package": "simplejson"}}],
    ):
        nb_1 = DatabricksNotebookOperator(
            task_id="nb_1",
            databricks_conn_id="databricks_default",
            notebook_path="/Shared/Notebook_1",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            notebook_packages=[{"pypi": {"package": "Faker"}}],
        )

        nb_2 = DatabricksNotebookOperator(
            task_id="nb_2",
            databricks_conn_id="databricks_default",
            notebook_path="/Shared/Notebook_2",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
        )

        nb_1 >> nb_2


basic_notebooks()
