from model import analyze_depression
from preprocessing import normalize_text
text = "I hope the pilot pulls through. There's been enough death today at #shoreham 😟" 

result = analyze_depression(text)
result2 = normalize_text(text)

print(result)
print(result2)