# realvoice: E31, the first check on real voice

Does personal calibration still help on top of a strong open speech-emotion model? See
[docs/28](../docs/28-speech-front-end.md).

```bash
pip install -r realvoice/requirements.txt
python -m pytest -q realvoice/tests            # the protocol on synthetic features (no download)
# RAVDESS speech: Zenodo record 1188976, "Audio_Speech_Actors_01-24.zip", unzipped to data/RAVDESS
python realvoice/e31_real_voice.py --data data/RAVDESS --encoder emotion2vec --out realvoice/results
python realvoice/e31_real_voice.py --data data/RAVDESS --encoder mfcc --out realvoice/results
```

On Windows PowerShell the same commands work with `\` in paths. The first emotion2vec run downloads the model
(`iic/emotion2vec_plus_base`, change it with `--model`); features are cached in `realvoice/results/cache`.

Output: `realvoice/results/E31_<encoder>.md` with accuracy and balanced accuracy for zero-shot, generic head,
+ personal baseline and + 2, 4, 8, 16 answers per speaker, leave one speaker out.
