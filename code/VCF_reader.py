import vcf
import requests
import argparse


def rest_query(query):
    try:
        r = requests.get(query, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
    except:
        try:
            r = requests.get(query[:-2] + "?", headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
        except:
            raise Exception('API query not found {}'.format(query))
    decoded = r.json()
    return decoded


def get_exac_allele_freq(record):
    server = "http://exac.hms.harvard.edu/"
    ext = "/rest/variant/variant/"
    variant = "-".join(map(str, [record.CHROM, record.POS, record.REF, record.ALT[0]]))
    query = server + ext + variant
    decoded = rest_query(query)
    if 'allele_freq' in decoded:
        freq = decoded['allele_freq']
    else:
        freq = "NA"
    return freq


def get_vep_consequence(record):
    server = "https://grch37.rest.ensembl.org"
    ext = "/vep/human/region/"
    # vcf is unphased so ref/alt will always refer to forward strand
    variant = "%s:%s-%s:1/%s?" % (record.CHROM, record.POS, record.POS + 1, record.ALT[0])
    query = server + ext + variant
    decoded = rest_query(query)
    if 'most_severe_consequence' in decoded[0]:  # what happens if this isn't just a list of one element
        consequence = decoded[0]["most_severe_consequence"]
    else:
        consequence = "NA"
    return consequence


def main():
    parser = argparse.ArgumentParser(description='Annotate VCF.')
    parser.add_argument('vcf', metavar='vcf', type=str, help='vcf filename')
    parser.add_argument('tsv', metavar='tsv', type=str, help='tsv filename')
    args = parser.parse_args()
    vcf_file = args.vcf
    tsv_file = args.tsv
    vcf_reader = vcf.Reader(open(vcf_file, 'r'))
    tsv = open(tsv_file, 'w')
    header = ["chrom", "position", "ref", "alt", "number of reads", "percent of reads", "exac freq",
              "consequence", "type", "\n"]
    tsv.write("\t".join(map(str, header)))
    for record in vcf_reader:
        number_of_reads = int(record.INFO['AO'][0])
        percentage_reads_supporting_variant = (float(record.INFO['AO'][0]) / record.INFO['DP'])
        freq = get_exac_allele_freq(record)
        consequence = get_vep_consequence(record)
        # only considers first alternative allele per record
        collect_row = [record.CHROM, record.POS, record.REF, record.ALT[0], number_of_reads,
                       percentage_reads_supporting_variant, freq, consequence, record.INFO["TYPE"][0], "\n"]
        tsv.write("\t".join(map(str, collect_row)))
    tsv.close()


if __name__ == "__main__":
    main()
