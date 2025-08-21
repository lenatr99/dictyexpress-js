PROCESS_DATA = [ {
            "created": "2021-02-24T02:23:18.320496+0000",
            "id": 2177,
            "modified": "2021-11-17T06:04:16.445726+0000",
            "is_active": True,
            "category": "Other:",
            "contributor": {
                "first_name": "Adi",
                "id": 2,
                "last_name": "Genialis",
                "username": "admin"
            },
            "data_name": "{{ alignment.bam.file|basename|default('?') }}",
            "description": "Dictyostelium-specific pipeline. Developed by Bioinformatics Laboratory,\nFaculty of Computer and Information Science, University of Ljubljana,\nSlovenia and Shaulsky Lab, Department of Molecular and Human Genetics,\nBaylor College of Medicine, Houston, TX, USA.\n",
            "entity_always_create": False,
            "entity_input": None,
            "entity_type": "sample",
            "input_schema": [
                {
                    "name": "alignment",
                    "type": "data:alignment:bam:",
                    "label": "Aligned sequence"
                },
                {
                    "name": "gff",
                    "type": "data:annotation:gff3:",
                    "label": "Features (GFF3)"
                },
                {
                    "name": "mappable",
                    "type": "data:mappability:bcm:",
                    "label": "Mappability"
                }
            ],
            "name": "Dictyostelium expressions",
            "output_schema": [
                {
                    "name": "exp",
                    "type": "basic:file:",
                    "label": "Expression RPKUM (polyA)",
                    "description": "mRNA reads scaled by uniquely mappable part of exons."
                },
                {
                    "name": "rpkmpolya",
                    "type": "basic:file:",
                    "label": "Expression RPKM (polyA)",
                    "description": "mRNA reads scaled by exon length."
                },
                {
                    "name": "rc",
                    "type": "basic:file:",
                    "label": "Read counts (polyA)",
                    "description": "mRNA reads uniquely mapped to gene exons."
                },
                {
                    "name": "rpkum",
                    "type": "basic:file:",
                    "label": "Expression RPKUM",
                    "description": "Reads scaled by uniquely mappable part of exons."
                },
                {
                    "name": "rpkm",
                    "type": "basic:file:",
                    "label": "Expression RPKM",
                    "description": "Reads scaled by exon length."
                },
                {
                    "name": "rc_raw",
                    "type": "basic:file:",
                    "label": "Read counts (raw)",
                    "description": "Reads uniquely mapped to gene exons."
                },
                {
                    "name": "exp_json",
                    "type": "basic:json:",
                    "label": "Expression RPKUM (polyA) (json)"
                },
                {
                    "name": "exp_type",
                    "type": "basic:string:",
                    "label": "Expression Type (default output)"
                },
                {
                    "name": "source",
                    "type": "basic:string:",
                    "label": "Gene ID database"
                },
                {
                    "name": "species",
                    "type": "basic:string:",
                    "label": "Species"
                },
                {
                    "name": "build",
                    "type": "basic:string:",
                    "label": "Build"
                },
                {
                    "name": "feature_type",
                    "type": "basic:string:",
                    "label": "Feature type"
                }
            ],
            "persistence": "CAC",
            "requirements": {
                "executor": {
                    "docker": {
                        "image": "public.ecr.aws/s4q6j6e8/resolwebio/biox:2.0.0"
                    }
                },
                "expression-engine": "jinja"
            },
            "run": {
                "program": "NAME=`basename {{ alignment.bam.file }} .bam`\n\nxexpression.py {{ gff.annot.file }} {{ alignment.bam.file }} --rc --rpkm --rpkum {{mappable.mappability.file}}\nre-checkrc \"Calculation of expression values failed.\"\nre-progress 0.5\n\nxexpression.py {{ gff.annot.file }} {{ alignment.bam.file }} --rc --rpkm --rpkum {{mappable.mappability.file}} --mrna\nre-checkrc \"Calculation of expression values failed.\"\nsamtools idxstats {{ alignment.bam.file }} | cut -f -2 | head -n -1 > chrom.sizes\nre-checkrc \"Samtools idxstats command failed.\"\n\nmv expression_rc.tab.gz ${NAME}_expression_rc.tab.gz\nre-save-file rc_raw ${NAME}_expression_rc.tab.gz\n\nmv expression_rc_polya.tab.gz ${NAME}_expression_rc_polya.tab.gz\nre-save-file rc ${NAME}_expression_rc_polya.tab.gz\n\nmv expression_rpkm.tab.gz ${NAME}_expression_rpkm.tab.gz\nre-save-file rpkm ${NAME}_expression_rpkm.tab.gz\n\nmv expression_rpkm_polya.tab.gz ${NAME}_expression_rpkm_polya.tab.gz\nre-save-file rpkmpolya ${NAME}_expression_rpkm_polya.tab.gz\n\nmv expression_rpkum.tab.gz ${NAME}_expression_rpkum.tab.gz\nre-save-file rpkum ${NAME}_expression_rpkum.tab.gz\n\nmv expression_rpkum_polya.tab.gz ${NAME}_expression_rpkum_polya.tab.gz\nexpression2storage.py ${NAME}_expression_rpkum_polya.tab.gz --output json.txt\nre-checkrc\nre-save exp_json json.txt\nre-save-file exp ${NAME}_expression_rpkum_polya.tab.gz\n\nre-save source {{gff.source}}\nre-save species {{alignment.species}}\nre-save build {{alignment.build}}\nre-save feature_type gene\nre-save exp_type polyA\n",
                "runtime": "polyglot",
                "language": "bash"
            },
            "scheduling_class": "BA",
            "slug": "expression-dicty",
            "type": "data:expression:polya:",
            "version": "1.4.1"
        }]