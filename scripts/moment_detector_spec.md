# Moment Detector Specification

## Purpose

Identify potentially interesting poker moments from a ClubWPT recording.

The output should be a timestamped event list.

---

## Phase 1 Goal

Reduce a 1-3 hour session into approximately 10-50 candidate moments for review.

---

## Event Types

### All-In

Description:

One or more players commit entire stack.

Priority:

High

---

### Showdown

Description:

Multiple hands revealed.

Priority:

High

---

### Large Pot

Description:

Pot exceeds configurable threshold.

Priority:

High

---

### Significant Stack Change

Description:

Player stack changes significantly after a hand.

Priority:

Medium

---

### Long Tank

Description:

Player takes significantly longer than normal to act.

Priority:

Medium

---

### Replay Opened

Description:

Hand replay window appears.

Priority:

Medium

---

### Hole Card Reveal

Description:

Opponent cards revealed through ClubWPT feature.

Priority:

High

---

### Rabbit Hunt

Description:

Rabbit hunt window appears.

Priority:

Low

---

## Output Format

Example:

00:12:14 - Large Pot

00:24:09 - Showdown

00:41:32 - All-In

---

## Success Criteria

A reviewer should be able to locate the most interesting hands of a session without watching the entire recording.

---

## Deferred Features

Not required for Phase 1:

* Hand reconstruction
* Commentary generation
* Podcast generation
* Avatar generation

