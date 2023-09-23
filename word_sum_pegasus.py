from transformers import PegasusForConditionalGeneration, PegasusTokenizer
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

def pegasus_sum(text):

    # Create tokens - number representation of our text
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    summary = model.generate(**tokens)
    summary[0]
    # Decode summary
    return(tokenizer.decode(summary[0]))