import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
# from airflow.operators.
from airflow.models.param import Param
from airflow.decorators import task
# from airflow.operators.

with DAG(
    dag_id="bio_pipeline",
    start_date=datetime.datetime(2021, 1, 1),
    schedule=None,
    catchup=False,
    params={
        "ref_path": Param('/host/ecoli/ref/GCF_000005845.2_ASM584v2_genomic.fna', type='string'),
        "fasta_path": Param('/host/ecoli/wgs_5/SRR24457391.fastq.gz', type='string'),
        "out_path": Param('/host/ecoli_out', type='string'),
    }
):  
    prepare_dir = BashOperator(
        task_id="prepare_dir",
        bash_command="mkdir -p '{{ params.out_path }}' && find '{{ params.out_path }}' -mindepth 1 -delete"
    )
    run_fastqc = BashOperator(
        bash_command="fastqc -o '{{ params.out_path }}' -t $(nproc) '{{ params.fasta_path }}'",
        task_id="run_fastqc"
    )
    run_bwa = BashOperator(
        bash_command="bwa mem -t $(nproc) '{{ params.ref_path }}' '{{ params.fasta_path }}' > '{{ params.out_path }}'/result.sam",
        task_id="bwa_id"
    )
    run_samtools_view = BashOperator(
        bash_command="samtools view --threads $(nproc) -b '{{ params.out_path }}'/result.sam > '{{ params.out_path }}'/result.bam",
        task_id='samtools_view'
    )

    get_quality = BashOperator(
        task_id='get_quality',
        bash_command="samtools flagstat --threads $(nproc) '{{ params.out_path }}'/result.bam | python3 -c 'from sys import stdin; d=stdin.read(); import re; print(re.findall(r\"\\d+\\s+\\+\\s+\\d+\\s+mapped\\s+\\((\\d+\\.\\d+)%\", d)[0])'",
        do_xcom_push=True
    )

    @task.branch(task_id="branch_on_quality")
    def branch_func(ti=None):
        val = float(ti.xcom_pull(task_ids='get_quality'))
        if val >= 90:
            return "sort"
        else:
            return "quality_bad"
        
    sort_task = BashOperator(
        task_id='sort',
        bash_command="samtools sort --threads $(nproc) -T '{{ params.out_path }}'/sam_tmp '{{ params.out_path }}'/result.bam > '{{ params.out_path }}'/result.sorted.bam"
    )

    freebayes = BashOperator(
        task_id='freebayes',
        bash_command="freebayes -f '{{ params.ref_path }}' '{{ params.out_path }}'/result.sorted.bam > '{{ params.out_path }}'/result.vcf"
    )

    quality_bad=EmptyOperator(task_id="quality_bad")
        
    branch_task = branch_func()

    prepare_dir >> [
        run_fastqc, 
        run_bwa,
        ]
    run_bwa >> run_samtools_view
    run_samtools_view >> get_quality >> branch_task
    branch_task >> quality_bad
    branch_task >> sort_task >> freebayes