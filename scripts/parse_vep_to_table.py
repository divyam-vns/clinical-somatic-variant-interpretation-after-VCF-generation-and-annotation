import argparse
import vcf  # PyVCF/npm install via requirements

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()

    vc = vcf.Reader(filename=args.input)
    with open(args.output, 'w') as out:
        out.write('chrom\tpos\tref\talt\teffects\tclin_sign\tnoncoding\n')
        for rec in vc:
            ann = rec.INFO.get('CSQ') or rec.INFO.get('ANN')
            effects = ';'.join(ann)
            clin_sig = rec.INFO.get('CLIN_SIG','.')
            out.write(f"{rec.CHROM}\t{rec.POS}\t{rec.REF}\t{rec.ALT[0]}\t{effects}\t{clin_sig}\n")

if __name__=='__main__':
    main()
