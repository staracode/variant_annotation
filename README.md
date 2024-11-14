## Annotate VCF

Annotate variant VCF file with the following:

1. Read depth.
2. Number of reads supporting alternative allele. 
2. Percent reads that support alternative allele over total reads. 
3. [ExAC](http://exac.hms.harvard.edu/) frequency. 
4. Most severe onsequence annotation using [VEP API] (https://rest.ensembl.org)
5. Variant type (substitution, insertion, CNV, etc.). 
 
link to repository: https://bitbucket.org/stara/variant_annotation/src/master/

---

# Example usage: 
python code/VCF_reader.py data/Challenge_data_\(1\).vcf output/final_output.txt

My personal laptop is still using python 2.7 so that is what I used.  

python --version 

Python 2.7.14 :: Anaconda, Inc.

package requirements listed in requirements.txt
