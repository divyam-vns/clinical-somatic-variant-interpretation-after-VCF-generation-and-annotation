region = "chr2:166187738-166187938"

with open("bam_review/igv_batch.txt", "w") as f:
    f.write(f"""
new
genome hg38
load input/proband.bam
load input/father.bam
load input/mother.bam
snapshotDirectory bam_review/snapshots
goto {region}
sort base
collapse
snapshot variant.png
exit
""")
