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

Include one or more Zoom chat transcripts as "form-data" files. Any key can provided for each file; good keys might be empty string `` or `chat`, but any string is accepted.

Multiple files are concatenated and treated as one.

## Design Notes and Considerations

### URLs

### Transcript Filenames

### Direct and Private Messages

### Line-ending Characters

Transcripts may come in with different line-ending characters depending on the user's operating system and how they POST the file.  Assume that there may be (at least):

```
\r\n
\n
\r
\n\r
```

### Multi-line Comments

Meeting participants can paste text with included line breaks.  Zoom appears to convert the first linebreak to two "Line Separator" characters (U+2028).  Subsequent linebreaks are left as-is.

When returning comments, consider that there may be different ways to represent one multi-line post:

- newlines are converted to one space character
- newlines are left as newlines
- newlines are converted to the literal string `\n`
- newlines are converted to the literal string `<br />`

### Unicode Characters

Zoom chat transcripts can include Unicode characters.  Commonly seen characters include "smart" punctuation characters and formatting characters including (but not limited to):

- U+2018, Left single quotation mark
- U+2019, Right single quotation mark
- U+201C, Left double quotation mark
- U+201D, Right double quotation mark
- U+2028, Line separator
