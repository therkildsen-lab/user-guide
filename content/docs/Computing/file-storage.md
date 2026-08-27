---
title: File Storage
type: docs
sidebar:
  open: true
---

## Best practices for file storage
We all share the same computing resources. Genomic data is massive and has significant storage requirements, so we need to work together and apply best practices for sustainable long-term computing. This document serves to define agreed-upon standards for data management on the servers. The document is broken down into two sections, one describing best-practices for file management during an active project, and the second describing best-practices for archiving inactive projects.
### General guidelines
Regardless of whether a project is active or archived, there is a core set of principles that should be followed regarding the main genomic data types. It should be noted that exceptions to this would be software incompatibilities with compressed data.

| file type | how to store |
|:----|:----|
| GFF | compressed with gzip |
| FASTQ | compressed with gzip or bgzip |
| Alignments | BAM or CRAM format |
| Variant Call Format | BCF format|
| BED | compressed with gzip |
| Misc text files > 200Mb | compressed with gzip | 

### Active Project Guidelines
During an active project, the core data tends to be the raw FASTQ files, BAM alignments, and resulting VCF/BCF variant call files. These files should adhere to the compression recommendations of the [General Guidelines](#general-guidelines).
- A buildup of large (1Gb+) intermediate files is not recommended– keep diagnostic files to assist in troubleshooting, but do not keep reams of large intermediate files, especially if an analysis can be rerun relatively quickly (<1 day).
- Do not keep large output files from folders that were created while exploring the parameter space and yielded unsatisfactory outcomes.
- Do not keep large intermediate variant call files– keep the initial VCF/BCF resulting from variant calling and the final few VCF/BCF files from variant filtering.
- Double-check why there might be large (>1Gb) plaintext files in your project, whether you need them, and, if so, if you can gzip them.
- If sequences were mapped and will not require additional mapping or involvement in your pipeline, you should remove the FASTQ files (assuming they are already archived).

### Project Archiving
#### Sequence Data
The FASTQ sequences of an archived project should be stored:
1. On NCBI
2. If stored locally, in CRAM format
The CRAM format will preserve FASTQ header comments (liked haplotagging information) and result in a single file for each sample (even if paired-end). Conversion between CRAM and FASTQ is lossless and trivial using samtools.

#### Reference Data
If a reference genome was required, it must be archived as a gzipped FASTA file in the archived project directory. If the reference genome is available on NCBI, then local archiving is not necessary.

#### Alignment Data
Alignment data (SAM/BAM/CRAM) should not be archived for a project, as it can be regenerated using the archived FASTQ files and the correct reference genome.

#### Variant Data
Only the final filtered variant data (VCF/BCF) should be archived, and only in BCF format.

#### Metadata
All relevant metadata for a project should be archived. This includes specimen information like sex, morphometrics, year of capture, sample name explanations, location of capture, etc. Essentially, any metadata relevant to getting from FASTQ data to final filtered variant data should be archived.

