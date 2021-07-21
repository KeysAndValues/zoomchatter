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

Include one or more Zoom chat transcripts as "form-data" files. Any key can provided for each file; good keys might be empty string ('') or `chat`, but any string is currently accepted.

Multiple files are concatenated and treated as one.

### Arguments

_Current version of ZoomChatter doesn't recognize any arguments; these represent future plans._

_Depending on implementation, ZoomChatter may accept arguments either as querystring parameters, or as POST form variables or both, to be determined._

- ?output= (see output types below)
- ?flags=include_private
- ?format=html (text (utf-8), ascii, markdown, HTML, JSON)

### Outputs

In a future version, you will be able to select which outputs you want.  The current version outputs all implemented output types.

- links - all links, de-duplicated
- participants - all participant names, de-duplicated
- lines - all lines from the chat
- input_linebreaks_fixed - the chat, with linebreak and line separator characters all normalized to `\n`

### "Clean" transcript formats

These formats are meant to be easily readable versions of the transcript text, with the timestamps and any noise around the Zoom handles (such as "to Everyone") removed.

These formats are not yet implemented.

- clean
- clean_grouped
- clean_no_names

#### clean

```
Terry Smith:

Hello Sun, how's it going today?

Terry Smith:

By the way, today is Marla's birthday.

Sun Lee:

Not bad, Terry, how about you?

Sun Lee:

Oh! Wish her a happy birthday for me!
```

#### clean_grouped

_Adjacent messages from the same person are coalesced._

```
Terry Smith:

Hello Sun, how's it going today?

By the way, today is Marla's birthday.

Sun Lee:

Not bad, Terry, how about you?

Oh! Wish her a happy birthday for me!
```



- clean_no_names

_Only the text, no Zoom handles. Names typed by participants are not stripped._

```
Hello Sun, how's it going today?

By the way, today is Marla's birthday.

Not bad, Terry, how about you?

Oh! Wish her a happy birthday for me!
```



## Design Notes and Considerations

### URLs (Links)

There are two primary ways to find URLs in text:

1. Regular expression, based on the syntax in RFC 3986.
2. Searching for valid top-level domains.

The current version of ZoomChatter uses a TLD-aware library, [URLExtract](https://github.com/lipoja/URLExtract).

There are various considerations in choosing either approach, and design decisions about which URLs to include and which to exclude, including:

- include URLs without a URL scheme (i.e., http: or https: or ftp:, etc.) or not?
- prepend an assumed URL scheme (i.e., https) if URL scheme does not exist?
- execution time for retrieving list of valid TLDs (also consider caching)?

### Transcript Filenames

Transcripts will have various filenames, which may not be relevant to their contents

### Direct and Private Messages

(PRIVATE MESSAGE SUPPRESSION NOT YET IMPLEMENTED IN ZOOMCHATTER)

Private (aka direct) messages should be suppressed by default.   They will be processed and returned when the `include_private` flag is set.

Consider that a private message may consist of multiple lines.

Note that historical transcripts may have different wording for private messages, "(Privately)" vs. "(Direct Message)".  Both formats (and any others) should be suppressed.

```
07:14:15 From Terry Smith to Sun Lee(Direct Message) : Can you believe it?!?
```

```
12:32:28\tFrom Terry Smith to Sun Lee (Privately) : Can you believe it?!?
```

### Timestamp/Name Formatting

Still need to validate, but it looks like there may be a difference between transcripts saved to the cloud (alongside recordings) and transcripts saved locally via "Save Chat" in the Zoom desktop client.

Cloud line:

```
00:40:47\tTerry Smith:\tHello, world."
```

Local line:

```
"09:10:55 From Terry Smith to Everyone : Hello, world.",
```

Watch out for other minor formatting differences as well.

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

Note that U+2028 may not be recognized in some text applications; consider replacing it.
