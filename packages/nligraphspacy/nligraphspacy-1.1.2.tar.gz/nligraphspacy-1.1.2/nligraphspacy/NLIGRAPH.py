import spacy

class RelationEntityExtract:
  def __init__(self, text):
    
    self.text = text
    
  def load_model(self):
    
    nlp = spacy.load("/home/project/kgmodel/")
    return nlp
  
  def process_text(self):
    
    model = self.load_model()
    doc = model(self.text)
    return doc.ents
  
  
