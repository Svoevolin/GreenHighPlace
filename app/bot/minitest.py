from datetime import date
import urlextract

extractor = urlextract.URLExtract()

def extractUniqueCode(text):
    return text.split()[1] if len(text.split()) > 1 else None

x = date.today().strftime("%d/%m/%Y")
print(x)