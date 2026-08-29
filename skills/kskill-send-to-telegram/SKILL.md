---
name: kskill-send-to-telegram
description: ALWAYS use this skill to send ANYTHING to kodex's Telegram / phone — text, a link, an image, video, audio, a file, a report, or terminal output. This is the ONE way to reach his Telegram; never hand-roll a curl to the Bot API. Trigger on ANY mention of sending/forwarding to Telegram or his phone, in English or Spanish and no matter how short: "send to telegram", "mandá/enviá esto a telegram", "pasame esto al celu/celular", "mandámelo por telegram", "a mi telegram", "for the phone", "send it to my telegram", or a task ending in "→ telegram". Picking the bot, escaping HTML, resolving the token (the `kdx-bot-token` helper handles it for whichever Unix user you are — do NOT `source` an .env, do NOT hand-roll `sudo`), and the curl are all handled inside; you only need the content. Works as kodex AND inside the sudo-less pykodex sandbox. TWO channels: REPORT OUTPUT (formatted reports, summaries, html, media) → @KdxHQBot (default); TERMINAL OUTPUT (raw command/terminal logs, plain dumps) → @KdxTuringBot.
---

# kskill-send-to-telegram

Send content to kodex's Telegram DM in one curl. kodex's DM chat id is fixed
(`780726530`); the only secret is the bot token.

## Two channels — pick the right bot

| Channel | Bot | Use for |
|---|---|---|
| **REPORT OUTPUT** (default) | `@KdxHQBot` | Reports, summaries, html artifacts, status updates, anything formatted/curated, media |
| **TERMINAL OUTPUT** | `@KdxTuringBot` | Raw terminal/command output, logs, plain dumps |

When in doubt, it's a **report** → use `@KdxHQBot`. Only use the Turing bot when
explicitly relaying raw terminal/log output.

## Constants

| What | Value |
|---|---|
| Chat id (kodex DM) | `780726530` |
| Token resolver | `/home/kodex/Skills/kskill-send-to-telegram/kdx-bot-token <report\|terminal>` |

**Never print or echo a token.** Capture it into a shell var and use it inline.
Always go through the resolver — never read an `.env` yourself, never hand-roll
`sudo`. The curl itself may need sandbox disabled.

## Recipes

Get the token for your channel, then build `$API`:

```bash
# REPORT OUTPUT (default):
TOKEN=$(/home/kodex/Skills/kskill-send-to-telegram/kdx-bot-token report)
# — or — TERMINAL OUTPUT:
# TOKEN=$(/home/kodex/Skills/kskill-send-to-telegram/kdx-bot-token terminal)
API="https://api.telegram.org/bot${TOKEN}"
```

> [!info] Why a resolver and not `sudo`
> The same skill runs under two Unix users. **kodex** has NOPASSWD sudo and no local
> copy, so the resolver reads the root-only `.env`. The **pykodex sandbox has no sudo
> at all**, so it reads its own `0600` copy under `~/.config/{kdxhq-bot,turing-bot}/.env`.
> Local copy wins when present; the sandbox never needs privilege. When neither a local
> copy nor a readable root `.env` exists, a **third lane** reads the token from AWS
> Secrets Manager — the durable, file-free fallback, gated on `KDX_BOT_TOKEN_SECRET_ID`
> (see *Context* → *Durable provisioning*). Full sandbox map:
> `~/Documents/System/ADRs/20260706-pykodex-sandbox-user.md`.

**Text** (HTML formatting; max 4096 chars per message — split if longer):

```bash
curl -s -F chat_id=780726530 -F parse_mode=HTML \
  --form-string "text=$(cat /tmp/msg.html)" "$API/sendMessage"
```

**Image / Video / Audio** (captions max 1024 chars, parse_mode works too):

```bash
curl -s -F chat_id=780726530 -F caption="..." -F photo=@file.png "$API/sendPhoto"
curl -s -F chat_id=780726530 -F caption="..." -F video=@file.mp4 "$API/sendVideo"
curl -s -F chat_id=780726530 -F caption="..." -F title="..." -F audio=@file.mp3 "$API/sendAudio"
```

(`sendDocument` with `document=@file` for anything else: PDF, zip, etc.)

**Verify**: pipe the response through `python3 -c "import json,sys; r=json.load(sys.stdin); print('ok:', r['ok'], '| message_id:', r.get('result',{}).get('message_id'), '|', r.get('description',''))"` and report ok + message_id. If `ok: False`, the description says why (entity parse errors usually mean malformed HTML — escape `<`, `>`, `&` in content; `chat not found` means kodex hasn't pressed Start on that bot yet).

## HTML formatting notes (text & captions)

- Allowed: `<b> <i> <u> <s> <code> <pre> <a href> <blockquote> <tg-spoiler>`.
  No `<br>` — use real newlines. Emoji are fine and render well.
- Generating audio first? No local TTS installed; use
  `uvx edge-tts --voice es-AR-TomasNeural --file guion.txt --write-media out.mp3`.

## Context

Two **dedicated** bots, both separate from the Hermes/Ada gateway bot
(`@KdxAdaBot`) so sends never collide with the agent's messaging:

- `@KdxHQBot` (id `8852504779`) — REPORT OUTPUT. Token at
  `/root/.config/kdxhq-bot/.env`.
- `@KdxTuringBot` (id `8667195754`) — TERMINAL OUTPUT. Token at
  `/root/.config/turing-bot/.env`.

Both root token files are perms `600`, root-only (kodex has NOPASSWD sudo to read).
The `pykodex` sandbox holds `600` copies of both under its own
`~/.config/{kdxhq-bot,turing-bot}/.env` — rotate a bot token and you must rewrite
those copies too.

### Durable provisioning (AWS Secrets Manager)

The two file lanes above are lost by a fresh clone or a clean — no token file lives
in the repo. The **durable** lane is a third fallback: set `KDX_BOT_TOKEN_SECRET_ID`
to a Secrets Manager secret whose `SecretString` is JSON keyed by the same var names
the `.env` files use —

```json
{"KDXHQ_BOT_TOKEN": "…", "TURING_BOT_TOKEN": "…"}
```

— and the resolver reads it as its **last** lane (ambient AWS profile, region
`AWS_REGION` or `us-east-1`) only when no local copy and no readable root `.env`
exist. This is the fix for the kodex-lane clean-loss problem: the token stops being
a hand-copied file. Provisioning the secret once (e.g. via the
`kskill-aws-secrets-create` skill) is a one-time operator step, not part of a normal
send. Which AWS account holds the secret is an operator decision made at
provisioning time — the resolver hardcodes no secret id and no account.

Honest limit: the lane is inert until **both** the secret exists AND
`KDX_BOT_TOKEN_SECRET_ID` is exported at the machine level — it survives a clean on a
configured machine, not a zero-config fresh clone.

Direct Bot API is faster and deterministic than going through the Hermes agent.
Hermes/Ada gateway (the other bot) is documented in
`/home/kodex/Documents/System/Hermes/HERMES-AGENT.md`.
