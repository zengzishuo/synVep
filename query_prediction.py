import sqlite3
import os
import sys

#############################################
###### functions to parse input files  ######
#############################################

def read_bed(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    chr = []
    pos1 = []
    pos2 = []
    ref = []
    alt = []
    for i in lines:
        splits = i.split('\t')
        if len(splits) <3 or len(splits) >5:
            print('ignoring lines that are not [chr pos pos] or [chr pos pos ref alt] (tab-separated)')
            continue
        else:
            chr.append(splits[0])
            pos1.append(splits[1])
            pos2.append(splits[2])
            if len(splits) == 5:
                ref.append(splits[3])
                alt.append(splits[4])
            else:
                ref.append('')
                alt.append('')
    return chr, pos1, pos2, ref, alt


def read_plain_text_list(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    L = []
    for l in lines:
        L.append(l.split('\n')[0])
    return L

def read_vcf(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    chr = []
    pos = []
    ref = []
    alt = []
    for l in lines:
        if l[0] == '#':
            continue
        else:
            splits = l.split('\t')
            if len(splits) >= 5:
                chr.append(splits[0])
                pos.append(int(splits[1]))
                ref.append(splits[3])
                alt.append(splits[4])
            else:
                chr.append(splits[0])
                pos.append(int(splits[1]))
                ref.append(splits[3])
                alt.append(splits[4].split('\n')[0])
    return chr, pos, ref, alt

##########################################
###### functions to query database  ######
##########################################

def query_vcf(chrs, positions, refs, alts, cur):
    res = []
    for i in range(len(chrs)):
        query = 'SELECT * FROM VARIANT_SCORE WHERE chr="' + chrs[i]+ '" AND pos=' +str(positions[i])+' AND ref="' +refs[i]+ '" AND alt="' +alts[i]+ '";'
        cur.execute(query)
        rows = cur.fetchall()
        res.append(rows)
    return res


def query_hgnc(hgnc_genes, cur):
    res = []
    for i in hgnc_genes:
        query = 'SELECT * FROM VARIANT_SCORE WHERE HGNC_gene_symbol="' + i + '";'
        cur.execute(query)
        rows = cur.fetchall()
        res.append(rows)
    return res

# def query_uniprot(uniprot_genes, cur):
#     res = []
#     for i in uniprot_genes:
#         query = "SELECT * FROM VARIANT_SCORE WHERE UniProt_gene_symbol='" + i + "';"
#         cur.execute(query)
#         rows = cur.fetchall()
#         res.append(rows)
#     return res

def query_dbsnp(dbSNPs, cur):
    res = []
    for i in dbSNPs:
        query = 'SELECT * FROM VARIANT_SCORE WHERE dbSNP_ID="' + i + '";'
        cur.execute(query)
        rows = cur.fetchall()
        res.append(rows)
    return res

# def query_genomic_coord(chrs, positions, cur):
#     res = []
#     for i in range(len(chrs)):
#         query = 'SELECT * FROM VARIANT_SCORE WHERE chr="' + chrs[i]+ '" AND pos=' +str(positions[i])+ ';'
#         cur.execute(query)
#         rows = cur.fetchall()
#         res.append(rows)
#     return res

def query_bed(chr, pos1, pos2, ref, alt, cur):
    res = []
    for i in range(len(chr)):
        if ref[i] != '' and alt[i] != '':
            query = "SELECT * FROM VARIANT_SCORE WHERE chr='" + chr[i] + "' AND pos=" + str(pos1[i]) + " AND ref='" + ref[i] + "' AND alt='" + alt[i] + "';"
        else:
            query = "SELECT * FROM VARIANT_SCORE WHERE chr='" + chr[i] + "' AND pos>=" + str(pos1[i]) + " AND pos<=" + str(pos2[i]) + ";"
        cur.execute(query)
        rows = cur.fetchall()
        res.append(rows)
    return res



def get_predictions(mode, input):
    '''
    :param mode (input format): vcf (VCF file), dbSNP_ID (a list in txt file),
                HGNC_gene_symbol (a list in txt file), UniProt_gene_symbol (a list in txt file)
                genomic coordinate (single query, a string. e.g., 16:2812365)
    :return: a data table with predictions in txt format with name designated in param output
    '''
    ###connect to sqlite database
    conn = sqlite3.connect('synvep_database.db')
    cur = conn.cursor()
    ###
    if mode not in ['bed', 'vcf','dbsnp','gene']:
        raise TypeError('mode should be one of the following: bed, vcf, dbsnp, gene')
    elif mode == 'vcf':
        chrs, positions, refs, alts = read_vcf(input)
        out = query_vcf(chrs, positions, refs, alts, cur)
        return out
    elif mode == 'dbsnp':
        L = read_plain_text_list(input)
        out = query_dbsnp(L, cur)
        return out
    elif mode == 'gene':
        L = read_plain_text_list(input)
        out = query_hgnc(L, cur)
        return out
    elif mode == 'bed':
        chrs, positions1, positions2, refs, alts = read_bed(input)
        out = query_bed(chrs, positions1, positions2, refs, alts, cur)
        return out



print('starting query ...')

args = sys.argv

if len(args) < 4:
    print('please specify mode, input, and output')

Mode = args[1]
Input = args[2]
Output = args[3]

sys.stdout = open(os.devnull, 'w')

result = get_predictions(Mode, Input)

with open(Output, 'w') as f:
    if '.csv' in Output:
        f.write('transcript_ID,transcript_position,codon_mutation,chr,genomic_position,ref,alt,strand,class,HGNC_gene_symbol,dbSNP_ID,GRCh38_genomic_position,synVep\n')
        for L in result:
            for l in L:
                l = list(l)
                synvep = l[8]
                l.pop(8)
                f.write(','.join(str(s) for s in l) + ',' + str(round(float(synvep), 4)) + '\n')
    else:
        f.write('transcript_ID\ttranscript_position\tcodon_mutation\tchr\tgenomic_position\tref\talt\tstrand\tclass\tHGNC_gene_symbol\tdbSNP_ID\tGRCh38_genomic_position\tsynVep\n')
        for L in result:
            for l in L:
                l = list(l)
                synvep = l[8]
                l.pop(8)
                f.write('\t'.join(str(s) for s in l) + '\t' + str(round(float(synvep), 4)) + '\n')


sys.stdout = sys.__stdout__

f.close()

print('done')
