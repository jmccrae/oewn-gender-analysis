import wn

#for wn_name in ["omw-en31"]:
for wn_name in ["oewn:2024-10-03"]:
#for wn_name in ["omw-en", "omw-en31", "oewn:2023", "oewn:2024-10-03"]:
    print(f"Loading {wn_name}")
    oewn = wn.Wordnet(wn_name)

    female = [synset for synset in oewn.synsets("female") if "person" in synset.definition()][0]
    male = [synset for synset in oewn.synsets("male") if "person" in synset.definition()][0]
    ungendered = [synset for synset in oewn.synsets("doer") if "person" in synset.definition()][0]

    def all_children(synset):
        children = synset.relations().get("hyponym", [])
        for child in children:
            children.extend(all_children(child))
        return set(children)
    
    def n_entries(synsets):
        return len([l for ss in synsets for l in ss.lemmas()])

    #male_synsets = all_children(male)
    #female_synsets = all_children(female)
    #ungendered_synsets = all_children(ungendered) - male_synsets - female_synsets
    male_synsets = set(ms for ms in all_children(male) 
                       if ms.id.startswith("oewn-0") or 
                       ms.id.startswith("oewn-1"))
    female_synsets = set(fs for fs in all_children(female)
                         if fs.id.startswith("oewn-0") or 
                         fs.id.startswith("oewn-1"))
    ungendered_synsets = set(us for us in all_children(ungendered)
                             if (us.id.startswith("oewn-0") or 
                             us.id.startswith("oewn-1")) and
                             us not in male_synsets and
                             us not in female_synsets)

    print(f"Number of Male Synsets: {len(male_synsets)}")
    print(f"Number of Male Entries: {n_entries(male_synsets)}")
    print(f"Number of Female Synsets: {len(female_synsets)}")
    print(f"Number of Female Entries: {n_entries(female_synsets)}")
    print(f"Number of Ungendered Synsets: {len(ungendered_synsets)}")
    print(f"Number of Ungendered Entries: {n_entries(ungendered_synsets)}")

    for both in set(male_synsets).intersection(female_synsets):
        print(both)

    male_chars = 0
    male_words = 0

    for ms in male_synsets:
        male_chars += len(ms.definition())
        male_words += len(ms.definition().split())

    female_chars = 0
    female_words = 0

    for fs in female_synsets:
        female_chars += len(fs.definition())
        female_words += len(fs.definition().split())

    ungendered_chars = 0
    ungendered_words = 0

    for us in ungendered_synsets:
        ungendered_chars += len(us.definition())
        ungendered_words += len(us.definition().split())

    print(f"Average Definition Length for Male Synsets: {male_chars/len(male_synsets)} characters, {male_words/len(male_synsets)} words")
    print(f"Average Definition Length for Female Synsets: {female_chars/len(female_synsets)} characters, {female_words/len(female_synsets)} words")
    print(f"Average Definition Length for Ungendered Synsets: {ungendered_chars/len(ungendered_synsets)} characters, {ungendered_words/len(ungendered_synsets)} words")

