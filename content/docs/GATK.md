---
title: Genome Analysis Toolkit (GATK) Variant Calling
type: docs
sidebar:
  open: true
---

## 1. Index reference genome
GATK requires two files to access information in the genome reference file:
1. an index file that provides information on the exact location of a particular reference base within a `.fasta` file (`bwa` or `samtools`)
2. a dictionary of the contig names and sizes (`picard`)

These files need to be generate prior to analysis for `GATK` to use a `.fasta` file as reference. `GATK` automatically looks for these files when passed the reference information, and thus, the names of these files are expected to following the same convention as the reference name.

```bash
REFDIR="path/genome"
REFNAME="reference.fasta"
BASENAME=${REFNAME%.fasta}

##Generate the BWA index
bwa index ${REFDIR}/${REFNAME}

##Generate the fasta file index
samtools faidx ${REFDIR}/${REFNAME}

##Generate the sequence dictionary
java -jar /programs/picard-tools-2.19.2/picard.jar CreateSequenceDictionary \
REFERENCE=${REFDIR}/${REFNAME} \
OUTPUT=${REFDIR}/${BASENAME}.dict
```

## 2. Mapping data to a reference genome
The `BWA-MEM` algorithm is used to align input reads to the reference genome. BWA-MEM is recommended because it can accommodate longer sequence reads (>70bp), is typically faster and more accurate than other aligners, and supports both paired-end and split-read alignments. Alignments are piped directly to `samtools` where they are converted into sorted, compressed `.bam` files. The read group information is required for all downstream analysis provides important meta-data about the sample(s). Read group tags can include multiple fields but the minimum information includes:
- `ID` – unique string specific to a given run
- `SM` – the name associated with the DNA sample 
- `LB` – library from which the DNA was sequenced
- `PL` – the platform used
- `PU` – the platform unit identifier for the run

```bash
# Global variables
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
THREADS="12"
COMPRESS="9"

#Read group information
ID="unique.id"
SAMPLE="sample.name"
LIBRARY="library.name"
PLATFORM="Illumina"
UNIT="NovaSeq6000"

bwa mem -C -M -t 12 ${REFDIR}/${REFNAME} \
${INDIR}/${FILENAME}_R1.fastq.gz \
${INDIR}/${FILENAME}_R2.fastq.gz \
-R "@RG\tID:${ID}\tSM:${SAMPLE}\tLB:${LIBRARY}\tPL:${PLATFORM}\tPU:${UNIT}" |
samtools view -bh - | samtools sort -@ ${THREADS} -l ${COMPRESS} -o ${OUTDIR}/${FILENAME}.sorted.bam -
```

## 3. Marking Duplicates
Duplicate reads introduced either during library preparation (i.e., PCR duplicates) or when read from a single amplification cluster incorrectly detected as multiple clusters by the optical sensor in the sequencer (i.e., optical duplicates) need to be identified and tagged. The `MarkDuplicates` algorithm can accommodate clipped and gapped alignments produced by BWA-MEM and duplicate marking is accomplished using the unique molecular barcodes (i.e., BX tags) applied to each sample. The identified duplicates are assigned the hexadecimal value of `0x0400`, which corresponds to a decimal value of `1024`. The program accepts coordinate-sorted bam files, but when run in this configuration the unmapped mates of mapped records and supplementary/secondary alignments are not marked as duplicates. `MarkDuplicates` also produces a metrics file which provides summary information about the numbers of duplicates for the paired-end input files

```bash
INDIR="directory/path"
FILENAME="file.name"
BASENAME=${FILENAME%.sorted.bam}
OUTDIR="directory/path"
       
java -jar /programs/picard-tools-2.19.2/picard.jar MarkDuplicates \
I=${INBAM}/${FILENAME} \
O=${OUTBAM}/${BASENAME}.pMarkdup.bam \
M=${OUTBAM}/${BASENAME}.pMarkdup.metrics \
ASSUME_SORT_ORDER=coordinate \
CREATE_INDEX=TRUE \
READ_ONE_BARCODE_TAG=BX \
READ_TWO_BARCODE_TAG=BX \
VALIDATION_STRINGENCY=LENIENT 
```

