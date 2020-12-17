
def calculate_ner_stats(doc):
    stats = {
        'ner': {
            'persons': [],
            'gpes': [],
            'orgs': [],
            'locs': [],
            'works_of_arts': [],
            'laws': [],
            'events': [],
            'products': [],
            'norps': [],
            'facs': [],
            'languages': []
        }
    }

    for token in doc:
        if "punct" in token.dep_:
            continue

    for ent in doc.ents:
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
        if ent.label_ == 'PERSON' and ent.text not in stats['ner']['persons']:
            stats['ner']['persons'].append(ent.text)
        if ent.label_ == 'GPE' and ent.text not in stats['ner']['gpes']:
            stats['ner']['gpes'].append(ent.text)
        if ent.label_ == 'ORG' and ent.text not in stats['ner']['orgs']:
            stats['ner']['gpes'].append(ent.text)
        if ent.label_ == 'LOC' and ent.text not in stats['ner']['locs']:
            stats['ner']['locs'].append(ent.text)
        if ent.label_ == 'WORK_OF_ART' and ent.text not in stats['ner']['works_of_arts']:
            stats['ner']['works_of_arts'].append(ent.text)
        if ent.label_ == 'LAWS' and ent.text not in stats['ner']['laws']:
            stats['ner']['laws'].append(ent.text)
        if ent.label_ == 'EVENT' and ent.text not in stats['ner']['events']:
            stats['ner']['events'].append(ent.text)
        if ent.label_ == 'PRODUCT' and ent.text not in stats['ner']['products']:
            stats['ner']['products'].append(ent.text)
        if ent.label_ == 'NORP' and ent.text not in stats['ner']['norps']:
            stats['ner']['norps'].append(ent.text)
        if ent.label_ == 'FAC' and ent.text not in stats['ner']['facs']:
            stats['ner']['facs'].append(ent.text)
        if ent.label_ == 'LANGUAGE' and ent.text not in stats['ner']['languages']:
            stats['ner']['languages'].append(ent.text)

    return stats
