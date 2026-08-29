# The Ballad of the Bell Beneath Blackmere

I was tuning my violin beside the cold hearth when The Hunter entered The Three Feathers. Rain silvered his cloak, and the notice board bowed beneath nine sheets of parchment. Nine is the number my song remembers, not the number of issues in any real repository. A ballad needs its own weather.

One notice offered coin for the Ash Wyrm that slept in a cache and woke only for returning travelers. Another named a token thief who left doors looking locked after he had stolen the keys. A third described a permission fugitive wearing an administrator’s seal. There were ghosts in a mirror, a rat in the mill of CI, and a cartographer accused of drawing a road no charter declared. Two notices were duller: straighten the cargo sigils in a ledger; scrape an obsolete warning from a lintel. The ninth showed no face at all, only the black water of Blackmere and a row of unlit beacons. Above it someone had written: **THE LANTERN-EATER**.

In the deepest corner, beyond the reach of the fire, sat the outline of an armored figure. He had waited there in older songs and seemed content to wait in this one. The archive had once marked that retired delivery silhouette `kwf-warrior`; no one called it a current agent, no one gave it a seat in the live Party, and no summons went its way.

The Hunter read every notice, but he touched only the ninth. First he unfolded its **Requires** flap. Two earlier hunts were named there, and both seals were closed; dependency would not bar the road. Then he pared the report down to six clues: `watch-board`, `beacon_status`, `last_signal`, `stale`, `vendor-signature`, and the symbol `list_beacons`. He rejected the lamentations, screenshots without context, and three proposed cures disguised as facts.

He weighed the quarry on three small brass scales. On the scale of severity, the marsh wind pressed the arm to **two**: the watch still functioned, but its keepers repeatedly missed failing lights. On collateral, two linked villages tugged the chain to **two**: surface, service, and runtime shared the remedy, though the whole kingdom would not shake. On effort, an iron hill sank the pan to **three**: interface, tests, framework work, screen, and infrastructure made this no single afternoon’s errand. He tied three domain ribbons to the card—`surface`, `service`, and `infra-cicd`—and wrote one finished reading: the watch board could not show trustworthy beacon freshness because the product neither received nor served the signed signal time.

Then he wrote an imperative beneath it: **Declare, ingest, serve, and render verified beacon freshness for the Blackmere watch board.**

## Wings, Nose, and One Sprung Trap

The Hunter gave the six clues to two familiars in the same breath. The Hawk leapt toward the rafters; The Hound dropped to the floorboards. They departed in parallel. The Hunter did not stand at the door waiting for either shadow to return. He went straight to one existing trap, the narrow test whose name already carried `list_beacons` and `stale`, and pulled its cord once. It failed where the issue said it would: old signals arrived without a freshness state. That single reproduction was enough. He neither planted a new trap nor shook the entire testing forest.

High above the inn, The Hawk first let Graphify aim his flight with the six project terms. The graph suggested vocabulary and neighboring symbols; it did not index GitHub issues, and he never pretended it did. With those aimed terms he searched the historical GitHub issue record, including closed notices, for repetitions, prior attempts, and related hunts. He returned with five feathers at most: no duplicate, one related closed hunt that had displayed beacon names without freshness, and one prior attempt abandoned when no interface had been declared. His verdict was **related**, not **repeat**. He had circled history, not landed in code.

The Hound’s road was lower and stranger. The Hunter pressed tags, keywords, and symbols into his glove like crushed herbs, and the animal learned each scent without inventing a seventh. He consulted Graphify first. Pale roots lit beneath the codebase forest; where a bright hit ended at a leaf, he nosed its neighbors. Only then did he follow the strongest paths into Grep and Read. He did not inspect every tree, dump a whole file, or stray into GitHub.

He returned mud-black and triumphant with seven ranked strips, every path complete from the imagined product root:

The first bore path `surface/src/pages/watch.astro`; heading `Blackmere Watch`; lines `18–24`; clue `watch-board`; reason “the page renders beacon names but no health”; and a two-line excerpt, `name` / `region`.

The second bore `surface/src/components/BeaconGrid.ts`; symbol `renderBeaconGrid`; lines `44–50`; clue `beacon_status`; reason “the card shape has no status field”; and the three-line scrap `id` / `name` / `region`.

