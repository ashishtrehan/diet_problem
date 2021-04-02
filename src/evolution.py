import random
import numpy as np

def decoder():
    return

def _generate_parent(size,geneSet,get_fitness):
    genes = []
    while len(genes)<size:
        parent = random.sample(geneSet,size)
        genes.extend(parent)
    fitness = get_fitness(genes)
    return Chromosome(genes,fitness)

def _generate_population(size,geneSet,get_fitness,population_size):
    p = [_generate_parent(size,geneSet,get_fitness) for x in range(population_size)]
    return p
    
def _generate_selection(population,k=6):
    selection_ix = np.random.randint(len(population))
    for ix in np.random.randint(0,len(population),k-1):
        if population[ix].fitness < population[selection_ix].fitness:
            selection_ix = ix
        return population[selection_ix]


def _mutate(parent,geneSet,get_fitness,rate):
    childGenes = parent.genes 
    size = len(parent.genes)
    zero_prob = 1 - rate
    p = np.random.choice(2,size,p=[zero_prob,rate])
    for x in np.where(p==1)[0]:
        newgene = random.sample(geneSet,1)[0]
        parent.genes[x]=newgene
    fitness = get_fitness(parent.genes)
    return Chromosome(parent.genes,fitness)

def _generate_crossover(p1,p2,r_cross,get_fitness):
    #Uniform Crossover (coin flip to decide who gets what from each parent)
    c1,c2 = [],[]
    genes = list(zip(p1.genes,p2.genes))
    for i,x in enumerate(genes):
        a = np.random.choice(2,1,p=[r_cross,1-r_cross])[0]
        b = np.random.choice(2,1,p=[r_cross,1-r_cross])[0]
        c1.append(genes[i][a])
        f1 = get_fitness(c1)
        c2.append(genes[i][b])
        f2 = get_fitness(c2)
    return Chromosome(c1,f1),Chromosome(c2,f2)



class Chromosome:
    def __init__(self,genes,fitness):
        self.genes = genes
        self.fitness = float(fitness)
