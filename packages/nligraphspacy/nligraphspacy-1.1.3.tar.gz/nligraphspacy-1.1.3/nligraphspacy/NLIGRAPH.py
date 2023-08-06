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
  
  
