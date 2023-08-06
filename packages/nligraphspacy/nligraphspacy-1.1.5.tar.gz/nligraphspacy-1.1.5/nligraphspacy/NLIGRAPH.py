import spacy
import en_nligraphspacy

class RelationEntityExtract:
  def __init__(self, text):
    
    self.text = text
    
  def load_model(self):
    
    nlp = spacy.load("en_nligraphspacy")
    return nlp
  
  def process_text(self):
    
    model = self.load_model()
    doc = model(self.text)
    return doc.ents

  def get_seperate_entities(self):

    list_entities = []
    model = self.load_model()
    doc = model(self.text)

    for tok in doc:
      if tok.ent_type != '':
        json_dict = {}
        json_dict['text'] = tok.text
        json_dict['label'] = tok.ent_type_

        list_entities.append(json_dict)

    return list_entities
  
  
