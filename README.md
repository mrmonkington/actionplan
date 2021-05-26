# Actionplan!

Meeting minutes for people who are terrible at writing up meetings.

This project was born out a desire to be able to efficiently take actionable
minutes in technical meetings using any ordinary text editor.

It consists of a minute taking convention and some simple tools for formatting
and publishing these. The ActionPlan format attempts to minimise boilerplate
and repetition so you can take minutes in *real-time*. It's DRY for your meeting.
 TODO OR
It consists of a minute taking convention, a simple configuration and team manifest, and some simple tools for formatting
and publishing your meeting notes. The ActionPlan format attempts to minimise boilerplate
and enable you to use your prefered tools to concentrate on writing what's said in meetings, rather than 

Actionplan is NOT:

  - a TODO list or task scheduler - it generates tasks but projects and individuals should manage their own todo lists
  - for generating reports for your boss - the audience is typically those who attended a meeting

## Quick reference

```
ap [new] <new file> - opens your default editor for <new file> and on close will lint with ap check
ap check - make sure the minutes parse ok
ap next <previous meeting file> - start a new meeting using the title and agenda from a previous meeting as a template
ap dump - format notes, denormalising owners
  --format=md|gh|html     - md is default
                          - gh is github flava'd markdown format useful for putting into an issue (you can then tick off the actions using browser interface)
                          - html is very vanilla and ideal for email
  --highlight <attendee> - highlight all actions for attendee, may be specified multiple times, works best in html
  --actionsonly - just dump actions and context for action, no other items
  --
ap send - send summary to attendees, formatted as HTML, with their actions highlighted
ap config
  dump - show current settings, including team and defaults
  addteam [meeting.ap [meeting.ap ...]] - add people from meetings to team, will error on conflicts and won't merge
  testsmtp <email address> - test the SMTP settings by emailing something nice to somebody (tip: don't spam)
ap contacts
  list
  merge
ap serve - runs a little minutes server, perfectly good for internal prod
ap review - steps through actions
ap git init - init a new actionplan notes repo (doesn't do anything special)
ap git push - shortcut for whatever git commands are need to push everything that's changed
ap git pull - ditto but for pulling
```

## Settings

```
EDITOR=vim right?
DEFAULT_MINUTES_FOLDER
MINUTES_SERVER_URL
```

## Howto

Write your minutes in Action Plan form, which is really just markdown with a few conventions. Any valid markdown file is also a valid action plan and vice versa.

The example in [docs/example.ap] should be pretty clear. But just in case...

An action plan file is split in to sections though almost everything is optional:

  - Attending (optional) - both for your own reference but also a shorthand for introducing new team members (see [#team-management])
  - Agenda (optional) - can be used to quickly populate all the section titles
  - Projects

Most of the action occurs in nested lists, which is how many people take meeting notes.

The most basic Action Plan is just a naked 

If a line is an action point, or reflects ongoing work, then
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

  - Switch to Marko for parsing
    - Update AST to include owners and denormalise
    - Create custom Marko renderers for everything

  - Publishing to github creates an issue for each meeting with all the actions tickable? (Can this sync back in some way?)

  - You can view outstanding actions for anybody
    - You can limit by a time window

  - Projects can be tagged as belonging to a repository

  - Action points can have very simple and intuitive due date indicators, e.g. "due before next meeting" with less intuitive shortcuts e.g. `=next`, `=10d` `=24/3`

  - You can define regular meeting 'series', e.g. "Weekly tech meeting" - why not just use folders?
    - Action points from each meeting will carry forward in the 

  - You can flag an item as a decision
    - You can view a list of decisions in reverse chronological order
    - You can view decisions by meeting series
    - You can view decisions by project

  - Host in charm cloud?! https://charm.sh/

  - Use Click for cli

You can maintain a contact list in `~/.local/actionplan/contacts.txt`

You can integrate with your directory provider e.g. Google Contacts?

