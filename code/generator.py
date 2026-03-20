import re
from config import GENERATOR_MODEL_NAME
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def load_generator_model():
    """
    Load the tokenizer and generator model.
    If model loading fails, return (None, None) and use extractive fallback.
    """
    try:
        print("Loading generator tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            GENERATOR_MODEL_NAME,
            use_fast=False
        )
        print("Tokenizer loaded.\n")

        print("Loading generator model...")
        model = AutoModelForSeq2SeqLM.from_pretrained(GENERATOR_MODEL_NAME)
        print(f"Generator model loaded: {GENERATOR_MODEL_NAME}\n")

        return tokenizer, model

    except Exception as e:
        print("Generator model could not be loaded.")
        print(f"Reason: {e}\n")
        print("Using extractive fallback instead.\n")
        return None, None


def split_into_sentences(text):
    """
    Split Sanskrit text into sentence-like units.
    """
    parts = re.split(r"[।?!\n]+", text)
    sentences = [part.strip() for part in parts if part.strip()]
    return sentences


def normalize_words(text):
    """
    Very simple word extraction for overlap matching.
    """
    words = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return set(words)


def extractive_answer(context, question):
    """
    Return the sentence from context that best matches the question.
    """
    sentences = split_into_sentences(context)

    if not sentences:
        return "Answer not found in the provided context."

    question_words = normalize_words(question)

    best_sentence = ""
    best_score = -1

    for sentence in sentences:
        sentence_words = normalize_words(sentence)
        score = len(question_words.intersection(sentence_words))

        if score > best_score:
            best_score = score
            best_sentence = sentence

    if best_score <= 0:
        return "Answer not found in the provided context."

    return best_sentence


def generate_answer(tokenizer, model, context, question):
    """
    Try generator model first.
    If output is empty or bad, use extractive fallback.
    """
    if tokenizer is not None and model is not None:
        try:
            prompt = f"question: {question} context: {context}"

            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512
            )

            outputs = model.generate(
                **inputs,
                max_new_tokens=40,
                do_sample=False
            )

            answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

            # Reject weak/broken outputs
            if answer and "<extra_id_" not in answer:
                return answer

        except Exception as e:
            print(f"Generator failed, switching to extractive fallback: {e}")

    return extractive_answer(context, question)


if __name__ == "__main__":
    tokenizer, model = load_generator_model()

    test_context = """
"अरे शंखनाद, गच्छापणम्, शर्कराम् आनय ।"
इति स्वभृत्यम् शंखनादम् गोवर्धनदासः आदिशति ।
ततः शंखनादः आपणम् गच्छति ।
शर्कराम् जीर्णे वस्त्रे न्यस्यति च ।
तस्मात् जीर्णवस्त्रात् मार्गे एव सर्वापि शर्करा स्त्रवति ।
ततः गोवर्धनदासः कोपेन शंखनादम् वदति, "अरे मूढ, कुत्रास्ति शर्करा ?"
"""

    test_question = "शर्करा कुत्र अस्ति ?"

    print("Generating answer...\n")
    answer = generate_answer(tokenizer, model, test_context, test_question)

    print(f"Question: {test_question}\n")
    print(f"Generated answer: {answer!r}")