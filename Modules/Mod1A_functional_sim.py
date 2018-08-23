from MyGene.mygene_client import QueryMyGene
from ontobio.ontol_factory import OntologyFactory
from ontobio.io.gafparser import GafParser
from ontobio.assoc_factory import AssociationSetFactory
from ontobio.assocmodel import AssociationSet
from .generic_similarity import GenericSimilarity

from typing import List, Union, TextIO

class FunctionalSimilarity(GenericSimilarity):
    def __init__(self, associations:AssociationSet=None):
        GenericSimilarity.__init__(self, associations=associations)

        self.symbol_map = {}
        self.identifier_map = {}

    def load_associations(self, ontology_name:str='go', subject_category:str='gene', object_category:str='function', file:Union[str, TextIO]=None, fmt:str=None):
        GenericSimilarity.load_associations(
            self,
            ontology_name=ontology_name,
            subject_category=subject_category,
            object_category=object_category,
            file=file,
            fmt=fmt
        )

    def load_gene_set(self, gene_set:List[str], taxon:str=None):
        self.gene_set = []

        for gene in gene_set:
            mg = QueryMyGene(curie=gene, taxon=taxon)
            mg.query_mygene()
            gene_dat = mg.package
            ukb = mg.parse_uniprot()

            uniprotkb = 'UniProtKB:{}'.format("".join(ukb))

            self.symbol_map[uniprotkb] = gene_dat['symbol']
            self.identifier_map[uniprotkb] = gene

    def compute_similarity(self):
        uniprotkb_gene_set = self.identifier_map.keys()
        results = self.compute_jaccard(uniprotkb_gene_set)

        for result in results:
            input_curie = result['input_curie']
            result['input_curie'] = self.identifier_map[input_curie]
            result['input_name'] = self.symbol_map[input_curie]

        return results
