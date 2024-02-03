
import os
from bs4 import BeautifulSoup
import spacy
import neuralcoref

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("div", {"class": "chapter-content"}).text


def get_entity_per_sentence(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentence_and_entity = []
    for sent in doc.sents:
        sentence_and_entity.append([sent, [ent for ent in sent.ents]])

    return sentence_and_entity


def print_types(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    sentence_and_entity = []
    for sent in doc.sents:
        # line = [sent]
        line = []
        for token in sent:
            if token.ent_type_:
                line.append([token.text, token.ent_type_, token.ent_iob_])
        sentence_and_entity.append(line)
    print(len(sentence_and_entity))

    # cleaning the list
    clean_entities = []
    for line in sentence_and_entity:
        line = list(filter(lambda ent: not ent.__contains__("\n"), line))
        clean_entities.append(line)

    # joining multi token entity names together
    joined_entities = []
    for line in clean_entities:
        tmp_line = []
        idx = 0
        for ent in line:
            if idx == 0:
                tmp_line.append([[ent[0]], ent[1]])
                idx += 1
            elif ent[2] == 'I' and tmp_line[idx - 1][1] == ent[1]:
                tmp_line[idx - 1][0].append(ent[0])
            else:
                tmp_line.append([[ent[0]], ent[1]])
                idx += 1

        joined_entities.append(tmp_line)
    for line in joined_entities:
        print(line)
    # for line in sentence_and_entity:
    #     print(line)




if __name__ == "__main__":
    program_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(program_path, "data", "chapter_2.html")
    file = open(file_path, 'r')
    html = file.read()
    text = parse_html(html)
    sent_ent = get_entity_per_sentence(text)
    # for line in sent_ent:
        # print(line[1])
    print_types(text)


# todo test out doc.vocab
