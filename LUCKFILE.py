from luck.shorts import LSC, TSSR, NCR, RNS, DNS

'''
1. genome.fasta
2. genome.fasta.fai (which is genome.sizes)
3. bowtie2 index
4. gtf and gff3 data for annotation to put into IGV
5. genepred for annotation. genepred is better than gtf and gff3 for transcriptome annotation.
'''


ns = RNS()
config = DNS()
config.version        = '0.0.1'
config.url_genome     = "ftp://ftp.ensemblgenomes.org/pub/plants/release-47/fasta/oryza_sativa/dna/Oryza_sativa.IRGSP-1.0.dna.toplevel.fa.gz"
config.url_gff3       = "ftp://ftp.ensemblgenomes.org/pub/plants/release-47/gff3/oryza_sativa/Oryza_sativa.IRGSP-1.0.47.gff3.gz"
threads = 2

requires = 'curl gzip'

TSSR.MWF(ns,
'install-deps.txt',
None,	
'''
{{
set -eux
which curl
which conda
which gzip
#conda install -y -c conda-forge -c bioconda ucsc-gff3togenepred==377--h199ee4e_0
conda install -y -c bioconda/label/cf201901 ucsc-gff3togenepred
conda install -y -c bioconda/label/cf201901 ucsc-genepredtogtf
conda install -y -c bioconda/label/cf201901 samtools 
conda install -y -c bioconda/label/cf201901 bowtie2 
}} > {c.o[0]}
'''
)



TSSR.MWF(ns,
	'genome.fa',
	None,
	'''
	curl -sL {config.url_genome} | gzip -d  > {c.o[0]}.temp
	mv {c.o[0]}.temp {c.o[0]}
	'''
)

TSSR.MWF(ns,
	'genome.fa.sizes',  ### in most cases, you can just use *.fa.fai instead, even for bedtools
	'genome.fa.fai',
	'''
	cat {c.i[0]} | cut -d$'\t' -f1-2 > {c.o[0]}
	'''
	)

TSSR.MWF(ns, 
	'genome.fa.fai',
	'genome.fa install-deps.txt',
	'samtools faidx genome.fa')

TSSR.MWF(ns,
	'bowtie2-index.1.bt2',
	'install-deps.txt',
	'bowtie2-build --threads 2 --seed 0 genome.fa bowtie2-build'
	)

TSSR.MWF(ns,
	'genome.gff3', ## output
	None,          ## input
	'''            ## command
	curl -sL {config.url_gff3} | gzip -d > {c.o[0]}.temp
	mv {c.o[0]}.temp {c.o[0]}  ## {c.o[0]} get replaced into genome.gff3 which is the output[0]
	'''
	)
TSSR.MWF(ns,
	'genome.genepred genome.gtf',
	'genome.gff3 install-deps.txt',
	'''
	gff3ToGenePred genome.gff3 genome.genepred
	genePredToGtf file genome.genepred genome.gtf
	''')

NCR.MWF(ns,
	'build',
	'genome.fa genome.fa.fai genome.fa.sizes '
	'bowtie2-index.1.bt2 genome.gff3 genome.gtf genome.genepred '
	)

NCR.MWF(ns,'clean', 'rm -rf -- !(LUCKFILE.py)')