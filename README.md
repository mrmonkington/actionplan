# Actionplan!

Meeting minutes for people who are terrible at writing up meetings.

This project was born out a desire to be able to efficiently take actionable
minutes in technical meetings using any ordinary text editor.

It consists of a minute taking convention and some simple tools for formatting
and publishing these. The ActionPlan format attempts to minimise boilerplate
and repetition so you can take minutes in *real-time*. It's DRY for your meeting.

Actionplan is NOT:

  - a TODO list or task scheduler - it generates tasks but projects and individuals should manage their own todo lists
  - for generating reports for your boss - the audience is typically those who attended a meeting

## Quick reference

```
ap dump - format notes
  --format=
    html, md
ap send - send summary to attendees with their actions highlighted
ap configure
  --smtp
```

## Howto

Write your minutes in Action Plan form, which is a series of nested lists, one
per major project. If a line is an action point, or reflects ongoing work, then
start the line with a `+` rather than a `-`.

A project has a default owner, designated by names(s) in `[]` at the end of a
line and any item in a project can have ownership overriden, which will then be
inherited by that items children.

If you provide a list of people mentioned in the meeting, with email addresses,
then you can use this information to email everybody with their action points using
the `ap send` command.

Storage backends supported:

  - Git
  - Actionplan server?!

### Backlog

  - Publishing to github creates an issue for each meeting with all the actions tickable? (Can this sync back in some way?)

  - You can view outstanding actions for anybody
    - You can limit by a time window

  - Projects can be tagged as belonging to a repository

  - Action points can have very simple and intuitive due date indicators, e.g. "due before next meeting" with less intuitive shortcuts e.g. `=next`, `=10d` `=24/3`

  - You can define regular meeting 'series', e.g. "Weekly tech meeting"
    - Action points from each meeting will carry forward in the 

  - You can flag an item as a decision
    - You can view a list of decisions in reverse chronological order
    - You can view decisions by meeting series
    - You can view decisions by project

You can maintain a contact list in `~/.local/actionplan/contacts.txt`

You can integrate with your directory provider e.g. Google Contacts?

An example should make it a bit clearer.

```
# Weekly meeting

sally: sally@example.com
barry: barry@example.com
gary: gary@example.com
marvin: marvin@example.com
mary: mary@example.com

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

The command `ap dump` will denormalise all of the owners and output
a simple HTML formatte version that you can do a few things with.



```
ap dump actionplan.ap
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

