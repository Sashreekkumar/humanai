# Spanish EIT Transcription Pipeline

An automated speech recognition (ASR) pipeline for transcribing Spanish **Elicited Imitation Task (EIT)** recordings. It uses Faster Whisper for transcription, Silero VAD for speech detection, and Levenshtein distance for matching transcribed output to a fixed set of 30 target stimulus sentences — exporting results to formatted Excel sheets.

---

## Overview

This pipeline was built to process audio recordings of participants completing an EIT, where they listen to Spanish sentences and repeat them back. The system:

1. Loads and preprocesses audio (resampling, DC offset removal, optional noise reduction)
2. Detects speech segments using Voice Activity Detection (VAD)
3. Transcribes each segment using a Whisper-based model
4. Merges nearby fragments and builds candidate windows
5. Matches transcriptions to known stimulus sentences using edit distance
6. Exports results to Excel and prints evaluation metrics

---

## Requirements

```bash
pip install python-Levenshtein
pip install pyannote.audio==3.1.1
pip install faster_whisper
pip install noisereduce
pip install openpyxl
```

Also requires:
- `torch` / `torchaudio`
- `pydub`
- `soundfile`
- `numpy`

---

## Pipeline Stages

### 1. Load & Resample
Converts any audio format to mono, 16 kHz WAV using `pydub`. Normalizes samples to `[-1, 1]`.

### 2. DC Offset Removal
Subtracts the signal mean to center the waveform around zero, improving downstream processing.

### 3. Voice Activity Detection (VAD)
Uses the **Silero VAD** model (`snakers4/silero-vad`) to detect speech regions. Key parameters:

| Parameter | Default | Description |
|---|---|---|
| `vad_thr` | `0.35` | Detection sensitivity threshold |
| `min_speech_duration_ms` | `400` | Minimum speech segment length |
| `min_silence_duration_ms` | `500` | Minimum silence to split segments |

### 4. Segment Padding & Merging
- **Padding** (`pad_ms=200`): Expands each VAD boundary slightly to avoid clipping word edges.
- **Merging** (`max_gap=0.5s`): Joins nearby VAD segments to reconstruct complete utterances.

### 5. Optional Noise Reduction
Spectral noise reduction via `noisereduce`. Disabled by default (`use_denoise=False`) — testing showed no significant improvement in evaluation metrics.

### 6. Transcription
Uses **Faster Whisper** (`medium` model, `float16`, CUDA) to transcribe each speech segment independently. Segments shorter than 0.5s are skipped. Language is forced to Spanish (`"es"`).

### 7. Fragment Merging
Consecutive transcriptions with a gap of ≤ 2 seconds are merged into a single entry. A `<pause>` token is inserted at each merge point to flag disfluency.

### 8. Candidate Window Matching
For each stimulus sentence, sliding windows of 1–3 consecutive ASR segments are generated as candidates. Each candidate is scored against the stimulus using **Levenshtein distance** after normalization (lowercasing, punctuation removal, `<pause>` stripping). The best non-overlapping match is selected. Sentences with no match within the `max_dist=20` threshold are marked `[not produced]`.

### 9. Export
Results are saved to a formatted `.xlsx` file with columns: **Sentence**, **Stimulus**, **Transcription**.

### 10. Evaluation
Reports per-file metrics: total sentences, matched count, not-produced count, exact matches, and average edit distance.

---

## Usage

```python
STIMULI = [
    (1, "Quiero cortarme el pelo"),
    (2, "El libro está en la mesa"),
    # ... 30 sentences total
]

result = run_eit_pipeline(
    audio_path="path/to/audio.mp3",
    stimuli=STIMULI,
    output_path="output.xlsx",
    target_sr=16000,
    vad_thr=0.35,
    pad_ms=200,
    max_gap=0.5,
    use_denoise=False
)
```

To run multiple files and summarize:

```python
all_metrics = []
for i, audio_path in enumerate(AUDIO_FILES):
    result = run_eit_pipeline(audio_path, STIMULI, f"output_{i+1}.xlsx")
    all_metrics.append(result["metrics"])

summarize_all_runs(all_metrics)
```

---

## Results

### Without Noise Reduction

| File   | Matched | Not Produced | Exact | Avg Distance |
|--------|---------|--------------|-------|--------------|
| File 1 | 24      | 6            | 5     | 6.12         |
| File 2 | 23      | 7            | 3     | 10.22        |
| File 3 | 14      | 16           | 0     | 11.43        |
| File 4 | 30      | 0            | 7     | 7.73         |
| **AVG**| **22.75**| **7.25**   | **3.75** | **8.88** |

### With Noise Reduction

| File   | Matched | Not Produced | Exact | Avg Distance |
|--------|---------|--------------|-------|--------------|
| File 1 | 24      | 6            | 5     | 6.12         |
| File 2 | 23      | 7            | 3     | 10.22        |
| File 3 | 14      | 16           | 0     | 11.64        |
| File 4 | 29      | 1            | 7     | 7.21         |
| **AVG**| **22.50**| **7.50**   | **3.75** | **8.80** |

> Noise reduction did not meaningfully change outcomes across the test files. File 3 performed poorly across both conditions, likely due to a much longer recording with significant non-target speech content before the EIT stimuli begin.

---

## Notes

- **File 3** had 99 VAD segments vs ~40 for the other files, suggesting it contains a longer preamble or unrelated speech content that disrupts matching.
- The `<pause>` token in transcriptions indicates the speaker paused mid-sentence — a potential disfluency marker useful for linguistic analysis.
- The pipeline assumes the 30 EIT stimuli are produced in order; the greedy matching algorithm respects temporal ordering by excluding already-used time spans.
- Whisper is run in **Spanish-forced mode** (`language="es"`), though some participants occasionally produced English (e.g., "Sometimes they take their dog..."), which Whisper transcribed in English anyway.

---

## Project Structure

```
.
├── spanish_transcription.ipynb   # Main Colab notebook
├── README.md
└── outputs/
    ├── output_1.xlsx             # Results for file 038010
    ├── output_2.xlsx             # Results for file 038011
    ├── output_3.xlsx             # Results for file 038012
    └── output_4.xlsx             # Results for file 038015
```