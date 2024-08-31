# Behind the scenes

If you're wondering why I needed to write an insert_invisible_char method, it's because of a little quirk in Matrix.
Whenever you type a name, Matrix automatically highlights that message in red, assuming it's a mention.
This highlighting is very distracting for the summaries.
