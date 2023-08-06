import pymysql
import pandas as pd
from cmhlims.connectToLIMS import connect_to_lims

def get_analyses(sample_names, reference_genome):
    if len(reference_genome) != 1:
        raise ValueError("getAnalyses() supports only a single reference genome")

    if len(sample_names) == 0:
        raise ValueError("getAnalyses() requires at least one sample name")

    analysis_query_template = """select s.label as sample_name,
        a.id as analysis_id,
        a.label as analysis_name,
        a.base_dir as analysis_dir,
        a.analysis_date as analysis_date,
        q.label as sequence_type,
        t.label as analysis_type,
        r.label as reference_genome
        from samples s,
            downstream_analyses a,
            downstream_analysis_types t,
            sequence_types q,
            reference_genomes r
        where s.id = a.sample_id
            and a.sequence_type_id = q.id
            and a.reference_genome_id = r.id
            and a.downstream_analysis_type_id = t.id
            and r.label = '{ref_genome}'
            and s.label IN ({sample_list});"""

    sample_list = "'" + "','".join(sample_names) + "'"

    analysis_query = analysis_query_template.format(ref_genome=reference_genome[0], sample_list=sample_list)
    lims_db = connect_to_lims()

    try:
        with lims_db.cursor() as cursor:
            cursor.execute(analysis_query)
            columns = [column[0] for column in cursor.description]
            analyses_data = cursor.fetchall()
            analyses_df = pd.DataFrame(analyses_data, columns=columns)
    finally:
        lims_db.close()

    return analyses_df
