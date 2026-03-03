# HumanAI

This repository contains google colab notebooks, notes, project timeline, proposal and all relevant information of my GSOC journey while contributing to HumanAI. 

## Dataset
A subset of [Open Speech and Language Resources Dataset](https://openslr.org/39/) is used for finetuning the model. 

The non-native audio subset of the dataset containing 2028 samples is used for fine-tuning the model.


### Details of dataset:

1. A subcorpus collected at Mexico's Military Academy called Heroico.

2. A subcorpus collected at the United States Military Academy (USMA) in West Point New York.

The Heroico corpus is further divided into recited and prompted speech subcorpora. The recited speech appears under the recordings directory and the prompted speech under the answers directory.

The USMA subcorpus includes 1.2 hours of speech from nonnative informants and 1 hour of speech from native speakers. All the speech in the USMA corpus was recited.

The Heroico subcorpus has 11.8 hours of speech. One hour segment of speech in the Heroico corpus was recited from the same set of prompts that was used in the USMA collection. 


### `generate_metadata`:
A [generate_metadata.py](generate_metadata.py) script creates a CSV file mapping the path, audio file name and transcription. This [metadata.csv](metadata.csv) file is used for loading the dataset. 

### `dataset.py`:
The [dataset.py](dataset.py) script 

## Notes
- [Notes I made while learning the pre-requisites for the required project](notes/Audio.pdf)

