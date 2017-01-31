# Actionplan!

Meeting minutes for pros.

## Howto

Write your minutes in Action Plan form:

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

Pipe it through process.py and it will denormalise all of the owners and output a more readable form:

```
python denormalise.py < actionplan.ap
```
Project: This is a project owned by sally  (owner: sally)
   - This is a note
   + This is an action point for sally [sally]
   - This is a note with new owners 
     + This action point will be for barry and gary [barry, gary]
     + So will this [barry, gary]
   + This AP will be for sally [sally]

Project: This other project has a new owner  (owner: marvin)
   + AP for  [mary]
   + AP for  [marvin]

```

