import spacy
from spacy.matcher import Matcher

all_entities = []
def add_event_ent(matcher, doc, i, matches):
    label = doc.vocab.strings[matches[i][0]]
    print('Label====>', label)
    print('Doc  ====>', doc)
    _, start, end = matches[i]
    entity_type = None
    entity_type = doc.vocab.strings[label]

    entity = (entity_type, start, end)
    doc.ents += (entity,)
    all_entities.append({ 'tag' : label, 'value' : doc[start:end].text})


def initialize_spacy():
    nlp = spacy.load('en')

    ner = nlp.get_pipe('ner')
    ner.add_label('LICENSE')
    ner.add_label('EXPIRY')
    ner.add_label('ISSUED')

    matcher = Matcher(nlp.vocab)

    matcher.add('LICENSE', add_event_ent,
                [{'LOWER': 'license'}, {'LOWER': 'number'}, {'ORTH': ':'}, {'IS_DIGIT': True}],
                [{'LOWER': 'license'}, {'LOWER': 'number'}, {'ORTH': ':'}, {}],
                [{'LOWER': 'credential'}, {'LOWER': 'number'}, {'ORTH': ':'}, {'ENT_TYPE': 'CARDINAL'}],
                [{'LOWER': 'identification'}, {'LOWER': 'number'}, {'ORTH': ':'}, {'ENT_TYPE': 'CARDINAL'}],
                [{'LOWER': 'identification'}, {'LOWER': 'number'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'license'}, {'LOWER': 'no'}, {'ORTH': '.'}, {'IS_DIGIT': True}],
                [{'LOWER': 'license'}, {'LOWER': 'no'}, {'ORTH': '.'}, {'IS_DIGIT': True}, {'ORTH': '.'}, {'IS_DIGIT': True}],
                )

    matcher.add('ISSUED', add_event_ent,
                [{'LOWER': 'date'}, {'LOWER': 'issued'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'issued'}, {'ORTH': 'on'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'issuance'}, {'lower': 'date'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'issuance'}, {'lower': 'date'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'effective'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                )

    matcher.add('EXPIRY', add_event_ent,
                [{'LOWER': 'date'}, {'LOWER': 'issued'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'expires'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'expiration'}, {'LOWER': 'date'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'expiration'}, {'LOWER': 'date'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}, {'ENT_TYPE': 'DATE'}, {'ORTH': ','}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'expiration'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
                [{'LOWER': 'expire'}, {'LOWER': 'on'}, {'ORTH': ':'}, {'ENT_TYPE': 'DATE'}],
            )

    return nlp, matcher


def split_entity(text):
    print('---------------TEXT-----------------')
    print(text)
    nlp = None
    matcher = None
    doc = None
    nlp, matcher = initialize_spacy()
    doc = nlp(u"{}".format(text))
    matcher(doc)
    print('---------------SPACY----------------')
    print(all_entities)
    if not all_entities:
        return []
    labels = ['LICENSE', 'ISSUED', 'EXPIRY']
    expected = []
    for label in labels:
	    expected.append( [d['value'] for d in all_entities if d['tag'] == label][-1])

    print(expected)
    return expected
    return [f['value'] for f in expected]

