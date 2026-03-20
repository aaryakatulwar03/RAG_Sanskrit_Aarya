from query_system import load_vectorstore, search_query
from generator import load_generator_model, generate_answer
from config import TOP_K


def build_context_from_results(results):
    """
    Combine retrieved chunks into one context string.
    """
    context_parts = []

    for doc in results:
        context_parts.append(doc.page_content)

    return "\n\n".join(context_parts)


if __name__ == "__main__":
    print("Loading retriever...\n")
    vectorstore = load_vectorstore()

    print("Loading generator...\n")
    tokenizer, model = load_generator_model()

    query = input("Enter your question: ").strip()
    print(f"\nYour question: {query}\n")

    results = search_query(vectorstore, query, top_k=TOP_K)

    print(f"Top {TOP_K} retrieved chunks:\n")
    for i, doc in enumerate(results, start=1):
        print(f"Result {i}")
        print(f"Source file: {doc.metadata.get('source_file')}")
        print(f"Chunk ID: {doc.metadata.get('chunk_id')}")
        print(doc.page_content[:250])
        print("\n" + "-" * 50 + "\n")

    context = build_context_from_results(results)

    print("Generating final answer...\n")
    answer = generate_answer(tokenizer, model, context, query)

    print(f"Final Answer:\n{answer}")