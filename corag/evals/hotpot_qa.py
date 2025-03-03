from datasets import load_dataset

dataset = load_dataset("hotpot_qa", "distractor")
print("loaded dataset successfully")

def preprocess_example(example):
    # Concatenate context paragraphs (you might choose a specific ordering)
    context = " ".join(example["context"])
    # Create a unified example dictionary
    return {"question": example["question"], "context": context, "answers": example["answer"]["text"]}

# Apply preprocessing to the validation split
val_dataset = dataset["validation"].map(preprocess_example)
print(val_dataset[0])

from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

model_name = "deepset/roberta-base-squad2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Create a QA pipeline
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)


def get_prediction(example):
    # Using our QA pipeline
    result = qa_pipeline({
        "question": example["question"],
        "context": example["context"]
    })
    return result["answer"]

# Let's run on the first 5 examples for a quick demo:
for i in range(5):
    example = val_dataset[i]
    predicted_answer = get_prediction(example)
    print(f"Question: {example['question']}")
    print(f"Predicted Answer: {predicted_answer}")
    print(f"Ground Truth: {example['answers']}\n")


import re
import string

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    
    def white_space_fix(text):
        return ' '.join(text.split())
    
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    
    def lower(text):
        return text.lower()
    
    return white_space_fix(remove_articles(remove_punc(lower(s))))

def compute_f1(prediction, ground_truths):
    prediction = normalize_answer(prediction)
    f1_scores = []
    for gt in ground_truths:
        gt = normalize_answer(gt)
        pred_tokens = prediction.split()
        gt_tokens = gt.split()
        common = set(pred_tokens) & set(gt_tokens)
        if len(common) == 0:
            f1_scores.append(0)
            continue
        precision = len(common) / len(pred_tokens)
        recall = len(common) / len(gt_tokens)
        f1 = (2 * precision * recall) / (precision + recall)
        f1_scores.append(f1)
    return max(f1_scores)  # Use the maximum f1 among all ground truth answers

# Compute F1 for a few examples:
for i in range(5):
    example = val_dataset[i]
    predicted_answer = get_prediction(example)
    f1 = compute_f1(predicted_answer, example["answers"])
    print(f"Question: {example['question']}")
    print(f"Predicted Answer: {predicted_answer}")
    print(f"F1 Score: {f1:.4f}\n")
