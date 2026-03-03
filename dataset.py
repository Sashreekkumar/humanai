from datasets import Audio, load_dataset, DatasetDict

'''
LOADING DATA 
'''

metadata_path = "dataset/metadata.csv"

dataset = load_dataset(
    "csv",
    data_files=metadata_path,
    split="train"
)

'''
RESAMPLING and adding audio to the directed path
'''

dataset = dataset.rename_column("path", "audio")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
dataset = dataset.rename_column("path", "audio")
print(dataset[0]["audio"]["array"].shape)
print(dataset[0]["audio"]["sampling_rate"])
print(dataset.shape)
print(dataset[:5])

'''TEST (10%) - TRAIN (80%) - VALIDATE (10%) SPLIT'''
SEED = 42

# First split
train_temp = dataset.train_test_split(
    test_size=0.2,
    seed=SEED
)

# Second Split 
val_test = train_temp["test"].train_test_split(
    test_size=0.5,
    seed=SEED
)

dataset_dict = DatasetDict({
    "train": train_temp["train"],
    "validation": val_test["train"],
    "test": val_test["test"]
})

print(dataset_dict)
