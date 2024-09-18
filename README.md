# Notes
```
# auth
msal

# Microsoft Graph
msgraph-sdk

# remember
# run once to download the NLTK data
# nltk.download('popular')
# nltk.download('punkt_tab')

```

# Prompts

if you need, given an excel file text.xlsx which you are going to use 2 columns  identified by the headers 'TextHeader1' and 'TextHeader2', use constant variables like TEXT_HEADER1, TEX_HEADERT2 to store the headers values e.g. TEXT_HEADER1 = 'TextHeader1'. This file is created using a Microsoft Form which gather personal information like, address, name, social id card number, phone, email, etc. Another excel file which will be your patterns, this file have some sheets there, you will use the column with header 'PatternHeader' in each sheet as patterns, use a constant variable like PATTERN_HEADER to store the header value, e.g. PATTERN_HEADER = 'PatterHeader'. The idea is find some pattern in the text. It can be the whole phrase but some words too

# Approach:

Tokenization: Break down the address texts into individual words or tokens. This can be done using simple string splitting or more sophisticated tokenization techniques like NLTK.
Normalization: Convert the tokens to a consistent format (e.g., lowercase, remove punctuation). This helps in comparing words regardless of case or formatting.
Similarity Metrics: Choose a suitable similarity metric to measure the similarity between the tokenized and normalized address texts. Some common metrics include:
Jaccard Similarity: Calculates the intersection over union of the sets of tokens.
Cosine Similarity: Measures the cosine of the angle between the vectors representing the tokenized texts.
Levenshtein Distance: Calculates the minimum number of edits (insertions, deletions, substitutions) required to transform one string into another.

- remueve la palabra parroquia.
- 