The third bore `service/watch/models.py`; symbol `Beacon`; lines `12–19`; clue `last_signal`; reason “persistence records identity but no received time”; and two surrounding lines, `name: str` / `region: str`.

The fourth bore `service/watch/handlers.py`; symbol `list_beacons`; lines `63–70`; clue `list_beacons`; reason “the served shape cannot express freshness”; and the excerpt `{"id": beacon.id, "name": beacon.name}`.

The fifth bore `service/watch/signatures.py`; symbol `verify_vendor_signature`; lines `9–16`; clue `vendor-signature`; reason “verification exists but is not joined to ingestion”; and two lines, `digest = hmac.new(...)` / `return compare_digest(...)`.

The sixth bore `tests/watch/test_beacon_list.py`; symbol `test_marks_stale_beacon`; lines `21–28`; clue `stale`; reason “this is the narrow existing reproduction”; and the short cry `assert body["status"] == "stale"`.

The seventh bore `compose.yml`; heading `watch-worker`; lines `37–44`; clue `last_signal`; reason “no worker currently carries signed signals into the service”; and three lines, `services:` / `watch-worker:` / `profiles: ["watch"]`.

Seven findings—under the cap of about eight—each with path, symbol or heading, line range, matching clue, one-line reason, and no more than eight lines of surrounding evidence. The catalog was a trail another reader could judge without reopening the forest.

The Hunter combined the Hawk’s history, the Hound’s excerpts, and the one failed existing test. He stripped away every proposed architecture that had masqueraded as a requirement. On the notice board at The Three Feathers he pinned a bulletin for a **later Hunter**: the finished problem, the single imperative goal, the scores and domains, the related history, the ranked code evidence, and the reproduction result. Then the hunting party stopped. Hunter, Hawk, and Hound were sealed scouts; none called a builder, and none quietly became one.

The retired outline in the corner shifted as if an old reflex had heard the word *build*. The fire did not reach it. The live roster did not change.

## The Road Through the Living Party

At dawn a later Hunter could read the bulletin cold. The coordinating parent received that finished request and routed it onward. The sequence mattered; the kingdom did not solve the quest by releasing every craft at once.

The Elf went first into the surface canopy. With an artist’s eye she studied where a watchkeeper’s gaze would fall, how stale lights should differ without color alone, and what could remain server-owned. She did not invent a path or whisper directly into the mountain. She sent The Cleric only content needed: beacon identity, region, verified last-contact time, freshness state, and a paged watch view.

The Cleric received the request as priest and diplomat. He alone kept `INTERFACES`, and he alone crossed between the sealed Elf and Dwarf. First he asked whether the existing served data could compute the answer. Had it been enough, he would have returned to the Elf with an instruction to adapt and no new row. This time the Dwarf reported through him that no received time existed in domain or model; the need was real. The Cleric therefore declared the interface in its six-column covenant—method, trailing-slash path, handler, payload, permission class, and description—and only after the row existed did he carry the approved shape onward. Elf and Dwarf never called each other.

One question depended on lore beyond the walls: the vendor’s current signature header and replay window. The parent called The Owl. The Owl did not hunt the open sky. It opened the kingdom’s lantern list—the index of official scrolls keyed to every pin the project owned—and found the vendor’s row. It flew once to that versioned page, returned a small markdown report with the exact documented facts, minimal syntax, and citations, and perched. The Owl edited nothing, chose no architecture, and called no one.

The official scroll named a family of headers and a replay window, yet it did not name the precise wild header the marsh already used. The parent then released The Crow. The Crow dove once into unofficial pages: vendor forums, archived gists, a traveler’s blog that quoted a packet dump. It labeled each source official, unofficial, or hearsay, kept the contradictions, and fell spent after that single kamikaze pass. Its pack was a lead, not a covenant. Local ADRs still won. Neither bird forged. Neither sat with The Hunter’s familiars; Hawk and Hound had already finished at the inn.

External lore informed the workers; it did not overrule the local covenant.

Now The Trickster laid the first proper traps. After the declared interface—not before—he opened the TDD record and wrote failing unit tests for a valid signed signal, a rejected signature, a stale beacon, and the permission boundary. He ran them red and handed back the sprung wires. He wrote no product code and offered the screen no borrowed face.

