import re

def normalize_text(text):
    text = text.lower()                   
    text = re.sub(r"http\S+", "", text)   # remove URLs
    text = re.sub(r"@\w+", "", text)      # remove mentions
    text = re.sub(r"[^\w\s']", "", text)  # remove punctuation
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)  # normalize repetition
    text = text.encode("ascii", "ignore").decode()





    return text




def tokenize(text):
    return re.findall(r'\b\w+\b', text)