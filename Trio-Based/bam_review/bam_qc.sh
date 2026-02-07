#!/bin/bash

REGION=$1
BAM=$2

samtools depth -r $REGION $BAM
samtools mpileup -r $REGION -Q 20 -q 30 $BAM

# Example
bash bam_qc.sh chr2:166187838 proband.bam
