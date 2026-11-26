# AI Avatars — design & image prompts

Four mascots, one per AI, in the same flat, friendly style as the game
(sticker look, thick outlines, soft rounded shapes — like the Fredoka-font
posters kids know from the slides). Square images, plain/transparent
background, so they fit in circles next to the AI names.

| AI | Mascot | Personality | Palette |
|---|---|---|---|
| Logic | a studious little robot-librarian with square glasses, holding a checklist/rulebook | precise, orderly, a bit pedantic — *"Let me check my rules, in order."* | purple `#6C4FE0`, cream paper |
| Search | a forward-looking scout with a big telescope, branching timeline lines behind it | confident, sees every future — *"I have already looked at every future."* | teal `#15C3B2`, deep navy |
| Probability | a cheerful dice-cube creature tossing two dice, a tally chart pinned behind it | playful, optimistic — *"Roll the dice and count!"* | amber `#FFC53D`, cream |
| RL | a determined baby robot lifting a tiny dumbbell, with a small "LV. 2" badge | eager, growing stronger — *"I start at zero and learn by playing!"* | coral `#F27B9B`, navy |

Shared style (put at the start of every prompt):

> Flat vector mascot illustration for a kids' coding course (ages 13–15),
> thick dark-navy outlines, soft rounded sticker shapes, simple big eyes,
> one or two flat colors per character, subtle hard shadow, clean white
> background, square composition, no text, no watermark.

## Prompt 1 — Logic

> Flat vector mascot illustration for a kids' coding course (ages 13–15),
> thick dark-navy outlines, soft rounded sticker shapes, simple big eyes,
> flat colors, clean white background, square composition, no text.
> A studious little robot-librarian with square glasses holding an open
> rulebook in one hand and a checklist pencil in the other; neat straight
> lines of tiny checkmarks float behind it. Purple body (#6C4FE0), cream
> pages, navy outlines. Friendly, precise, slightly proud expression.

## Prompt 2 — Search

> Flat vector mascot illustration for a kids' coding course (ages 13–15),
> thick dark-navy outlines, soft rounded sticker shapes, simple big eyes,
> flat colors, clean white background, square composition, no text.
> A forward-looking little scout robot holding a big telescope to one eye,
> looking into the distance; behind it, three forking dotted lines
> (branching future paths) ending in small stars. Teal body (#15C3B2),
> navy outlines, small confident smile.

## Prompt 3 — Probability

> Flat vector mascot illustration for a kids' coding course (ages 13–15),
> thick dark-navy outlines, soft rounded sticker shapes, simple big eyes,
> flat colors, clean white background, square composition, no text.
> A cheerful dice-cube creature with stubby arms and legs tossing two
> dice into the air; a small tally chart with checkmarks pinned on a
> board behind it. Amber body (#FFC53D) with white dice, navy outlines,
> big joyful smile.

## Prompt 4 — RL

> Flat vector mascot illustration for a kids' coding course (ages 13–15),
> thick dark-navy outlines, soft rounded sticker shapes, simple big eyes,
> flat colors, clean white background, square composition, no text.
> A determined small baby robot lifting a tiny dumbbell with both hands,
> a small "LV. 2" badge pinned on its chest and a single sweat drop;
> a rising bar-chart of stars behind it. Coral body (#F27B9B), navy
> outlines, proud hopeful expression.

Negative prompt (add to all): `photo, 3D render, realistic, text, letters,
watermark, background scenery, extra limbs, cluttered`

Format: 1024×1024 PNG, transparent or pure-white background.
Once generated, drop the four images in this repo (e.g. `avatars/logic.png`,
`avatars/search.png`, `avatars/probability.png`, `avatars/rl.png`) and the
app can show them next to each AI's name and in its thinking panel.
