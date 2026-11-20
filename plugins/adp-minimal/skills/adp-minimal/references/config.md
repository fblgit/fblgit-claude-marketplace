> Copy of [`docs/config.md`](https://github.com/fblgit/artifacts-done-properly/blob/3f0062952f499370f88200d114e954bff82fe841/docs/config.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# Config: the switches of an ADP page

This is the reference for ADP's settings, called switches. Everything below is stated from the code and names the file and function it comes from. Where a switch does nothing, the table says so.

Sources: `plugins/artifacts-done-properly/skills/adp/assets/adp.js` (the runtime, section "config"), `plugins/artifacts-done-properly/skills/adp/scripts/adp.py` (`CORE`, `guard`, `config_cmd`, `hold`, `record`), `plugins/artifacts-done-properly/skills/adp/catalog/kit/patterns/settings.js`, `plugins/artifacts-done-properly/skills/adp/catalog/kit/patterns/namespaces.js`, `plugins/artifacts-done-properly/skills/adp/catalog/kit/patterns/playground.js`, `plugins/artifacts-done-properly/skills/adp/catalog/kit/patterns/assist.js`, `plugins/artifacts-done-properly/skills/adp/templates/starter/parts/app.js.txt`. `plugins/artifacts-done-properly/skills/adp/catalog/adp.js` is byte-identical to `plugins/artifacts-done-properly/skills/adp/assets/adp.js` at the time of writing.

## 1. What a switch is

A switch is one named value, `group.name`, in lower case with dashes allowed (`edit.locked`, `log.data-changes`). The runtime checks each segment against `/^[a-z0-9][a-z0-9-]*$/` (`define` in adp.js); `adp.py config set` checks the whole key against `KEY` (`config_cmd`).

All values live in one database document, `config/current`:

```
{schema: 'adp-config/1', at: <ISO time>, by: <who>, values: {key: value}, changed: {key: {by, at}}}
```

- `values` holds only keys whose value differs from the default. `set` in adp.js deletes the key from `values` when the new value equals the default (compared with `JSON.stringify`); `reset()` with no argument empties both `values` and `changed`; `reset(key)` is `set(key, default)`.
- `changed[key]` is `{by, at}` of the last write to that key. It is what the lock banner and the settings page use for "by".
- `get(key)` returns `values[key]` if present, else the registered default, else `undefined` for an unregistered key (`get` in adp.js).
- Without a database (`db` null) or before a snapshot, every `get` returns the default.

Switch types and their defaults when a definition gives none (`dflt` in adp.js): `bool` false, `list` [], every other type `''`.

| type | accepted by `ADP.config.set` (`check1` in adp.js) |
|---|---|
| bool | a JS boolean |
| enum | a value in `options` (strict `includes`) |
| url | a string that is `''` or starts with `https://` |
| list | an array of strings |
| datetime | `''` or a string `Date.parse` accepts |
| text | a string of at most 2000 characters |

An unknown key makes `set` reject with `Unknown setting <key>`.

## 2. The registry

Sixteen core switches are registered at load by `define(...)` calls at the end of the config section of adp.js. `CORE` in adp.py lists the same sixteen with the same type, default and options (a comment there says adp.js is the source of truth), except `look.theme`: its options and its default belong to the page, so `CORE` gives it options `None` and the default `default`.

Core switches carry no `level`, so `define` gives each `level: 'page'`. No core switch uses `level: 'db'`.

"Read by" lists every place in the adp skill (`skills/adp/`) that reads the switch. "None" means no reader was found by searching the adp skill for the key, for `get('<key>')`, and for the group's use.

| key | type | default | options | read by | effect |
|---|---|---|---|---|---|
| `edit.locked` | bool | false | | adp.js `effects`, `check`; settings.js `save`, `refresh`; adp.py `guard` | Sets `data-adp-locked` on `<html>`. The runtime stylesheet then gives every `[data-adp-edit]` `pointer-events: none; opacity: .55` and a banner `div.adp-lock` (role status) is placed first in `<body>`. `check` copies the value to `checks/latest` as `locked`. adp.py `hold` and `record` refuse with exit 2 when it is true. |
| `edit.until` | datetime | `''` | | adp.js `effects` | Text of the banner only ("until <date>"). Nothing lifts the freeze at that time. adp.py does not read it. |
| `edit.reason` | text | `''` | | adp.js `effects`; adp.py `guard` | Text of the banner; the `reason` field of the adp.py `locked` error. |
| `edit.require-hold` | bool | false | | adp.py `guard` (only through `record`) | `record` refuses changed existing parts that have no holder in `--holds`. The page does not read it. |
| `parts.locked` | list | `[]` | | adp.js `partLocked` via `label`; namespaces.js `locks`; adp.py `guard` | In the page: the label of a comment anchor on a locked part gets the prefix "locked: " (with a lock emoji). In adp.py: `hold` and `record` refuse parts under a listed prefix. Whole-segment prefix match. |
| `comments.enabled` | bool | true | | none | Registered and shown on the settings page, but nothing in the adp skill (`skills/adp/`) reads it. It changes no behaviour. |
| `panel.changes` | enum | everyone | everyone, editors, off | adp.js `hideChanges`, `panels` | Sets `hidden` on every `[data-part="page.changes"]` when the value is `off`, or is `editors` and the viewer cannot edit. |
| `panel.checks` | enum | editors | everyone, editors, off | adp.js `badge` | `badge` fills the text of every `[data-adp-integrity]` element. It returns without touching them when the value is `off`, or is `editors` and the viewer cannot edit (the elements are not hidden, just not filled). |
| `playground.enabled` | bool | true | | playground.js `isOff` | When it is exactly false the playground renders one line and nothing else; re-checked on change. |
| `look.theme` | enum | the theme `index.html` links (`kit/themes/<name>.css`, read when adp.js loads), else `default` | that one theme; on a page with a theme switch, the themes it has installed | adp.js `effects`; `plugins/artifacts-done-properly/skills/adp/templates/assistant/parts/app.js.txt` | adp.js sets the attribute `data-adp-theme` on `<html>` and nothing else, so on a page without a theme switch (the starter) the setting offers one choice and changes nothing. The assistant and default templates define the switch again with the themes in `installed.json` and wear the chosen one through `kit.skins` (`docs/themes.md`, "At runtime"); a viewer's own pick in the header wins over it in that browser. |
| `look.mode` | enum | auto | auto, light, dark | adp.js `effects` | `light` or `dark` sets `data-theme` on `<html>`; `auto` removes the attribute. |
| `look.density` | enum | comfortable | comfortable, compact | adp.js `effects` | Sets `data-adp-density` on `<html>` (removed when empty). No stylesheet or script in the adp skill (`skills/adp/`) reads that attribute. |
| `links.catalog` | url | `''` | | adp.py `take` | The catalog URL `take` uses when a local `catalog.json` is given, no `--url` is passed and `--config` is passed. |
| `links.board` | url | `''` | | none | Registered only. adp.py `config DIR` prints every `links.*` value under `links`. |
| `links.repo` | url | `''` | | none | As `links.board`. |
| `log.data-changes` | bool | true | | adp.js `write`; adp.py `config_cmd` | When not false, each write of `config/current` also writes a `changes/d-<ms>` doc (section 4). |

### Switches that kits and templates define

A kit or a page adds a switch with `ADP.config.define(group, {name: {type, default, label, help, options, level}})`. `define` rejects a bad group or name, stores `type` (default `text`), `level` (default `page`) and `default`, and re-runs the page effects if the config is already ready. A switch defined after load appears in `all()` and on the settings page; nothing is written to `config/current` until it is set.

Defined in the adp skill (`skills/adp/`):

| key | type | default | options | defined in | read by |
|---|---|---|---|---|---|
| `assist.enabled` | bool | true | | assist.js | assist.js (`enabled`) |
| `assist.lanes` | list | ask, task, fix, design | | assist.js | assist.js (`lanes`), assist-panel.js |
| `assist.ask-now` | bool | true | | assist.js | assist.js, assist-panel.js |
| `assist.presence-minutes` | enum | 5 | 2, 5, 15 (strings) | assist.js | assist.js; inbox.js |
| `assist.shortcut` | text | Mod+Shift+K | | assist.js | assist.js, assist-panel.js |
| `page.show-about` | bool | true | | `plugins/artifacts-done-properly/skills/adp/templates/starter/parts/app.js.txt` and `plugins/artifacts-done-properly/skills/adp/templates/assistant/parts/app.js.txt` | the same files: `ADP.config.on('page.show-about', ...)` hides `[data-part="home.about"]` |
| `look.theme` (defined again) | enum | as in the runtime | the themes in `installed.json`, Default first | `plugins/artifacts-done-properly/skills/adp/templates/assistant/parts/app.js.txt` | the same file: `ADP.config.on('look.theme', ...)` wears the theme |

assist.js defines its five switches only when `H.config.define` exists, and reads each through a helper that falls back to its own default. inbox.js reads `assist.presence-minutes` as `Number(...) || 5`, so it uses 5 minutes when the switch is not defined or not a number; with the switch defined the value is also 5 unless changed. docs/assist.md covers what the assist switches do.

## 3. Soft layer and hard layer

adp.js says the switches are a soft layer and the database rules are the hard one. This is what each layer does.

### What the page does (adp.js, settings.js)

- `edit.locked` true: CSS makes `[data-adp-edit]` elements unclickable and dimmed, and the banner is shown. That is all adp.js does. The CSS blocks pointer input only; it does not disable keyboard or script access, and it does not touch elements without `data-adp-edit`.
- `ADP.config.set` and `reset` do not check `edit.locked`. A script can still write `config/current` while editing is paused, if the viewer can edit.
- The settings page (settings.js `save`) does check: while `edit.locked` is true it refuses to save any switch except `edit.locked`, `edit.until` and `edit.reason` (the `UNLOCK` list), with "Editing is paused, so this was not saved." Those three controls and their Undo carry `data-adp-unlock` instead of `data-adp-edit`, and `settings.css` keeps them clickable under `html[data-adp-locked]`. The Reset all button carries `data-adp-edit`.
- Every write in adp.js requires `canEdit` and a database (section 4). A viewer who cannot edit gets the controls disabled on the settings page.
- `parts.locked` in the page only changes the anchor label (a lock marker) and what namespaces.js lists under "Locked parts". It does not stop anyone from editing a part.

### What adp.py does (`guard`)

`guard` runs only when `--config C.json` is passed. `C.json` is `config/current` as read, bare or wrapped in `data` (`read_doc`). Defaults from `CORE` fill any key missing from `values`. It runs in `hold` (with the part ids given) and `record` (with the ids added, changed or removed between OLD.json and the DIR manifest). On a refusal it prints a JSON object and exits 2. The checks run in this order:

1. `edit.locked` is true: `{"error": "locked", "by", "at", "reason"}`. `by` and `at` come from `changed['edit.locked']`, else the doc's own `by` and `at`.
2. A touched part id falls under a `parts.locked` prefix and that prefix is not named by `--unlock PREFIX` (exact string equality with the prefix): `{"error": "locked parts", "parts": [...]}`. Matching is by whole segment (`under`): prefix `core` matches `core` and `core.x`, not `corex`.
3. `edit.require-hold` is true and `record` was called (only `record` passes the `deepest` set): without `--holds` it refuses with `{"error": "unheld", "parts": [...], "note": ...}`; with `--holds H.json` it refuses the changed parts that already exist in OLD.json, have no changed child part, and have no holder in H.json (`{"error": "unheld", "parts": [...]}`). New parts are not checked. A holder is `H[id].holder` or `H[id]` when it is a string. `hold_until` is not checked, so an expired hold counts.

Without `--config`, none of this runs.

### What neither layer stops

- adp.py never reads the database. It relies on the `config/current` the caller passes; a stale or omitted `--config` is not detected.
- A publish by any other route (the Artifact tool directly, a hand-edited file) bypasses `guard`.
- `edit.until`, `edit.reason`, `comments.enabled`, `links.board`, `links.repo`, `look.theme` and `look.density` enforce nothing.

### The hard layer

Who can write which database path is set by the rules in the page's `<meta name="adp:db-rules">`. In the three templates under `plugins/artifacts-done-properly/skills/adp/templates/`, the first rule is `{"path":"","read":"view","write":"admin"}`, so `config/current`, like any path without a more specific rule, needs `admin` to write; `ns/shared`, `ns/users/{self}` and (starter) `status` or (assistant, default) `requests`, `conversations`, `presence` need `interact`. namespaces.js draws these rules. The code in this repository declares the rules; it does not enforce them, so what the platform enforces beyond that cannot be checked here. The adp.js write path itself writes only if `canEdit` is true.

## 4. Reading and writing

`window.ADP.config` is frozen and has `define`, `get`, `all`, `on`, `set`, `reset`, `ready` and `doc`.

| member | what it does |
|---|---|
| `get(key)` | current value (section 1). |
| `all()` | `{group: {name: {...definition, value, changed}}}`, where `changed` is `{by, at}` or null. |
| `on(key, fn)` | calls `fn(value, key)` on a change of that key. `on('*', fn)` is called for every key. Returns an unsubscribe function. When already ready, `fn` is called once, asynchronously, straight away. |
| `ready` | a promise that resolves after the first `config/current` snapshot, or at once when there is no `window.claude` or no database, or when the snapshot errors. |
| `doc` | the last `config/current` data, or null. |
| `set(key, value)` | validates (`check1`), then writes. Rejects with the validation error. |
| `reset(key)` / `reset()` | `reset(key)` sets the default; `reset()` empties `values` and `changed`. |

On the first ready, each registered listener is called once with the current value; a `'*'` listener gets `undefined` and `'*'` in that call. After that, a snapshot change fires the listeners of each key whose value differs from before and re-applies the page effects.

### The write (`write` in adp.js)

1. Waits for `ready`. Rejects with "Settings cannot be saved here: this page has no database." when there is no database, and with "Settings cannot be saved: you cannot edit this artifact." when `canEdit` is false.
2. Tries at most twice: reads `config/current`, applies the edit to the `values` and `changed` it just read, and sets `{schema: 'adp-config/1', at, by, values, changed}`. `by` is `ADP.user.id`, else `page`. The page's db handle returns no version, so the write is unpinned (last writer wins); the retry only re-reads and merges once. After the second failure the error is thrown.
3. `set` stores `changed[key] = {by, at}` even when the value goes back to its default (the key is then removed from `values` but stays in `changed`).
4. When `log.data-changes` is not false, it then writes `changes/d-<Date.now()>` with `{version: '', at, by, summary: 'Set <key> = <json>' (or 'Reset all settings'), parts: [], threads: [], data: [{doc: 'config/current'}]}`. A failure of this second write is swallowed.

### The pinned write (`adp.py config set KEY VALUE`)

`adp.py config set KEY VALUE [--doc C.json] [--by NAME] [--pins P.json] [--out DIR]` builds the same document and the same `changes/d-<ms>` record as files, as an ArtifactData batch (see `Batch` in adp.py); it does not call the database. It differs from the page in these observed ways:

- VALUE is parsed as JSON when it parses, else taken as text. `check_value` validates it against `CORE` with the same rules as `check1`: text of at most 2000 characters, url `''` or `https://` only, datetime `''` or an ISO date or date-time that is a real moment (`real_date`: a regex for the shape, then `datetime.fromisoformat` with a trailing `Z` read as UTC, so `2026-13-45` and `T25:00` fail). A mismatch exits 1 with one line on stderr.
- A key not in `CORE` is accepted if it matches `KEY`, and its value is not type-checked (Python cannot know its type); the output then carries `"unknown": true`. This is intentional: pages define their own switches (for example `assist.lanes`) that `CORE` does not list. The page rejects unknown keys.
- Without `--doc`, it starts from empty `values` and `changed`, so the written doc replaces `config/current` with only this key. Pass `--doc` (the doc as read) to keep the others.
- When the value equals the `CORE` default, the key is removed from `values` and `changed[key]` is still written with this `by` and `at`, as the page does.
- `look.theme` is the exception (`page_decides`): Python cannot know which themes a page has installed or which one it was built with, so any theme name (lower case, digits, dashes) is accepted and the value is always written, `default` included. A name the page does not have leaves it on its own default.
- `by` defaults to `agent`. The doc is written with `exists=True`: without `--pins` carrying `config/current` the output has `needs_pin`, meaning read its version and pass `--pins P.json` (`{"config/current": <version>}`), so the write is version-pinned.
- The change record is skipped when `log.data-changes` is false in `--doc`.

`adp.py config DIR [--doc C.json]` prints `{defaults, values, locked, locked_parts, links}`: the `CORE` defaults, the merged values, whether `edit.locked` is true, `parts.locked`, and every `links.*` value. `DIR` is optional: it is accepted and not read.

## 5. The settings pattern

`plugins/artifacts-done-properly/skills/adp/catalog/kit/patterns/settings.js` is `Kit.settings.mount(root, {config, user, groups, labels, onChange, download, timeZone})`, returning `{update, destroy}`. `config` defaults to `ADP.config` and may be any object with `all`, `get`, `set`, `reset` and `on`; `user` defaults to `ADP.user`.

It draws, from `config.all()`:

- A summary: number of settings and groups, how many differ from defaults, and whether editing is open or paused (and by whom, from `config.doc.changed['edit.locked']`).
- One panel per group in registry order (or the order and filter of `groups`). Heading labels come from `GROUPS`: edit "Editing", parts "Parts", comments "Comments", panel "Panels", playground "Playground", look "Look", links "Links", log "Logging", board "Board"; any other group is shown with its name capitalised, unless `labels` overrides. "board" is only a label: no core switch belongs to it.
- One row per switch with the label, the key, the help, a meta line (the layer from `level`: "Enforced by the page" or "Enforced by the database rule"; "Changed by"; the default when different), and the control for the type: bool a switch, enum radio segments (at most four options, each at most 14 characters) or a select, text and url an input, list a textarea with one item per line, datetime a `datetime-local` input.
- Each row saves at once through `config.set` and shows "Saved" with an Undo for ten seconds, or the rejection message. Undo calls `set` with the previous value.
- Footer: "Export config.json" (the values that differ from defaults) and "Reset all to defaults" (a second press within five seconds confirms; it calls `reset()`).

It never touches the database itself. Rows redraw on `config.on('*')`. Without `user.canEdit` every control is disabled. With no defined settings it shows "No settings are defined yet."

### How a kit or page registers its own switch

Call `ADP.config.define(group, {...})` before or after the runtime is ready; the settings page lists it under its group on the next draw. The starter template shows the pattern in `plugins/artifacts-done-properly/skills/adp/templates/starter/parts/app.js.txt`: it defines `page.show-about`, follows it with `ADP.config.on`, and applies the value again when the home view renders.

### The gear and the settings view

In the starter and assistant templates the header has `<button id="gear" hidden>`. `app.js.txt` toggles between the Settings view and Home on click, and after `ADP.config.ready` un-hides the gear only when `ADP.user.canEdit` is true. The Settings view is `<section class="view settings-view" data-part="settings">`; `.settings-view` is a grid in `plugins/artifacts-done-properly/skills/adp/templates/starter/styles/page.css.txt`. On entering the view it mounts `Kit.settings` into `[data-part="settings.switches"]`, `Kit.inbox` into `settings.inbox` (when `ADP.db` exists) and `Kit.namespaces` into `settings.namespaces`, once `ADP.config.ready` has resolved; leaving the view calls `destroy`. If `Kit.settings` or `Kit.namespaces` is missing, the switches area shows "The settings kit is not installed."

namespaces.js "Locked parts" lists each `parts.locked` prefix with the part ids it covers (whole-segment match, as in section 3) and the count of parts left open. It reads `parts.locked` from `ADP.config` and writes nothing.

## 6. Holds

`adp.py hold DIR ID ... --by NAME [--hours H] [--pins P.json] [--config C.json] [--unlock PREFIX ...]` writes an ArtifactData batch (to `--out`, default `DIR.adp/`) with:

- for each ID, an `update` of `parts/<ID>` with `{holder: NAME, hold_until: <UTC time>}`. `--hours` defaults to 2 and is capped at 2 (`min(hrs, 2)`), so a larger value is accepted and writes two hours. The JSON output carries `hold_until`, the time written.
- a `set` (or `update`, when `agents/<id>` is in `--pins`) of `agents/<agent_id(NAME)>` with `{last_seen, holds: [IDs]}`.

`--config` runs `guard` with the IDs: `edit.locked` and `parts.locked` apply to a hold; `edit.require-hold` does not (no `deepest` is passed).

`record` clears the holds of the parts it writes (`holder: ''`, `hold_until: ''`) and sets the agent's `holds` to `[]`. `edit.require-hold` consumes holds as described in section 3: `record --config C.json --holds H.json` looks the holder up in H.json, which the caller builds from the `parts/<id>` docs it read.

## 7. Discrepancies between comments, help text and code

These are observed differences; the code is what this document follows.

1. `edit.require-hold` help in adp.js says "A publish touching a part nobody holds is refused". The code refuses only in `record`, only changed parts that existed before, only the deepest changed ones, and needs `--holds`; the expiry in `hold_until` is not checked.
2. `edit.locked` help says it "Freezes every control marked data-adp-edit". The code does this with CSS pointer events only; scripts can still call `ADP.config.set`.
3. `adp.py config set` and `ADP.config.set` differ on unknown keys (rejected versus accepted with `unknown: true`, on purpose). Url, text length and datetime real-ness agree for ISO values; `Date.parse` also accepts non-ISO text and overflowing days such as `2026-02-30` (read as 2 March) that `real_date` refuses.
4. `comments.enabled`, `links.board` and `links.repo` are registered with no reader in the adp skill (`skills/adp/`); `look.density` only sets an attribute nothing reads, and so does `look.theme` on a page without a theme switch.
5. settings.js labels the layer from `level`; every core switch has `level: 'page'`, so `parts.locked` and `edit.require-hold` also show "Enforced by the page" although adp.py also enforces them.
6. `adp.py hold --hours H` accepts larger values but writes at most 2 hours; the usage line says so and the output states `hold_until`.
