from transformers import T5ForConditionalGeneration, T5Tokenizer
# Load the tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-base')

# Load the pre-trained T5 model
model = T5ForConditionalGeneration.from_pretrained('/Users/samhoanghong/data_science/natural language processing/summary_model')
def word_sum_t5(text):
    

    inputs = tokenizer.encode(text, return_tensors="pt")
    #outputs = model.generate(inputs, max_length=160, num_beams=4, early_stopping=True, min_length=80, length_penalty=80)
    outputs = model.generate(inputs, num_beams=4, early_stopping=True, max_length=40)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

