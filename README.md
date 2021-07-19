# ZoomChatter

ZoomChatter - extract information from Zoom chat transcripts

Copyright 2021 Peter Kaminski. Licensed under MIT License.

## Usage

### Installation

Download repository.

Install requirements:

```
pip install -r requirements.txt
```

### Development / Debugging

```
python api.py
```

Send POST requests to URL that Flask provides.

## Usage

Send POST requests to `(base url)/zoomchatter`.

Include one or more Zoom chat transcripts as "form-data" files. Any key can provided for each file; good values might be empty string ('') or 'chat'.

## Notes and Considerations

Zoom chat transcripts can include Unicode characters.  Commonly seen characters include "smart" punctuation characters and formatting characters including (but not limited to):

- U+2018, Left single quotation mark
- U+2019, Right single quotation mark
- U+201C, Left double quotation mark
- U+201D, Right double quotation mark
- U+2028, Line separator