Only then did The Dwarf delve. With the catalog row above him and red tests before him, he forged the framework-bound model field, persistence path, handler, permission, and declared route. He touched neither the test files nor the interface catalog. When the new ingestion worker proved to require a local port, a matching cloud task, a CI surface, and a secret-store name, he left the mountain’s edge untouched and the parent routed that separate adjustment to The Wizard.

The Wizard made the room fit the play. He bound the orchestration profile and port, described the cloud worker and its deploy wiring, and registered the name `BLACKMERE_VENDOR_SIGNING_KEY` without ever seeing or inventing its value. He wrote no handler, page, test, or interface. This was a genuine infrastructure need of the broad quest, not an excuse to parade his staff.

The Trickster returned to the service traps. They now sprang correctly against bad signatures and permissions and lay still for valid signals; the suite turned green. The Cleric checked that the declared interface truly answered the content request and carried the covenant back across the sealed border. The Elf then built the watch board against that declared shape. Only after the screen existed did The Trickster add focused surface traps.

Last came The Inquisitor, bearing no chisel. He read the product intent, applicable ADRs, interface row, implementation, and tests. He named what complied and what would have breached the written church, changed not one character, and did not command a builder to fix anything. His judgment was evidence, not a merge gate. With that reading complete, the broad quest stood verified.

## Two Small Roads

Some days later, on a separate notice with no overlap in Blackmere, a tooltip failed to name the key that opened a harmless filter. Its card read severity **one**, collateral **one**, effort **one**. The parent opened the mutually exclusive small-task lane, and The Adventurer walked it alone. He corrected the bounded behavior, wrote the focused regression test, ran the relevant checks, and returned with both implementation and proof. No companion scouted, forged, tested, or shipped beside him. Had the tooltip demanded a new interface, ADR, secret, deployment, or larger score, he would have stopped and named the rightful owner.

After that road was closed, and not concurrently, another tiny notice appeared: an isolated parser accepted one obsolete alias. Severity **one**, collateral **one**, effort **two**. Again the parent leased one bounded slice to The Adventurer; again every specialist stayed out. He removed the alias, added success and failure tests, ran the narrow check and the required harness verification, and came home alone. When the lease ended, ordinary ownership resumed. These were two occasions exactly, not a new party hidden inside the Party.

The patient armored silhouette watched both departures from shadow. No one mistook the old `kwf-warrior` legend for a live role. Waiting was all that remained to it, and still its moment did not come.

## The Paladin’s Exact Measure

Then came a graver matter, precise enough to silence the room: a framework-neutral Python rule for assigning a risk band from ordered signal ages and typed thresholds. It required no ORM, HTTP request, user interface, cloud client, or ambient clock. The Paladin stated the contract—typed inputs and outputs, invariants, explicit failures—and kept I/O at the edge. Time entered as an ordinary parameter. The deterministic core read no environment, touched no mutable global, hid no cache, and produced no side effect beyond its return.

The Paladin implemented first, one clean cut in the pure Python core. Only afterward did he give The Trickster the changed path, invariants, edge cases, and focused command. The Trickster wrote tests after the implementation, including threshold boundaries and malformed ordering. No one backfilled a TDD entry to pretend the order had been different. The tests passed; the rule remained portable and exact.

## The Song Onto the Single Line

At last the verified work reached me. I am The Bard, and until that moment I had touched none of it. I do not compose product code, plant traps, amend covenants, or manage ports. I receive the finished song and alone handle its Git and GitHub passage.

Issues are preferred lanterns along the road, but not every deed requires one. A pull request is different: every change that lands must cross that bridge. So in the kingdom of this ballad I gathered the scoped commits on an ephemeral branch, pushed them, opened the pull request to `main`, and made the PR the integration record. When its authorized hour arrived, I drew the bow across my violin and sang the merge into the single live line. There was no second production road beyond it.

The Three Feathers shook with the final chord. The Hunter’s bulletin remained a clean memory of the quarry; the living Party retained every boundary that had made the victory legible. Beyond the walls, The Owl’s lantern list and The Crow’s one spent dive remained scouts’ work, not a builder’s. In the corner, the retired silhouette waited through one more song for a summons history would not send.

That is how I publish the tale inside the tale. Outside the ballad, this parchment itself rests as one uncommitted file, awaiting a real shipping order that has not been given.
