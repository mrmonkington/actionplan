# Actionplan!

Meeting minutes for pros.

## Howto

Write your minutes in modified markdown form:

```

This is a project owned by sally [sally]
  - This is a note
  + This is an action point for sally
  - This is a note with new owners [barry/gary]
    + This action point will be for barry and gary
    + So will this
  + This AP will be for sally

This other project has a new owner [marvin]
  + AP for [mary]
  + AP for [marvin]

```

Or see `example.ap`.

Pipe it through process.py and it will denormalise all of the owners and output valid markdown.

```

python process.py < actionplan.ap


