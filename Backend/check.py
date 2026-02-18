import database

database.initialize_data()

print("Metadata loaded:", database.metadata is not None)
print("Embeddings loaded:", database.id_list is not None)

test_id = 5664

print(f"{test_id} in metadata:", test_id in database.metadata.index)
print(f"{test_id} in embeddings:", test_id in database.id_list)

print("Metadata size:", len(database.metadata))
print("Embedding size:", len(database.id_list))
