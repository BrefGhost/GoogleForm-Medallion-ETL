from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="medallion_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    bronze_task = DockerOperator(
        task_id="bronze_task",
        image="googleform-medallion-etl-bronze:latest",
        docker_url="unix://var/run/docker.sock",
        network_mode="medallion_network",
        auto_remove="success",
    )

    silver_task = DockerOperator(
        task_id="silver_task",
        image="googleform-medallion-etl-silver:latest",
        docker_url="unix://var/run/docker.sock",
        network_mode="medallion_network",
        auto_remove="success",
    )

    gold_task = DockerOperator(
        task_id="gold_task",
        image="googleform-medallion-etl-gold:latest",
        docker_url="unix://var/run/docker.sock",
        network_mode="medallion_network",
        auto_remove="success",
    )

    bronze_task >> silver_task >> gold_task