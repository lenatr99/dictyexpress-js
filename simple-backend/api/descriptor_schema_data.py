DESCRIPTOR_SCHEMA = [
    {
        "created": "2017-02-26T22:58:45.646455+0000",
        "id": 4,
        "modified": "2021-11-17T06:04:12.089708+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "0.0.0",
        "description": "Gene set details schema",
        "name": "Gene set details",
        "schema": [
            {
                "name": "description",
                "type": "basic:text:",
                "label": "Description"
            }
        ],
        "slug": "geneset",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    },
    {
        "created": "2017-02-26T22:58:45.705178+0000",
        "id": 8,
        "modified": "2021-11-17T06:04:12.112489+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "0.0.0",
        "description": "Sample annotation template (detailed)",
        "name": "Sample annotation",
        "schema": [
            {
                "name": "sample",
                "group": [
                    {
                        "name": "annotator",
                        "type": "basic:string:",
                        "label": "Annotator"
                    },
                    {
                        "name": "organism",
                        "type": "basic:string:",
                        "label": "Organism",
                        "choices": [
                            {
                                "label": "Homo sapiens",
                                "value": "Homo sapiens"
                            },
                            {
                                "label": "Mus musculus",
                                "value": "Mus musculus"
                            }
                        ],
                        "description": "Identify the organism from which the sequences were derived.\n"
                    },
                    {
                        "name": "source",
                        "type": "basic:string:",
                        "label": "Source",
                        "description": "Briefly identify the biological material e.g., vastus lateralis muscle.\n",
                        "custom_choice_conditions": [
                            "sample.organism"
                        ]
                    },
                    {
                        "name": "cell_type",
                        "type": "basic:string:",
                        "label": "Cell type",
                        "default": "N/A",
                        "required": False,
                        "description": "Type of cell of the sample or from which the sample was obtained.\n",
                        "custom_choice_conditions": [
                            "sample.organism"
                        ]
                    },
                    {
                        "name": "strain",
                        "type": "basic:string:",
                        "label": "Strain",
                        "hidden": "(sample.organism == 'Homo sapiens' || sample.organism == 'Mus musculus')",
                        "description": "Microbial or eukaryotic strain name.\n",
                        "custom_choice_conditions": [
                            "sample.organism"
                        ]
                    },
                    {
                        "name": "cell_line",
                        "type": "basic:string:",
                        "label": "Cell line",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "molecule",
                        "type": "basic:string:",
                        "label": "Molecule",
                        "choices": [
                            {
                                "label": "total RNA",
                                "value": "total RNA"
                            },
                            {
                                "label": "polyA RNA",
                                "value": "polyA RNA"
                            },
                            {
                                "label": "cytoplasmic RNA",
                                "value": "cytoplasmic RNA"
                            },
                            {
                                "label": "nuclear RNA",
                                "value": "nuclear RNA"
                            },
                            {
                                "label": "genomic DNA",
                                "value": "genomic DNA"
                            },
                            {
                                "label": "protein",
                                "value": "protein"
                            },
                            {
                                "label": "other",
                                "value": "other"
                            }
                        ],
                        "description": "Type of molecule that was extracted from the biological material.\n"
                    },
                    {
                        "name": "gender",
                        "type": "basic:string:",
                        "label": "Gender",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "age",
                        "type": "basic:integer:",
                        "label": "Age",
                        "required": False
                    },
                    {
                        "name": "xcag",
                        "type": "basic:integer:",
                        "label": "xCAG",
                        "required": False
                    },
                    {
                        "name": "group",
                        "type": "basic:string:",
                        "label": "Control/Experimenal group",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "optional_char",
                        "type": "list:basic:string:",
                        "label": "Optional characteristics",
                        "required": False,
                        "description": "Optional annotation of a biosource characteristic (e.g. strain, tissue, developmental stage, tumor stage, etc). For each of the entered characteristics, enter the associated value (e.g. 129SV, brain, embryo, etc). Enter the optional characteristics in the format <characteristic:value>.\n"
                    },
                    {
                        "name": "description",
                        "type": "basic:string:",
                        "label": "Description",
                        "default": "N/A",
                        "required": False,
                        "description": "Additional information not provided in the other fields, or paste in broad descriptions that cannot be easily dissected into the other fields.\n"
                    }
                ],
                "label": "Sample annotation"
            }
        ],
        "slug": "sample-detailed",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    },
    {
        "created": "2017-06-28T14:23:34.527290+0000",
        "id": 31,
        "modified": "2021-11-17T06:04:12.203097+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "0.0.1",
        "description": "Differential expression details template",
        "name": "Differential expression details",
        "schema": [
            {
                "name": "thresholds",
                "group": [
                    {
                        "name": "logfc",
                        "type": "basic:decimal:",
                        "label": "Log2 FC",
                        "default": 1
                    },
                    {
                        "name": "prob",
                        "type": "basic:decimal:",
                        "label": "Probability",
                        "default": 0.05
                    },
                    {
                        "name": "prob_field",
                        "type": "basic:string:",
                        "label": "Probability field",
                        "choices": [
                            {
                                "label": "fdr",
                                "value": "fdr"
                            },
                            {
                                "label": "fwer",
                                "value": "fwer"
                            },
                            {
                                "label": "pvalue",
                                "value": "pvalue"
                            },
                            {
                                "label": "logodds",
                                "value": "logodds"
                            }
                        ],
                        "default": "fdr"
                    }
                ],
                "label": "thresholds"
            },
            {
                "name": "case_label",
                "type": "basic:text:",
                "label": "Case label"
            },
            {
                "name": "control_label",
                "type": "basic:text:",
                "label": "Control label"
            },
            {
                "name": "description",
                "type": "basic:text:",
                "label": "Description",
                "required": False
            }
        ],
        "slug": "diff-exp",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    },
    {
        "created": "2018-10-10T11:22:52.690911+0000",
        "id": 73,
        "modified": "2021-11-17T06:04:12.361141+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "1.0.0",
        "description": "Annotation of raw sequencing data",
        "name": "Reads annotation",
        "schema": [
            {
                "name": "description",
                "type": "basic:string:",
                "label": "Description",
                "required": False
            }
        ],
        "slug": "reads",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    },
    {
        "created": "2022-06-28T20:28:20.398642+0000",
        "id": 102,
        "modified": "2022-06-28T20:28:20.398671+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "1.2.1",
        "description": "Sample meta data compliant with GEO and ENCODE databases.",
        "name": "Sample annotation (detailed)",
        "schema": [
            {
                "name": "general",
                "group": [
                    {
                        "name": "description",
                        "type": "basic:string:",
                        "label": "Description",
                        "required": False
                    },
                    {
                        "name": "species",
                        "type": "basic:string:",
                        "label": "Species",
                        "choices": [
                            {
                                "label": "Caenorhabditis elegans",
                                "value": "Caenorhabditis elegans"
                            },
                            {
                                "label": "Cricetulus griseus",
                                "value": "Cricetulus griseus"
                            },
                            {
                                "label": "Dictyostelium discoideum",
                                "value": "Dictyostelium discoideum"
                            },
                            {
                                "label": "Dictyostelium purpureum",
                                "value": "Dictyostelium purpureum"
                            },
                            {
                                "label": "Drosophila melanogaster",
                                "value": "Drosophila melanogaster"
                            },
                            {
                                "label": "Homo sapiens",
                                "value": "Homo sapiens"
                            },
                            {
                                "label": "Macaca mulatta",
                                "value": "Macaca mulatta"
                            },
                            {
                                "label": "Mus musculus",
                                "value": "Mus musculus"
                            },
                            {
                                "label": "Odocoileus virginianus texanus",
                                "value": "Odocoileus virginianus texanus"
                            },
                            {
                                "label": "Rattus norvegicus",
                                "value": "Rattus norvegicus"
                            },
                            {
                                "label": "Solanum tuberosum",
                                "value": "Solanum tuberosum"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ]
                    },
                    {
                        "name": "strain",
                        "type": "basic:string:",
                        "label": "Strain",
                        "hidden": "general.species != 'Mus musculus' && general.species != 'Rattus norvegicus'",
                        "required": False,
                        "description": "If using an animal model, this is strain information of that model, e.g. C57BL6,\nSprague Dawley, etc.\n"
                    },
                    {
                        "name": "genotype",
                        "type": "basic:string:",
                        "label": "Genotype",
                        "required": False,
                        "description": "Genotype of your sample, e.g. P53+/-, Tg2576, etc.\n"
                    },
                    {
                        "name": "biosample_type",
                        "type": "basic:string:",
                        "label": "Biosample type",
                        "choices": [
                            {
                                "label": "Cell line",
                                "value": "cell_line"
                            },
                            {
                                "label": "Tissue",
                                "value": "tissue"
                            },
                            {
                                "label": "Primary cell",
                                "value": "primary_cell"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ],
                        "required": False,
                        "description": "Source of samples/biological material, e.g. cell line, tissue, primary cell lines, etc.\n"
                    },
                    {
                        "name": "primary_cell_line",
                        "type": "basic:string:",
                        "label": "Primary cell line",
                        "hidden": "general.biosample_type != 'primary_cell'",
                        "required": False,
                        "description": "Search for your tissue type: http://www.ontobee.org/ontology/UBERON and enter the UBERON\nnumber e.g. thymus - UBERON:0002370.\n"
                    },
                    {
                        "name": "cell_line",
                        "type": "basic:string:",
                        "label": "Cell line",
                        "hidden": "general.biosample_type != 'cell_line'",
                        "required": False,
                        "description": "Name of your cell line, e.g. MF331, DAOY, etc."
                    },
                    {
                        "name": "cell_type",
                        "type": "basic:string:",
                        "label": "Cell type",
                        "required": False,
                        "description": "Type of cell, e.g. embryonic stem cell.\n"
                    },
                    {
                        "name": "organ",
                        "type": "basic:string:",
                        "label": "Organ / tissue",
                        "choices": [
                            {
                                "label": "Adipose tissue",
                                "value": "adipose_tissue"
                            },
                            {
                                "label": "Adrenal gland",
                                "value": "adrenal_gland"
                            },
                            {
                                "label": "Artery",
                                "value": "artery"
                            },
                            {
                                "label": "Blood",
                                "value": "blood"
                            },
                            {
                                "label": "Blood vessel",
                                "value": "blood_vessel"
                            },
                            {
                                "label": "Bodily fluid",
                                "value": "bodily_fluid"
                            },
                            {
                                "label": "Bone element",
                                "value": "bone_element"
                            },
                            {
                                "label": "Bone marrow",
                                "value": "bone_marrow"
                            },
                            {
                                "label": "Brain",
                                "value": "brain"
                            },
                            {
                                "label": "Breast",
                                "value": "breast"
                            },
                            {
                                "label": "Bronchus",
                                "value": "bronchus"
                            },
                            {
                                "label": "Connective tissue",
                                "value": "connective_tissue"
                            },
                            {
                                "label": "Embryo",
                                "value": "embryo"
                            },
                            {
                                "label": "Epithelium",
                                "value": "epithelium"
                            },
                            {
                                "label": "Esophagus",
                                "value": "esophagus"
                            },
                            {
                                "label": "Extraembryonic component",
                                "value": "extraembryonic_component"
                            },
                            {
                                "label": "Eye",
                                "value": "eye"
                            },
                            {
                                "label": "Gonad",
                                "value": "gonad"
                            },
                            {
                                "label": "Heart",
                                "value": "heart"
                            },
                            {
                                "label": "Intestine",
                                "value": "intestine"
                            },
                            {
                                "label": "Kidney",
                                "value": "kidney"
                            },
                            {
                                "label": "Large intestine",
                                "value": "large_intestine"
                            },
                            {
                                "label": "Limb",
                                "value": "limb"
                            },
                            {
                                "label": "Liver",
                                "value": "liver"
                            },
                            {
                                "label": "Lung",
                                "value": "lung"
                            },
                            {
                                "label": "Lymphatic vessel",
                                "value": "lymphatic_vessel"
                            },
                            {
                                "label": "Lymphoid tissue",
                                "value": "lymphoid_tissue"
                            },
                            {
                                "label": "Lymph node",
                                "value": "lymph_node"
                            },
                            {
                                "label": "Mammary gland",
                                "value": "mammary_gland"
                            },
                            {
                                "label": "Mouth",
                                "value": "mouth"
                            },
                            {
                                "label": "Musculature of body",
                                "value": "musculature_of_body"
                            },
                            {
                                "label": "Nerve",
                                "value": "nerve"
                            },
                            {
                                "label": "Nose",
                                "value": "nose"
                            },
                            {
                                "label": "Ovary",
                                "value": "ovary"
                            },
                            {
                                "label": "Pancreas",
                                "value": "pancreas"
                            },
                            {
                                "label": "Penis",
                                "value": "penis"
                            },
                            {
                                "label": "Pericardium",
                                "value": "pericardium"
                            },
                            {
                                "label": "Placenta",
                                "value": "placenta"
                            },
                            {
                                "label": "Prostate gland",
                                "value": "prostate_gland"
                            },
                            {
                                "label": "Skeleton",
                                "value": "skeleton"
                            },
                            {
                                "label": "Skin of body",
                                "value": "skin_of_body"
                            },
                            {
                                "label": "Small intestine",
                                "value": "small_intestine"
                            },
                            {
                                "label": "Spinal cord",
                                "value": "spinal_cord"
                            },
                            {
                                "label": "Spleen",
                                "value": "spleen"
                            },
                            {
                                "label": "Stomach",
                                "value": "stomach"
                            },
                            {
                                "label": "Testis",
                                "value": "testis"
                            },
                            {
                                "label": "Thymus",
                                "value": "thymus"
                            },
                            {
                                "label": "Thyroid gland",
                                "value": "thyroid_gland"
                            },
                            {
                                "label": "Trachea",
                                "value": "trachea"
                            },
                            {
                                "label": "Tongue",
                                "value": "tongue"
                            },
                            {
                                "label": "Uretar",
                                "value": "uretar"
                            },
                            {
                                "label": "Urinary bladder",
                                "value": "urinary_bladder"
                            },
                            {
                                "label": "Uterus",
                                "value": "uterus"
                            },
                            {
                                "label": "Vagina",
                                "value": "vagina"
                            },
                            {
                                "label": "Vasculature",
                                "value": "vasculature"
                            },
                            {
                                "label": "Vein",
                                "value": "vein"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            },
                            {
                                "label": "N/A",
                                "value": "na"
                            }
                        ],
                        "required": False
                    },
                    {
                        "name": "biosample_source",
                        "type": "basic:string:",
                        "label": "Biosample source",
                        "required": False,
                        "description": "General description of where your sample was derived from, e.g. osteosarcoma, vastus\nlateralis muscle, etc.\n"
                    },
                    {
                        "name": "growth_protocol",
                        "type": "basic:string:",
                        "label": "Growth protocol",
                        "required": False,
                        "description": "Describe the conditions that were used to grow or maintain organisms or cells prior to\nextract preparation.\n"
                    },
                    {
                        "name": "biosample_treatment",
                        "type": "basic:string:",
                        "label": "Biosample treatment",
                        "required": False,
                        "description": "If your sample was treated with a chemical agent search for the CHEBI number at\nhttps://www.ebi.ac.uk/chebi/, e.g. cisplatin, CHEBI:27899.\n"
                    },
                    {
                        "name": "treatment_protocol",
                        "type": "basic:string:",
                        "label": "Treatment protocol",
                        "required": False,
                        "description": "Describe how your sample was treated, at different timepoints, if using non-chemical\ntreatments e.g. exercise, aging, etc.\n"
                    },
                    {
                        "name": "annotator",
                        "type": "basic:string:",
                        "label": "Annotator",
                        "required": False,
                        "description": "Person who annotated the sample."
                    },
                    {
                        "name": "qc",
                        "group": [
                            {
                                "name": "status",
                                "type": "basic:string:",
                                "label": "Status",
                                "choices": [
                                    {
                                        "label": "Pass",
                                        "value": "PASS"
                                    },
                                    {
                                        "label": "Warning",
                                        "value": "WARNING"
                                    },
                                    {
                                        "label": "Fail",
                                        "value": "FAIL"
                                    }
                                ],
                                "required": False
                            },
                            {
                                "name": "message",
                                "type": "basic:string:",
                                "label": "Message",
                                "required": False
                            }
                        ],
                        "label": "Quality check"
                    }
                ],
                "label": "General"
            },
            {
                "name": "experiment",
                "group": [
                    {
                        "name": "assay_type",
                        "type": "basic:string:",
                        "label": "Assay type",
                        "choices": [
                            {
                                "label": "RNA-seq",
                                "value": "rna-seq"
                            },
                            {
                                "label": "ChIP-seq",
                                "value": "chip-seq"
                            },
                            {
                                "label": "ATAC-seq",
                                "value": "atac-seq"
                            },
                            {
                                "label": "ChIPmentation",
                                "value": "chipmentation"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ],
                        "required": False
                    },
                    {
                        "name": "extract_protocol",
                        "type": "basic:string:",
                        "label": "Extract protocol",
                        "required": False,
                        "description": "Describe the protocols used to extract and prepare the material to be sequenced.\n"
                    },
                    {
                        "name": "molecule",
                        "type": "basic:string:",
                        "label": "Library made from / Molecule",
                        "choices": [
                            {
                                "label": "Total RNA",
                                "value": "total_rna"
                            },
                            {
                                "label": "polyA RNA",
                                "value": "polya_rna"
                            },
                            {
                                "label": "Cytoplasmic RNA",
                                "value": "cytoplasmic_rna"
                            },
                            {
                                "label": "Nuclear RNA",
                                "value": "nuclear_rna"
                            },
                            {
                                "label": "Genomic DNA",
                                "value": "genomic_dna"
                            },
                            {
                                "label": "Protein",
                                "value": "protein"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ],
                        "required": False,
                        "description": "Select what molecule your samples are from, e.g. totalRNA, polyA RNA, genomic DNA, etc.\n"
                    },
                    {
                        "name": "library_depleted_in",
                        "type": "basic:string:",
                        "label": "Library depleted in",
                        "choices": [
                            {
                                "label": "rRNA",
                                "value": "rrna"
                            },
                            {
                                "label": "polyA mRNA",
                                "value": "polya_mrna"
                            },
                            {
                                "label": "N/A",
                                "value": "na"
                            }
                        ],
                        "required": False,
                        "description": "Select how your library was depleted, otherwise choose N/A.\n"
                    },
                    {
                        "name": "library_treatment",
                        "type": "basic:string:",
                        "label": "Library treatment",
                        "required": False,
                        "description": "Describe how your library was treated."
                    },
                    {
                        "name": "replication_type",
                        "type": "basic:string:",
                        "label": "Replication type",
                        "choices": [
                            {
                                "label": "Biological",
                                "value": "biological"
                            },
                            {
                                "label": "Isogenic",
                                "value": "isogenic"
                            },
                            {
                                "label": "Technical",
                                "value": "technical"
                            },
                            {
                                "label": "Sequencing",
                                "value": "sequencing"
                            },
                            {
                                "label": "Pseudoreplicate",
                                "value": "pseudoreplicate"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ],
                        "required": False,
                        "description": "Select what replication type you used. For more info, go to\nhttps://www.encodeproject.org/data-standards/terms/.\n"
                    },
                    {
                        "name": "platform",
                        "type": "basic:string:",
                        "label": "Platform",
                        "choices": [
                            {
                                "label": "NextSeq 500",
                                "value": "nextseq_500"
                            },
                            {
                                "label": "HiSeq 2500",
                                "value": "hiseq_2500"
                            },
                            {
                                "label": "HiSeq 2000",
                                "value": "hiseq_2000"
                            },
                            {
                                "label": "NovaSeq 6000",
                                "value": "novaseq_6000"
                            },
                            {
                                "label": "Other",
                                "value": "other"
                            }
                        ],
                        "required": False,
                        "description": "Select the platform used to sequence your samples."
                    },
                    {
                        "name": "chip_seq",
                        "group": [
                            {
                                "name": "target_of_assay",
                                "type": "basic:string:",
                                "label": "Target of assay",
                                "choices": [
                                    {
                                        "label": "Transcription factor",
                                        "value": "transcription_factor"
                                    },
                                    {
                                        "label": "Histone",
                                        "value": "histone"
                                    },
                                    {
                                        "label": "Control",
                                        "value": "control"
                                    },
                                    {
                                        "label": "Chromatin associated protein",
                                        "value": "chromatin_associated_protein"
                                    },
                                    {
                                        "label": "RNA binding protein",
                                        "value": "rna_binding_protein"
                                    },
                                    {
                                        "label": "Chromatin remodeller",
                                        "value": "chromatin_remodeller"
                                    },
                                    {
                                        "label": "Nucleotide modification",
                                        "value": "nucleotide_modification"
                                    },
                                    {
                                        "label": "Other",
                                        "value": "other"
                                    }
                                ],
                                "required": False,
                                "description": "Target in a ChIP-seq experiment, e.g. transcription factor, histone mark, etc.\n"
                            },
                            {
                                "name": "antibody_target",
                                "type": "basic:string:",
                                "label": "Antibody target",
                                "required": False,
                                "description": "Antigen that you are enriching for, e.g. Myc, H3K27AC, etc."
                            },
                            {
                                "name": "antibody_manufacturer",
                                "type": "basic:string:",
                                "label": "Antibody manufacturer",
                                "choices": [
                                    {
                                        "label": "Abcam",
                                        "value": "abcam"
                                    },
                                    {
                                        "label": "BioRad",
                                        "value": "biorad"
                                    },
                                    {
                                        "label": "ThermoFisher",
                                        "value": "thermofisher"
                                    },
                                    {
                                        "label": "CellSignal",
                                        "value": "cellsignal"
                                    },
                                    {
                                        "label": "Diagenode",
                                        "value": "diagenode"
                                    },
                                    {
                                        "label": "ActiveMotif",
                                        "value": "activemotif"
                                    },
                                    {
                                        "label": "Other",
                                        "value": "other"
                                    }
                                ],
                                "required": False,
                                "description": "Name of the vendor where the antibody used came from."
                            },
                            {
                                "name": "antibody_catalog_number",
                                "type": "basic:string:",
                                "label": "Antibody catalog number",
                                "required": False
                            },
                            {
                                "name": "antibody_lot_number",
                                "type": "basic:string:",
                                "label": "Antibody lot number",
                                "required": False
                            }
                        ],
                        "label": "ChIP-seq",
                        "hidden": "experiment.assay_type != 'chip-seq' && experiment.assay_type != 'chipmentation'"
                    }
                ],
                "label": "Experiment details"
            },
            {
                "name": "custom",
                "group": [
                    {
                        "name": "sex",
                        "type": "basic:string:",
                        "label": "Sex",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "age",
                        "type": "basic:integer:",
                        "label": "Age",
                        "required": False
                    },
                    {
                        "name": "passage",
                        "type": "basic:integer:",
                        "label": "Passage",
                        "required": False
                    },
                    {
                        "name": "xcag",
                        "type": "basic:integer:",
                        "label": "xCAG",
                        "required": False
                    },
                    {
                        "name": "group",
                        "type": "basic:string:",
                        "label": "Control/Experimenal group",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "rin",
                        "type": "basic:decimal:",
                        "label": "RIN",
                        "required": False
                    },
                    {
                        "name": "days_in_vitro",
                        "type": "basic:integer:",
                        "label": "Days in vitro",
                        "required": False
                    },
                    {
                        "name": "number_of_cells_per_pellet",
                        "type": "basic:integer:",
                        "label": "Number of cells per pellet",
                        "required": False
                    },
                    {
                        "name": "derivation",
                        "type": "basic:string:",
                        "label": "Derivation",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "sort_marker",
                        "type": "basic:string:",
                        "label": "Sort marker",
                        "default": "N/A",
                        "required": False
                    },
                    {
                        "name": "sort_percent",
                        "type": "basic:decimal:",
                        "label": "Sort percent (for marker of interest)",
                        "required": False
                    },
                    {
                        "name": "sort_date",
                        "type": "basic:date:",
                        "label": "Sort date",
                        "default": "1900-01-01",
                        "required": False
                    }
                ],
                "label": "Additional properties"
            }
        ],
        "slug": "sample-detailed",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    },
    {
        "created": "2022-09-21T03:17:16.477906+0000",
        "id": 104,
        "modified": "2022-09-21T03:17:16.477929+0000",
        "contributor": {
            "first_name": "Adi",
            "id": 2,
            "last_name": "Genialis",
            "username": "admin"
        },
        "version": "1.0.0",
        "description": "Annotation schema for dictyExpress time series experiments.",
        "name": "dictyExpress time series",
        "schema": [
            {
                "name": "project",
                "type": "basic:string:",
                "label": "Project",
                "required": False
            },
            {
                "name": "citation",
                "type": "basic:url:view:",
                "label": "Citation",
                "required": False
            },
            {
                "name": "details",
                "type": "basic:string:",
                "label": "Details",
                "required": False
            },
            {
                "name": "strain",
                "type": "basic:string:",
                "label": "Strain",
                "required": False
            },
            {
                "name": "growth",
                "type": "basic:string:",
                "label": "Growth",
                "required": False
            },
            {
                "name": "treatment",
                "type": "basic:string:",
                "label": "Treatment",
                "required": False
            }
        ],
        "slug": "dicty-time-series",
        "current_user_permissions": [
            {
                "type": "public",
                "permissions": [
                    "view"
                ]
            }
        ]
    }
]