## 4. Alignment Quality Assessment/Control
The quality of the alignment can be examined using `qualimap bamqc`, which provides a number of useful graphs summarizing basic statistics of the alignment. The principle metrics include mean and standard deviation of coverage, mean GC content, mean insert size and mean mapping qualities. Other metrics include: coverage across reference, coverage histogram, genome fraction coverage, duplication rate histogram, mapped reads GC content, mapped reads GC content distribution, mapped reads clipping profile, mapping quality across reference, mapping quality histogram, and, if applicable, insert size across reference and insert size histogram. The BAM file are required to be sorted by chromosomal coordinates.

```bash
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory.name"

/programs/qualimap_v2.2.1/qualimap bamqc -nt 8 -bam ${INDIR}/${FILENAME} -outdir ${OUTDIR}
```

## .5 Merge SAM Files
Samples sequenced on separate lanes need to be combine into a single file prior to variant calling. It is critical to identify/label read groups appropriately to prevent errors in downstream processing. If samples run on different lanes contain identical read group IDs, the tool will avoid conflicts by modifying the read group IDs to be unique.

```bash
INDIR="directory/path"
INFILE01="file.name01"
INFILE02="file.name02"
INFILE03="file.name03"
INFILE04="file.name04"
OUTDIR="directory/path"
OUTNAME="file.name"

java -jar /programs/picard-tools-2.19.2/picard.jar MergeSamFiles \
INPUT=${INDIR}/${INFILE01}.pMarkdup.bam \
INPUT=${INDIR}/${INFILE02}.pMarkdup.bam \
INPUT=${INDIR}/${INFILE03}.pMarkdup.bam \
INPUT=${INDIR}/${INFILE04}.pMarkdup.bam \
O=${OUTDIR}/${OUTNAME}.pMarkdup.bam
```

## 6. Haplotype Calling
Calling SNPs and indels is performed simultaneously via local de-novo assembly of haplotypes using the `HaplotypeCaller` tool. The program identifies ‘active’ regions of the genome based on the presence of sequence variation and then realigns each haplotype within these regions against the reference haplotype using the Smith-Waterman algorithm to identify potentially variant sites. This approach allows more accurate calling of SNPs and indels in regions where these different types of variants are close to each other. `HaplotypeCaller` generate intermediate GVCF files for joint genotyping of multiple samples and should not to be used in final analysis.

```bash
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
OUTNAME="file.name"

/programs/gatk4/gatk --java-options "-Xmx4G" HaplotypeCaller \
-R ${REFDIR}/${REFNAME} \
-I ${INDIR}/${FILENAME} \
-O ${OUTDIR}/${OUTNAME}_variants.g.vcf \
-ERC GVCF
```

## 7. Combine Multiple Lanes
The per-sample gVCF files need to be combined into a multi-sample gVCF file using the `CombineGVCFs` tool. The merged GVCFs are then used to simultaneously genotype multiple individuals. This approach is recommended when there are few samples to merge but for much larger sample sizes GenomicsDBImport may be preferred.

```bash
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
INFILE01="file.name01"
INFILE02="file.name02"
INFILE03="file.name03"
OUTDIR="directory/path"
OUTNAME="file.name"

/programs/gatk4/gatk --java-options "-Xmx4G" CombineGVCFs \
-R ${REFDIR}/${ REFNAME } \
-V ${INDIR}/${INFILE01}_variants.g.vcf \
-V ${INDIR}/${INFILE02}_variants.g.vcf \
-V ${INDIR}/${INFILE03}_variants.g.vcf \
-O ${OUTDIR}/${OUTNAME}_combine.g.vcf.gz
```

## 8 Genotype Combine File
The `GenotypeGVCFs` tool is used to perform joint genotyping on a single GVCF input, which may contain one or many samples. The input samples must contain genotype likelihoods produced by HaplotypeCaller with `-ERC GVCF` option.

