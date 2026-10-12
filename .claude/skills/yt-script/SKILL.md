---
name: yt-script
description: >-
  Write the ElevenLabs narration for a Cirrus Land restoration video - sparse
  documentary lines, one 12-16 word line per 8-second Veo clip, mapped to Veo
  numbers: an imagined-restoration opening, a unique intro per room, silence
  while the crew works, a closing room-by-room recap and a short CTA. Use for
  "narration", "voice-over", "VO script", "write the script for <project>".
---

# yt-script

The voice-over for one restoration video. Not a talking-head script, not a hook generator.

## Read first

1. `voice.md`: voice, narration rules, audio mix, ElevenLabs settings, skill rules. It wins over
   anything here. Look in `youtube/voice.md` (repo), then `~/.claude/youtube/voice.md`, then the
   copy bundled in this skill folder (used in Claude chat, where there is no repo).
2. `production-rules.md`: the project's status, rooms, crews and reveals. Same lookup order.
3. Past narrations: every file in `youtube/narrations/`, or, in Claude chat, any narration the user
   pastes or uploads. Nothing in them may be reused. If none are available, ask for them.

## What you need before writing

The **Veo shot list** for the parts being narrated: Veo number and what is on screen in it, for the
opening, each room intro clip and the recap clips. Narration only goes on documentary / room-intro
clips (and the closing recap). Restoration clips and reveals get no voice.

If the shot list is missing, ask for it. You may draft lines for what is already known, but mark
their Veo IDs `TBD`, and never describe anything not confirmed to be on screen.

## The shape

1. **Opening** (2-4 lines): sets the place and the ruin, and includes one line that says plainly this
   is an imagined, AI-created restoration. Calm, no hype, no question-bait.
2. **Room intros** (1-3 lines per newly entered room, including the exterior): each one different in
   structure and wording from every other intro, in this video and in past ones. Describe what the
   viewer sees as it appears; never announce an action before it is on screen.
3. **Silence** while the crew works. Write `— silence (work sound only) —` rows for those ranges so
   the editor sees the gaps.
4. **Recap** at the end: one line per room, room by room, in order.
5. **CTA**: one short line. Pick-your-room comment ask and/or subscribe. One ask, not three.

## Line rules

- One 8 s Veo = one line, **12-16 words** (6-7 s spoken at speed 0.92, 1-2 s of breathing room).
- Key words in the middle of the line, not at the very start or end, so a trim doesn't cut them.
- Spoken words only: no brackets, stage directions or labels inside the line. Write numbers and
  symbols as they should be said.
- Never claim it is real: no "we found", "our crew", "footage", real place names as the location.
- Whole script **under 10,000 characters**. New wording every project.

## What to hand back

A table, one row per narrated Veo:

| Veo | Line | Target | Delivery | Sync cue |
| --- | --- | --- | --- | --- |
| 000 | the spoken line | 6.5 s | calm, slow, warm | starts as the drone clears the trees |

Then a plain **ElevenLabs paste block**: the lines only, in order, one per paragraph.

Before handing it over, save the table to `youtube/narrations/<project>.md` and run:

```bash
python3 .claude/skills/yt-script/narration_check.py youtube/narrations/<project>.md
```

It checks words per line, total characters, banned real-footage / hype phrases, and any 5-word run
reused from another file in `youtube/narrations/`. Fix every FAIL; rewrite every reused run.

## The gate

Nothing here publishes. End every run with: **ship it, or change it?**
