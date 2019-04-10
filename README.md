# Part-fo-speech-tagging-Viterbi-Algorithm


Dataset Requirements:
The corpus has been adapted from the Italian (ISDT) and Japanese (GSD) sections of the universal dependencies corpus. The source corpora, documentation, and credits can be found at http://universaldependencies.org

Adaptations include:

- The corpus contains only tokens and original parts of speech.
- The format has been changed to the word/TAG format, with each sentence on a separate line. The 'raw' files contain the words only.

Adaptations were made by Ron Artstein, artstein@ict.usc.edu

The coding assignment corpus is licensed under the same terms as the original: 

The Italian portion is released under Creative Commons
Attribution-NonCommercial-ShareAlike 3.0 Unported: https://creativecommons.org/licenses/by-nc-sa/3.0/

The Japanese portion is released under Creative Commons
Attribution-NonCommercial-ShareAlike 3.0 United States: https://creativecommons.org/licenses/by-nc-sa/3.0/us/




# Description

Hidden Markov Model part-of-speech tagger for Italian, Japanese, and a surprise language. The training data are provided tokenized and tagged; the test data will be provided tokenized, and tagger will add the tags.


Two programs: hmmlearn.py will learn a hidden Markov model from the training data
hmmdecode.py will use the model to tag new data. The learning program will be invoked in the following way:

> python hmmlearn3.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.
The tagging program will be invoked in the following way:

> python hmmdecode3.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.
