import wn
import wn.taxonomy

oewn = wn.Wordnet('oewn:2024')

man_synset = oewn.synset('oewn-10306910-n')
woman_synset = oewn.synset('oewn-10807146-n')

def all_hyponyms(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms.add(hyponym)
        hyponyms.update(all_hyponyms(hyponym))
    return hyponyms

male_lemmas = [lemma for synset in all_hyponyms(man_synset) 
               for lemma in synset.lemmas()
               if not lemma[0] == lemma[0].upper()] # Ignore proper nouns
female_lemmas = [lemma for synset in all_hyponyms(woman_synset) 
                 for lemma in synset.lemmas()
                 if not lemma[0] == lemma[0].upper()]

print(male_lemmas)
print(female_lemmas)

for overlap in set(male_lemmas).intersection(set(female_lemmas)):
    for word in oewn.words(overlap):
        print(word)
        for synset in word.synsets():
            for path in wn.taxonomy.hypernym_paths(synset):
                for i, ss in enumerate(path):
                    print(' ' * i, ss, ss.lemmas()[0])

def is_hyp(hypo, hyper):
    return hypo == hyper or any(is_hyp(h, hyper) for h in hypo.hypernyms())

#for word in oewn.words(pos='n'):
#    if any(word.lemma().endswith(male_lemma) for male_lemma in male_lemmas):
#        for synset in word.synsets():
#            if not is_hyp(synset, man_synset):
#                print(word, synset.definition())

