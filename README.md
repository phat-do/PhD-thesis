# Repo for the PhD thesis of Phat Do (Campus Fryslân, University of Groningen)

This is the repository to accompany the PhD thesis of Phat Do titled **Praat mar Frysk (mei amper data): Speech Synthesis for Low-Resource Languages with Cross-Lingual Transfer Learning** at Campus Fryslân, University of Groningen. This repo details the source code and data (to the extent possible) of the experiments described in the thesis. For the open-access, open-data, and open-source implementation of Frisian TTS (from **Chapter 7**), please refer to [https://huggingface.co/spaces/phatdo/Frysk-TTS](https://huggingface.co/spaces/phatdo/Frysk-TTS).

![](./assets/Friesland.png)

# Structure

The repo is structured as follows:
- `FastSpeech2`: the codebase for the FastSpeech 2 model as used in the experiments in **Chapters 3, 5, and 6**.
- `mosfinetune-ssl`: the codebase for the wav2vec2.0-based MOS prediction model as used in the experiments in **Chapters 4**.
- `chapter_2`: the metadata used for the meta-analysis in **Chapter 2**.
- `chapter_3`: the scripts for phone mapping and ASPF calculation as mentioned in **Chapter 3**.
- `chapter_5`: the scripts for preprocessing and converting the phone labels into phonological features as mentioned in **Chapter 5**.

For the experiments in **Chapter 5**, there are two branches---`phone_labels` and `phono_features`---with corresponding changes in `FastSpeech2`.

# Dependencies
The experiments were done using `Python 3.8.6`. Dependencies can be installed using the included `requirements.txt`.

# References

The FastSpeech 2 implementation used in the experiments is modified from [https://github.com/ming024/FastSpeech2](https://github.com/ming024/FastSpeech2)

- Chien, C. M., Lin, J. H., Huang, C. Y., Hsu, P. C., & Lee, H. Y. (2021, June). Investigating on incorporating pretrained and learnable speaker representations for multi-speaker multi-style text-to-speech. In ICASSP 2021-2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 8588-8592). IEEE.

The wav2vec2.0-based MOS prediction model is from [https://github.com/nii-yamagishilab/mos-finetune-ssl](https://github.com/nii-yamagishilab/mos-finetune-ssl)

- Cooper, E., Huang, W. C., Toda, T., & Yamagishi, J. (2022, May). Generalization ability of MOS prediction networks. In ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 8442-8446). IEEE.

