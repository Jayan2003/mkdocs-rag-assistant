from rag_answer import rag_answer

q = input("Ask something about MkDocs: ")

answer = rag_answer(q)

print("\n======== ANSWER =========\n")
print(answer)
print("\n=========================\n")
