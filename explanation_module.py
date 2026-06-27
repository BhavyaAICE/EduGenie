from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# AutoTokenizer for tokenization process. AutoModelForSeq2SeqLM for loading the main architectural model of lamini

tokenizer = None
model = None
# initialize the global variable with none

def get_explanation(topic: str) -> str:

    global tokenizer, model
    # For using the global variables (not creating new ones)
    
    if model is None:
        # for the startup only, when the application loads for the first time, model = none , so it will download the 1gb of data required by Lamini

        print("Lamini model is loading...")
        tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-248M")
        model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-248M")

    prompt = f"Explain the following topic in very simple terms for a student: {topic}"
    # Prompt creation

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    # print(inputs)
    # Converts the prompt into tokens

    outputs = model.generate(**inputs, max_length=256, do_sample=True, temperature=0.7)
    # print(outputs)
    # generate the output

    text_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # number to text generation
    
    return text_output.strip()