```bash
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
OUTNAME="file.name"

/programs/gatk4/gatk --java-options "-Xmx4G" GenotypeGVCFs \
-R ${REFDIR}/${REFNAME} \
-V ${INDIR}/${FILENAME}_combine.g.vcf.gz \
-O ${OUTDIR}/${OUTNAME}_variants.vcf.gz
```

## 9. Subset SNPs/Indels-only
SNPs or indels need to be split into separate VCF files, because these different classes of variation require different metrics to assess whether they are real or artifactual. Moreover, it is not possible to apply the `VariantFiltration` tool selectively to only one class of variants, and thus, the filtering process need to be run separately on SNPs and indels

```bash
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
OUTNAME="file.name"

##Subset to SNPs-only callset
/programs/gatk4/gatk --java-options "-Xmx4G" SelectVariants \
-R ${REFDIR}/${REFNAME} \
-V ${INDIR}/${FILENAME} \
-select-type SNP \
-O ${OUTDIR}/${OUTNAME}_snps.vcf.gz

##Subset to indels-only callset
/programs/gatk4/gatk --java-options "-Xmx4G" SelectVariants \
-R ${REFDIR}/${REFNAME} \
-V ${INDIR}/${FILENAME} \
-select-type INDEL \
--O ${OUTDIR}/${OUTNAME}_indels.vcf.gz
```

## 10. Filter SNPs & Indels
Hard-filtering is required when panels of know variants are not available for a given study organism, and thus, requires manual filtering. Filtering based on sample-level annotations, i.e. `FORMAT` field annotations, consists of choosing specific thresholds for one or more annotation metric and throwing out any variants that have annotation values above or below the set thresholds. The program will specify which parameter was chiefly responsible for the exclusion of the SNP using the culprit annotation. SNPs that do not match any of these conditions will be considered good and marked `PASS` in the output VCF file. Possible filters include (but not limited to):
- `QD` - variant confidence divided by the unfiltered depth
- `QUAL` - variant confidence
- `SOR` - strand bias estimated by the symmetric odds ratio test
- `FS` - Fisher’s Exact Test to detect strand bias
- `MQ` - root mean square of read mapping quality across all samples
- `MQRankSum` - u-based z-approximation from the Mann-Whitney Rank Sum Test for the distance from the end of the read for reads with the alternate allele
- `ReadPosRankSum` - u-based z-approximation from the Mann-Whitney Rank Sum Test for mapping qualities

```bash
# Global variables
REFDIR="genome/path"
REFNAME="reference.fasta"
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
OUTNAME="file.name"

## Hard-filter snps
/programs/gatk4/gatk --java-options "-Xmx4G" VariantFiltration \
-R ${REFDIR}/${REFNAME} \
-V ${INDIR}/${FILENAME}_snps.vcf.gz \
-O ${OUTDIR}/${OUTNAME}_snps_filtered.vcf.gz \
-filter "QD < 2.0" --filter-name "QD2" \
-filter "QUAL < 30.0" --filter-name "QUAL30" \
-filter "SOR > 3.0" --filter-name "SOR3" \
-filter "FS > 60.0" --filter-name "FS60" \
-filter "MQ < 40.0" --filter-name "MQ40" \
-filter "MQRankSum < -12.5" --filter-name "MQRankSum-12.5" \
-filter "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8"

## Hard-filter indels
/programs/gatk4/gatk --java-options "-Xmx4G" VariantFiltration \
-R ${REFDIR}/${REFNAME} \
-V ${INDIR}/${FILENAME}_indels.vcf.gz \
-O ${OUTDIR}/${OUTNAME}_indels_filtered.vcf.gz \
-filter "QD < 2.0" --filter-name "QD2" \
-filter "QUAL < 30.0" --filter-name "QUAL30" \
-filter "FS > 200.0" --filter-name "FS200" \
-filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20"
```

## 11. Subset Filtered Genotypes

```bash
# Global variables
INDIR="directory/path"
FILENAME="file.name"
OUTDIR="directory/path"
OUTNAME="file.name"

bcftools view -i 'FILTER="PASS"' ${INDIR}/${FILENAME}_snps_filtered.vcf.gz  > ${OUTDIR}/${OUTNAME}_snps_filtered_passed.vcf.gz
```
