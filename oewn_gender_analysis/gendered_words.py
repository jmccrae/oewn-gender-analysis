import wn
import wn.taxonomy
import csv

oewn = wn.Wordnet('oewn:2024-25-09')

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

male_lemmas.append("man")
female_lemmas.append("woman")
female_lemmas.append("ess")
male_lemmas.remove("master")
male_lemmas.remove("ex")
female_lemmas.remove("ex")
male_lemmas.remove("cat")
female_lemmas.remove("cat")

print(male_lemmas)
print(female_lemmas)

for overlap in set(male_lemmas).intersection(set(female_lemmas)):
    for word in oewn.words(overlap):
        print()
        print(word)
        male_overlaps = []
        female_overlaps = []
        for synset in word.synsets():
            for path in wn.taxonomy.hypernym_paths(synset):
                if man_synset in path:
                    male_overlaps.append((synset.lemmas(), path))
                if woman_synset in path:
                    female_overlaps.append((synset.lemmas(), path))
        print(male_overlaps)
        print(female_overlaps)

def is_hyp(hypo, hyper):
    return hypo == hyper or any(is_hyp(h, hyper) for h in hypo.hypernyms())

with open("gendered_words.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Synset ID", "Lemma", "Gendered Word", "Gender", 
                     "Is Gendered Word?"])
    doer = oewn.synset('oewn-09786620-n')
    for synset in all_hyponyms(doer):
        for word in synset.words():
            for male_lemma in male_lemmas:
                if (word.lemma().endswith(male_lemma) and
                    not is_hyp(synset, man_synset) and
                    not word.lemma().endswith("woman")):
                    writer.writerow([synset.id,
                                     word.lemma(),
                                     male_lemma,
                                     "M",
                                     ""])
            for female_lemma in female_lemmas:
                if (word.lemma().endswith(female_lemma) and
                    not is_hyp(synset, woman_synset)):
                    writer.writerow([synset.id,
                                     word.lemma(),
                                     female_lemma,
                                     "F",
                                     ""])

