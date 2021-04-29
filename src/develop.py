from classes import Values
from evolution import _generate_parent,_generate_population,_generate_selection,_mutate,_generate_crossover,Chromosome
import random
import pandas as pd
import numpy as np

df = pd.read_csv('data/nutrients.csv')
food_dictionary = df.set_index('id').T.to_dict()
ids = list(set(df['id']))


def null(x):
    return np.where(np.isnan(x),0.0,x)


def nutrition(meals):
    p,s,c,f,sd = [],[],[],[],[]
    for x in meals:
        b = Values(food_dictionary.get(x))
        sugars = null(b.sugars)
        protein = null(b.protein)
        cal = null(b.calories)
        fat = null(b.fat)
        sodium = null(b.sodium)
        # print (b.group)
        p.append(protein)
        s.append(sugars)
        c.append(cal)
        f.append(fat)
        sd.append(sodium)
    return np.array((p,c,s,f,sd)).T
        

def get_fitness(x):
    m = nutrition(x)
    # return (np.sum(p)*4.0-np.sum(s))/np.sum(c)
    sigma = np.sum(m,axis=0)
    # sugar_constraint = np.where(sigma[2]>0,1,0)
    # print (sugar_constraint)
    fat = sigma[3]/sigma[1]
    sodium = 1 if sigma[4] <= 2300 else 0
    # pro = (sigma[0]*4.0)/sigma[1]
    pro = f(sigma[0]*4.0,sigma[1])
    a = 1 if pro >= .3 else 0
    return a - fat - sodium
    # return fat*9/sigma[1]

def f(x, y):
    "fixing division by null"
    return (0 if x==0 and y==0 else float(x**2*y)/(x**4 + y**4))


def genetic_algorithm(generations,population_size):
    #initial population
    pop = _generate_population(10,ids,get_fitness,1000)
    best_eval = pop[0].fitness
    metrics = []
    for x in range(generations):
        children=[] 
        for i in range(0,population_size,2):
            p1,p2 = _generate_selection(pop),_generate_selection(pop)
            c1,c2 = _generate_crossover(p1,p2,.5,get_fitness)
            c1 = _mutate(c1,ids,get_fitness,.15)
            c2 = _mutate(c2,ids,get_fitness,.20)
            children.append(c1)
            children.append(c2)
        for z in children:
            if best_eval < (z.fitness):
                print (z.fitness)
                best_eval = z.fitness
                a = [Values(food_dictionary.get(x)) for x in z.genes]
                print ([i.name for i in a])
                c = Chromosome(z.genes,z.fitness)
        pop = children
        max_fitness = max([x.fitness for x in children])
        metrics.append([{'generation':x,'max_fitness':max_fitness}])
    # print (metrics)
    return c,children


c,children = (genetic_algorithm(100,1000))