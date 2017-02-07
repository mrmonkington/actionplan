# Actionplan!

Meeting minutes for pros.

This project was born out a desire to be able to efficiently take actionable
minutes in technical meetings using any ordinary text editor.

It consists of a minute taking convention and some simple tools for formatting
and publishing these. The ActionPlan format attempts to minimise boilerplate
and 

## Howto

Write your minutes in Action Plan form, which is a series of nested lists, one
per major project. If a line is an action point, or reflects ongoing work, then
start the line with a `+` rather than a `-`.

A project has a default owner, designated by names(s) in `[]` at the end of a
line and any item in a project can have ownership overriden, which will then be
inherited by that items children.

An example should make it a bit clearer.

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

Pipe it through process.py and it will denormalise all of the owners and output
a markdown compatible form that will render well on github, complete with
checkboxes for action points.

```
python denormalise.py < actionplan.ap
```

```
**Project: This is a project owned by sally**  (owner: sally)

   - This is a note
   - [ ] This is an action point for sally [sally]
   - This is a note with new owners 
     - [ ] This action point will be for barry and gary [barry, gary]
     - [ ] So will this [barry, gary]
   - [ ] This AP will be for sally [sally]

Project: This other project has a new owner  (owner: marvin)
   - [ ] AP for  [mary]
   - [ ] AP for  [marvin]
```

