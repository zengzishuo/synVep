##############################
## About this application   ##
##############################

* We built a model to evaluate the effects of human synonymous variants, and we used this model to
precompute all possible human synonymous variants. All these predictions are stored in a SQL database called'synvep_database.db'. 

* Reference genome assembly for query is GRCh37 (hg19), GRCh38 (hg38) genomic positions are also returned as part of the result.

* This application retrieves precomputed prediction score for you from your query.

* This application is built in Python 3.


###################################
## How to use this application?  ##
###################################

* Dependencies: python (version 3) 

* Download 'query_prediction.py' from github, download 'synvep_database.db' from xxxxxxxxx

* Place 'query_prediction.py', 'synvep_database.db' in the same directory.

* This application takes five different formats as inputs: "vcf" (VCF file), "gene" (HGNC gene symbol),  "dbsnp" (dbSNP ID), and "bed" (BED format).


* Command line should be as follows:

python query_prediction.py <FORMAT> <INPUT_FILE> <OUTPUT_FILE>

If <OUTPUT_FILE> contains '.csv' as extension, a CSV result file will be generated; otherwise, a tab-separated file will be generated.

For example, if your input format is "vcf", then the command should be

python query_prediction_program.py vcf sample_vcf.txt result1.csv


Similarly, if your input format is "dbSNP_ID", just change "vcf" to "dbSNP_ID", as well as the input file, in the command line:

python query_prediction.py bed sample_bed_format.txt result2

python query_prediction.py dbsnp sample_dbSNP_ID.txt result3

python query_prediction.py gene sample_gene.txt result4


* note that "python" should be aliased with python version 3.


#############################################
## How to interpret the predicted scores?  ##
#############################################

* Predicted scores range from 0 to 1, which represents the likelihood of a variant having an effect (we assume effects are mostly deleterious).


################################################
## Why there is no prediction for my input?  ###
################################################

* It's possible that the reference allele of your input does not match the reference genome on that position.

* It's possible that the variant-bearing transcript did not pass our quality control (e.g., with patched chromosome symbol, no starting/ending codon, etc.).


* The vcf file should have at least 5 columns: CHROM, POS, ID (optional, if missing, use '.' as place holder), REF, and ALT. The column name row should be headed with "#". More columns are allowed but will not be considered. Entries in a row are separated by tab. Ref and Alt allele in the vcf file should be capital letter. For more information about vcf file format, please visit https://samtools.github.io/hts-specs/VCFv4.2.pdf. 


####################
## Online query  ###
####################
We provide an online server to process your query: xxxxxxxxxxxx.


#########################
## Other information  ###
#########################

* If you have any question about this application, or want to report a bug, please contact: zzeng@bromberglab.org

* If you use this application or the predictions in published research, please cite:
xxxxxxxxx (to be filled)

* License: MIT






