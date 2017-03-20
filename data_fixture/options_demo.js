options = {
    palette: ["#00A0B0", "#6A4A3C", "#CC333F", "#EB6841"],
    locus: "7:55,085,725-55,276,031",

    reference: {
        id: "hg19",
        fastaURL: "//igv.broadinstitute.org/genomes/seq/1kg_v37/human_g1k_v37_decoy.fasta",
        cytobandURL: "//igv.broadinstitute.org/genomes/seq/b37/b37_cytoband.txt"
    },

    trackDefaults: {
        bam: {
            coverageThreshold: 0.2,
            coverageQualityWeight: true
        }
    },

    tracks: [
        {
            name: "Genes",
            url: "//igv.broadinstitute.org/annotations/hg19/genes/gencode.v18.collapsed.bed",
            index: "//igv.broadinstitute.org/annotations/hg19/genes/gencode.v18.collapsed.bed.idx",
            displayMode: "EXPANDED"
        }
    ]
};