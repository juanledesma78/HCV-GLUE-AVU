2021-11-17 14:51:01,719 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'sql_mode'
2021-11-17 14:51:01,719 INFO sqlalchemy.engine.Engine [raw sql] {}
2021-11-17 14:51:01,720 INFO sqlalchemy.engine.Engine SHOW VARIABLES LIKE 'lower_case_table_names'
2021-11-17 14:51:01,721 INFO sqlalchemy.engine.Engine [generated in 0.00015s] {}
2021-11-17 14:51:01,723 INFO sqlalchemy.engine.Engine SELECT DATABASE()
2021-11-17 14:51:01,723 INFO sqlalchemy.engine.Engine [raw sql] {}
2021-11-17 14:51:01,723 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2021-11-17 14:51:01,724 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,724 INFO sqlalchemy.engine.Engine [generated in 0.00014s] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_aligned_segment'}
2021-11-17 14:51:01,725 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,725 INFO sqlalchemy.engine.Engine [cached since 0.001103s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_alignment'}
2021-11-17 14:51:01,726 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,726 INFO sqlalchemy.engine.Engine [cached since 0.002047s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_alignment_member'}
2021-11-17 14:51:01,727 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,727 INFO sqlalchemy.engine.Engine [cached since 0.002742s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_feature'}
2021-11-17 14:51:01,727 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,727 INFO sqlalchemy.engine.Engine [cached since 0.003377s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_feature_location'}
2021-11-17 14:51:01,728 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,728 INFO sqlalchemy.engine.Engine [cached since 0.004101s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_feature_metatag'}
2021-11-17 14:51:01,729 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,729 INFO sqlalchemy.engine.Engine [cached since 0.004784s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_feature_segment'}
2021-11-17 14:51:01,729 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,729 INFO sqlalchemy.engine.Engine [cached since 0.005546s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_member_floc_note'}
2021-11-17 14:51:01,730 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,730 INFO sqlalchemy.engine.Engine [cached since 0.00637s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_module'}
2021-11-17 14:51:01,731 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,731 INFO sqlalchemy.engine.Engine [cached since 0.007174s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_module_resource'}
2021-11-17 14:51:01,732 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,732 INFO sqlalchemy.engine.Engine [cached since 0.008279s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_project_setting'}
2021-11-17 14:51:01,733 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,733 INFO sqlalchemy.engine.Engine [cached since 0.00924s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_reference_sequence'}
2021-11-17 14:51:01,734 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,734 INFO sqlalchemy.engine.Engine [cached since 0.01053s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_seq_orig_data'}
2021-11-17 14:51:01,735 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,736 INFO sqlalchemy.engine.Engine [cached since 0.01161s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_sequence'}
2021-11-17 14:51:01,736 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,736 INFO sqlalchemy.engine.Engine [cached since 0.01258s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_source'}
2021-11-17 14:51:01,737 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,738 INFO sqlalchemy.engine.Engine [cached since 0.01362s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_var_almt_note'}
2021-11-17 14:51:01,738 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,738 INFO sqlalchemy.engine.Engine [cached since 0.01448s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_variation'}
2021-11-17 14:51:01,739 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,739 INFO sqlalchemy.engine.Engine [cached since 0.01527s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_variation_metatag'}
2021-11-17 14:51:01,740 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,740 INFO sqlalchemy.engine.Engine [cached since 0.01608s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_who_country'}
2021-11-17 14:51:01,741 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,741 INFO sqlalchemy.engine.Engine [cached since 0.01679s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_who_intermediate_region'}
2021-11-17 14:51:01,741 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,741 INFO sqlalchemy.engine.Engine [cached since 0.01752s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_who_region'}
2021-11-17 14:51:01,742 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,742 INFO sqlalchemy.engine.Engine [cached since 0.01829s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_who_sub_region'}
2021-11-17 14:51:01,743 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,743 INFO sqlalchemy.engine.Engine [cached since 0.01911s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_sample'}
2021-11-17 14:51:01,744 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,744 INFO sqlalchemy.engine.Engine [cached since 0.02006s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_patient'}
2021-11-17 14:51:01,746 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,746 INFO sqlalchemy.engine.Engine [cached since 0.02251s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_hospital'}
2021-11-17 14:51:01,747 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,747 INFO sqlalchemy.engine.Engine [cached since 0.02357s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_treatment'}
2021-11-17 14:51:01,748 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2021-11-17 14:51:01,748 INFO sqlalchemy.engine.Engine [cached since 0.02423s ago] {'table_schema': 'GLUE_TOOLS', 'table_name': 'hcv_glue_avu_drug'}
2021-11-17 14:51:01,749 INFO sqlalchemy.engine.Engine COMMIT
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 460d623af7cb

CREATE INDEX sample_id ON hcv_glue_avu_sequence (sample_id);

CREATE INDEX who_country_id ON hcv_glue_avu_sequence (who_country_id);

ALTER TABLE hcv_glue_avu_sequence ADD FOREIGN KEY(sample_id) REFERENCES hcv_glue_avu_sample (id);

ALTER TABLE hcv_glue_avu_sequence ADD FOREIGN KEY(who_country_id) REFERENCES hcv_glue_avu_who_country (id);

ALTER TABLE hcv_glue_avu_who_country ADD FOREIGN KEY(who_sub_region_id) REFERENCES hcv_glue_avu_who_sub_region (id);

ALTER TABLE hcv_glue_avu_who_country ADD FOREIGN KEY(who_region_id) REFERENCES hcv_glue_avu_who_region (id);

ALTER TABLE hcv_glue_avu_who_country ADD FOREIGN KEY(who_intermediate_region_id) REFERENCES hcv_glue_avu_who_intermediate_region (id);

INSERT INTO alembic_version (version_num) VALUES ('460d623af7cb');

