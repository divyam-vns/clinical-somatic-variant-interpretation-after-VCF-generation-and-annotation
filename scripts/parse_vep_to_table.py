
import argparse
import vcf

def main():

    p = argparse.ArgumentParser()

    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)

    args = p.parse_args()

    vc = vcf.Reader(filename=args.input)

    with open(args.output, 'w') as out:

        out.write(
            'chrom\tpos\tref\talt\teffects\tclin_sign\n'
        )

        for rec in vc:

            ann = rec.INFO.get('CSQ') or rec.INFO.get('ANN')

            if ann is None:
                effects = '.'
            elif isinstance(ann, list):
                effects = ';'.join(map(str, ann))
            else:
                effects = str(ann)

            clin_sig = rec.INFO.get('CLIN_SIG', '.')

            out.write(
                f"{rec.CHROM}\t"
                f"{rec.POS}\t"
                f"{rec.REF}\t"
                f"{rec.ALT[0]}\t"
                f"{effects}\t"
                f"{clin_sig}\n"
            )

if __name__ == '__main__':
    main()
