# Vectors: adp-protocol

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-rebuild](../adp-rebuild/SKILL.md) reads them; they are run against the tools assembled from the fragments.

## Contract: `hold` and `record`

```json fixture
{"fixture": "rec", "files": {
 "old.json": "{\"schema\":\"adp/2\",\"page_hash\":\"7f4556515dd9\",\"parts\":{\"_rest:index.html\":\"ee2d7cd8fa75\",\"_rest:parts/app.js\":\"e3b0c44298fc\",\"_rest:styles/page.css\":\"e3b0c44298fc\",\"home\":\"081b78b8f894\",\"home.lead\":\"c6a82a517ff8\",\"page.header\":\"0d957e9aee8d\",\"page.script.app\":\"35c146f76e12\",\"page.style\":\"997faceca260\"},\"files\":{\"index.html\":\"bd002c3d502b\",\"parts/app.js\":\"574c60bebc47\",\"styles/page.css\":\"56ee869c6a7b\"},\"parents\":{\"_rest:index.html\":\"\",\"_rest:parts/app.js\":\"\",\"_rest:styles/page.css\":\"\",\"home\":\"\",\"home.lead\":\"home\",\"page.header\":\"\",\"page.script.app\":\"\",\"page.style\":\"\"},\"elements\":{\"_rest:index.html\":2,\"_rest:parts/app.js\":0,\"_rest:styles/page.css\":0,\"home\":1,\"home.lead\":1,\"page.header\":1,\"page.script.app\":0,\"page.style\":0},\"part_file\":{\"_rest:index.html\":\"index.html\",\"_rest:parts/app.js\":\"parts/app.js\",\"_rest:styles/page.css\":\"styles/page.css\",\"home\":\"index.html\",\"home.lead\":\"index.html\",\"page.header\":\"index.html\",\"page.script.app\":\"parts/app.js\",\"page.style\":\"styles/page.css\"},\"version\":\"7\"}",
 "pins.json": "{\"manifest/current\": 7, \"parts/home\": 2, \"parts/home.lead\": 3, \"agents/agent-a\": 1}",
 "locked.json": "{\"schema\": \"adp-config/1\", \"values\": {\"edit.locked\": true}, \"changed\": {\"edit.locked\": {\"by\": \"owner\", \"at\": \"2026-11-19T09:00:00Z\"}}}",
 "core-locked.json": "{\"schema\": \"adp-config/1\", \"values\": {\"parts.locked\": [\"home\"]}, \"changed\": {}}"}}
```

```json vector
{
 "vector": "hold-pinned",
 "run": [
  "adp.py",
  "hold",
  "{page-a}",
  "home.lead",
  "--by",
  "agent-a",
  "--hours",
  "1",
  "--pins",
  "{rec}/pins.json",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "hold_until": "<time>",
  "batches": [
   [
    {
     "op": "update",
     "collection": "parts",
     "doc_id": "home.lead",
     "file_path": "<tmp>/out/parts__home.lead.json",
     "if_version": 3
    },
    {
     "op": "update",
     "collection": "agents",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/agents__agent-a.json",
     "if_version": 1
    }
   ]
  ],
  "docs_dir": "<tmp>/out"
 },
 "files_out": {
  "{out}/parts__home.lead.json": {
   "holder": "agent-a",
   "hold_until": "<time>"
  },
  "{out}/agents__agent-a.json": {
   "last_seen": "<time>",
   "holds": [
    "home.lead"
   ]
  }
 }
}
```

```json vector
{
 "vector": "hold-unpinned",
 "run": [
  "adp.py",
  "hold",
  "{page-a}",
  "home.lead",
  "--by",
  "agent-a",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "hold_until": "<time>",
  "batches": [
   [
    {
     "op": "update",
     "collection": "parts",
     "doc_id": "home.lead",
     "file_path": "<tmp>/out/parts__home.lead.json"
    },
    {
     "op": "set",
     "collection": "agents",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/agents__agent-a.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out",
  "needs_pin": [
   "parts/home.lead"
  ]
 }
}
```

```json vector
{
 "vector": "hold-refused-locked",
 "run": [
  "adp.py",
  "hold",
  "{page-a}",
  "home.lead",
  "--by",
  "agent-a",
  "--config",
  "{rec}/locked.json",
  "--out",
  "{out}"
 ],
 "exit": 2,
 "stdout": {
  "error": "locked",
  "by": "owner",
  "at": "<time>",
  "reason": ""
 }
}
```

```json vector
{
 "vector": "hold-refused-locked-part",
 "run": [
  "adp.py",
  "hold",
  "{page-a}",
  "home.lead",
  "--by",
  "agent-a",
  "--config",
  "{rec}/core-locked.json",
  "--out",
  "{out}"
 ],
 "exit": 2,
 "stdout": {
  "error": "locked parts",
  "parts": [
   "home.lead"
  ]
 }
}
```

```json vector
{
 "vector": "record-a-wording-change",
 "run": [
  "adp.py",
  "record",
  "{rec}/old.json",
  "{page-a2}",
  "--seq",
  "8",
  "--by",
  "agent-a",
  "--summary",
  "Lead: wording",
  "--version",
  "8",
  "--threads",
  "t-42",
  "--pins",
  "{rec}/pins.json",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "batches": [
   [
    {
     "op": "update",
     "collection": "parts",
     "doc_id": "home",
     "file_path": "<tmp>/out/parts__home.json",
     "if_version": 2
    },
    {
     "op": "update",
     "collection": "parts",
     "doc_id": "home.lead",
     "file_path": "<tmp>/out/parts__home.lead.json",
     "if_version": 3
    },
    {
     "op": "set",
     "collection": "changes",
     "doc_id": "000008",
     "file_path": "<tmp>/out/changes__000008.json"
    },
    {
     "op": "update",
     "collection": "threads",
     "doc_id": "t-42",
     "file_path": "<tmp>/out/threads__t-42.json"
    },
    {
     "op": "update",
     "collection": "agents",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/agents__agent-a.json",
     "if_version": 1
    },
    {
     "op": "set",
     "collection": "manifest",
     "doc_id": "current",
     "file_path": "<tmp>/out/manifest__current.json",
     "if_version": 7
    }
   ]
  ],
  "docs_dir": "<tmp>/out",
  "needs_pin": [
   "threads/t-42"
  ]
 },
 "files_out": {
  "{out}/parts__home.lead.json": {
   "hash": "8e7c2ba46ff4",
   "version": "8",
   "at": "<time>",
   "by": "agent-a",
   "summary": "Lead: wording",
   "holder": "",
   "hold_until": "",
   "file": "index.html"
  },
  "{out}/parts__home.json": {
   "hash": "f98716c9ddf4",
   "version": "8",
   "at": "<time>",
   "by": "agent-a",
   "summary": "Lead: wording",
   "file": "index.html"
  },
  "{out}/changes__000008.json": {
   "version": "8",
   "at": "<time>",
   "by": "agent-a",
   "summary": "Lead: wording",
   "parts": [
    {
     "id": "home",
     "from": "081b78b8f894",
     "to": "f98716c9ddf4"
    },
    {
     "id": "home.lead",
     "from": "c6a82a517ff8",
     "to": "8e7c2ba46ff4"
    }
   ],
   "threads": [
    "t-42"
   ]
  },
  "{out}/agents__agent-a.json": {
   "last_seen": "<time>",
   "holds": []
  },
  "{out}/manifest__current.json": {
   "schema": "adp/2",
   "version": "8",
   "page_hash": "c125279381ff",
   "parts": {
    "_rest:index.html": "ee2d7cd8fa75",
    "_rest:parts/app.js": "e3b0c44298fc",
    "_rest:styles/page.css": "e3b0c44298fc",
    "home": "f98716c9ddf4",
    "home.lead": "8e7c2ba46ff4",
    "page.header": "0d957e9aee8d",
    "page.script.app": "35c146f76e12",
    "page.style": "997faceca260"
   },
   "elements": {
    "_rest:index.html": 2,
    "_rest:parts/app.js": 0,
    "_rest:styles/page.css": 0,
    "home": 2,
    "home.lead": 1,
    "page.header": 1,
    "page.script.app": 0,
    "page.style": 0
   },
   "files": {
    "index.html": "a56efc30baaf",
    "parts/app.js": "574c60bebc47",
    "styles/page.css": "56ee869c6a7b"
   },
   "part_file": {
    "_rest:index.html": "index.html",
    "_rest:parts/app.js": "parts/app.js",
    "_rest:styles/page.css": "styles/page.css",
    "home": "index.html",
    "home.lead": "index.html",
    "page.header": "index.html",
    "page.script.app": "parts/app.js",
    "page.style": "styles/page.css"
   },
   "content": {},
   "at": "<time>",
   "by": "agent-a"
  },
  "{out}/threads__t-42.json": {
   "status": "done",
   "holder": "",
   "done_in": "8"
  }
 }
}
```

## Contract: switches (`config`) and requests (`requests`)

```json fixture
{"fixture": "asks", "files": {
 "dump.json": "[{\"id\": \"r-2\", \"version\": 1, \"data\": {\"lane\": \"ask\", \"text\": \"Why two badges?\", \"scope\": {\"page\": true}, \"by\": \"viewer-2\", \"at\": \"2026-11-19T11:00:00Z\"}}, {\"id\": \"r-1\", \"version\": 3, \"data\": {\"lane\": \"edit\", \"text\": \"Make the lead warmer\", \"quote\": \"Hi\", \"scope\": {\"part\": \"home.lead\"}, \"by\": \"viewer-1\", \"at\": \"2026-11-19T10:00:00Z\"}}, {\"id\": \"r-0\", \"version\": 7, \"data\": {\"lane\": \"edit\", \"text\": \"Fix the title\", \"status\": \"done\", \"by\": \"viewer-1\", \"at\": \"2026-11-18T10:00:00Z\"}}]",
 "answer.md": "The lead now says Hello.\n",
 "config.json": "{\"schema\": \"adp-config/1\", \"values\": {\"edit.locked\": false, \"look.theme\": \"default\"}, \"changed\": {}}",
 "pins.json": "{\"config/current\": 4}"}}
```

```json vector
{
 "vector": "config-defaults",
 "run": [
  "adp.py",
  "config"
 ],
 "exit": 0,
 "stdout": {
  "defaults": {
   "edit.locked": false,
   "edit.until": "",
   "edit.reason": "",
   "edit.require-hold": false,
   "parts.locked": [],
   "comments.enabled": true,
   "panel.changes": "everyone",
   "panel.checks": "editors",
   "playground.enabled": true,
   "look.theme": "default",
   "look.mode": "auto",
   "look.density": "comfortable",
   "links.catalog": "",
   "links.board": "",
   "links.repo": "",
   "log.data-changes": true
  },
  "values": {
   "edit.locked": false,
   "edit.until": "",
   "edit.reason": "",
   "edit.require-hold": false,
   "parts.locked": [],
   "comments.enabled": true,
   "panel.changes": "everyone",
   "panel.checks": "editors",
   "playground.enabled": true,
   "look.theme": "default",
   "look.mode": "auto",
   "look.density": "comfortable",
   "links.catalog": "",
   "links.board": "",
   "links.repo": "",
   "log.data-changes": true
  },
  "locked": false,
  "locked_parts": [],
  "links": {
   "catalog": "",
   "board": "",
   "repo": ""
  }
 }
}
```

```json vector
{
 "vector": "config-set-pinned",
 "run": [
  "adp.py",
  "config",
  "set",
  "look.theme",
  "paper",
  "--doc",
  "{asks}/config.json",
  "--by",
  "agent-a",
  "--pins",
  "{asks}/pins.json",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "key": "look.theme",
  "value": "paper",
  "batches": [
   [
    {
     "op": "set",
     "collection": "config",
     "doc_id": "current",
     "file_path": "<tmp>/out/config__current.json",
     "if_version": 4
    },
    {
     "op": "set",
     "collection": "changes",
     "doc_id": "d-<ms>",
     "file_path": "<tmp>/out/changes__d-<ms>.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out"
 },
 "files_out": {
  "{out}/config__current.json": {
   "schema": "adp-config/1",
   "at": "<time>",
   "by": "agent-a",
   "values": {
    "edit.locked": false,
    "look.theme": "paper"
   },
   "changed": {
    "look.theme": {
     "by": "agent-a",
     "at": "<time>"
    }
   }
  },
  "{out}/changes__d-*.json": {
   "version": "",
   "at": "<time>",
   "by": "agent-a",
   "summary": "Set look.theme = \"paper\"",
   "parts": [],
   "threads": [],
   "data": [
    {
     "doc": "config/current"
    }
   ]
  }
 }
}
```

```json vector
{
 "vector": "config-set-unknown-key-unpinned",
 "run": [
  "adp.py",
  "config",
  "set",
  "nope.key",
  "1",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "key": "nope.key",
  "value": 1,
  "unknown": true,
  "batches": [
   [
    {
     "op": "set",
     "collection": "config",
     "doc_id": "current",
     "file_path": "<tmp>/out/config__current.json"
    },
    {
     "op": "set",
     "collection": "changes",
     "doc_id": "d-<ms>",
     "file_path": "<tmp>/out/changes__d-<ms>.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out",
  "needs_pin": [
   "config/current"
  ]
 }
}
```

```json vector
{
 "vector": "requests-open",
 "run": [
  "adp.py",
  "requests",
  "{asks}/dump.json"
 ],
 "exit": 0,
 "stdout": {
  "open": [
   {
    "id": "r-1",
    "lane": "edit",
    "state": "queue",
    "scope": {
     "part": "home.lead"
    },
    "project": "",
    "text": "Make the lead warmer",
    "quote": "Hi",
    "by": "viewer-1",
    "at": "<time>",
    "last_progress": "",
    "reopened": false,
    "resolved": false,
    "lease": null
   },
   {
    "id": "r-2",
    "lane": "ask",
    "state": "queue",
    "scope": {
     "page": true
    },
    "project": "",
    "text": "Why two badges?",
    "quote": "",
    "by": "viewer-2",
    "at": "<time>",
    "last_progress": "",
    "reopened": false,
    "resolved": false,
    "lease": null
   }
  ],
  "count": 2,
  "trailer": "· adp request {<rid>} · lane <lane> · scope part:<id>|page"
 }
}
```

```json vector
{
 "vector": "requests-ack",
 "run": [
  "adp.py",
  "requests",
  "{asks}/dump.json",
  "--ack",
  "r-1",
  "--by",
  "agent-a",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "request": "r-1",
  "state": "ack",
  "batches": [
   [
    {
     "op": "update",
     "collection": "requests",
     "doc_id": "r-1",
     "file_path": "<tmp>/out/requests__r-1.json",
     "if_version": 3
    },
    {
     "op": "set",
     "collection": "presence",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/presence__agent-a.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out"
 },
 "files_out": {
  "{out}/requests__r-1.json": {
   "state": "ack",
   "ackBy": "agent-a",
   "ackAt": "<time>"
  },
  "{out}/presence__agent-a.json": {
   "at": "<time>",
   "doing": "r-1 (edit)",
   "session": "agent-a"
  }
 }
}
```

```json vector
{
 "vector": "requests-progress",
 "run": [
  "adp.py",
  "requests",
  "{asks}/dump.json",
  "--progress",
  "r-1",
  "--text",
  "Drafting",
  "--by",
  "agent-a",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "request": "r-1",
  "state": "working",
  "batches": [
   [
    {
     "op": "update",
     "collection": "requests",
     "doc_id": "r-1",
     "file_path": "<tmp>/out/requests__r-1.json",
     "if_version": 3
    },
    {
     "op": "set",
     "collection": "presence",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/presence__agent-a.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out"
 },
 "files_out": {
  "{out}/requests__r-1.json": {
   "state": "working",
   "progress": [
    {
     "at": "<time>",
     "text": "Drafting"
    }
   ]
  }
 }
}
```

```json vector
{
 "vector": "requests-done",
 "run": [
  "adp.py",
  "requests",
  "{asks}/dump.json",
  "--done",
  "r-1",
  "--response",
  "{asks}/answer.md",
  "--changed",
  "home.lead",
  "--version",
  "8",
  "--by",
  "agent-a",
  "--out",
  "{out}"
 ],
 "exit": 0,
 "stdout": {
  "request": "r-1",
  "state": "done",
  "batches": [
   [
    {
     "op": "update",
     "collection": "requests",
     "doc_id": "r-1",
     "file_path": "<tmp>/out/requests__r-1.json",
     "if_version": 3
    },
    {
     "op": "set",
     "collection": "presence",
     "doc_id": "agent-a",
     "file_path": "<tmp>/out/presence__agent-a.json"
    }
   ]
  ],
  "docs_dir": "<tmp>/out"
 },
 "files_out": {
  "{out}/requests__r-1.json": {
   "status": "done",
   "doneAt": "<time>",
   "changed": [
    "home.lead"
   ],
   "version": "8",
   "response": "The lead now says Hello."
  },
  "{out}/presence__agent-a.json": {
   "at": "<time>",
   "doing": "",
   "session": "agent-a"
  }
 }
}
```

```json vector
{
 "vector": "requests-unknown-id",
 "run": [
  "adp.py",
  "requests",
  "{asks}/dump.json",
  "--ack",
  "r-9",
  "--by",
  "agent-a",
  "--out",
  "{out}"
 ],
 "exit": 1,
 "stderr_text": [
  "r-9: not in <tmp>/asks/dump.json"
 ]
}
```

## Contract: agent work on a request (`work`)

```json fixture
{
 "fixture": "lease",
 "files": {
  "open.json": "[\n {\n  \"call\": {\n   \"tool\": \"ArtifactData\",\n   \"args\": {\n    \"action\": \"list\",\n    \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\",\n    \"collection\": \"requests\",\n    \"query\": {\n     \"limit\": 1000\n    }\n   },\n   \"collection\": \"requests\"\n  },\n  \"result\": \"{\\\"id\\\": \\\"r-1\\\", \\\"data\\\": {\\\"lane\\\": \\\"edit\\\", \\\"text\\\": \\\"Make the lead warmer\\\", \\\"quote\\\": \\\"Hi\\\", \\\"scope\\\": {\\\"part\\\": \\\"home.lead\\\"}, \\\"by\\\": \\\"viewer-1\\\", \\\"at\\\": \\\"2026-11-19T10:00:00Z\\\"}, \\\"version\\\": 3}\"\n }\n]\n",
  "held.json": "[\n {\n  \"call\": {\n   \"tool\": \"ArtifactData\",\n   \"args\": {\n    \"action\": \"list\",\n    \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\",\n    \"collection\": \"requests\",\n    \"query\": {\n     \"limit\": 1000\n    }\n   },\n   \"collection\": \"requests\"\n  },\n  \"result\": \"{\\\"id\\\": \\\"r-1\\\", \\\"data\\\": {\\\"lane\\\": \\\"edit\\\", \\\"text\\\": \\\"Make the lead warmer\\\", \\\"quote\\\": \\\"Hi\\\", \\\"scope\\\": {\\\"part\\\": \\\"home.lead\\\"}, \\\"by\\\": \\\"viewer-1\\\", \\\"at\\\": \\\"2026-11-19T10:00:00Z\\\", \\\"state\\\": \\\"working\\\", \\\"execution\\\": {\\\"schema\\\": \\\"adp-work/1\\\", \\\"origin\\\": {\\\"host\\\": \\\"claude\\\", \\\"artifact\\\": \\\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\\\"}, \\\"actor\\\": \\\"agent-a\\\", \\\"token\\\": \\\"tok-1\\\", \\\"attempt\\\": 1, \\\"inputHash\\\": \\\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\\\", \\\"claimedAt\\\": \\\"2026-11-20T10:00:00Z\\\", \\\"state\\\": \\\"working\\\", \\\"leaseUntil\\\": \\\"2099-01-01T00:00:00Z\\\", \\\"updatedAt\\\": \\\"2026-11-20T10:00:00Z\\\"}}, \\\"version\\\": 4}\"\n }\n]\n",
  "expired.json": "[\n {\n  \"call\": {\n   \"tool\": \"ArtifactData\",\n   \"args\": {\n    \"action\": \"list\",\n    \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\",\n    \"collection\": \"requests\",\n    \"query\": {\n     \"limit\": 1000\n    }\n   },\n   \"collection\": \"requests\"\n  },\n  \"result\": \"{\\\"id\\\": \\\"r-1\\\", \\\"data\\\": {\\\"lane\\\": \\\"edit\\\", \\\"text\\\": \\\"Make the lead warmer\\\", \\\"quote\\\": \\\"Hi\\\", \\\"scope\\\": {\\\"part\\\": \\\"home.lead\\\"}, \\\"by\\\": \\\"viewer-1\\\", \\\"at\\\": \\\"2026-11-19T10:00:00Z\\\", \\\"state\\\": \\\"working\\\", \\\"execution\\\": {\\\"schema\\\": \\\"adp-work/1\\\", \\\"origin\\\": {\\\"host\\\": \\\"claude\\\", \\\"artifact\\\": \\\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\\\"}, \\\"actor\\\": \\\"agent-a\\\", \\\"token\\\": \\\"tok-1\\\", \\\"attempt\\\": 1, \\\"inputHash\\\": \\\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\\\", \\\"claimedAt\\\": \\\"2026-11-20T10:00:00Z\\\", \\\"state\\\": \\\"working\\\", \\\"leaseUntil\\\": \\\"2026-01-01T00:00:00Z\\\", \\\"updatedAt\\\": \\\"2026-11-20T10:00:00Z\\\"}}, \\\"version\\\": 4}\"\n }\n]\n",
  "other-artifact.json": "[\n {\n  \"call\": {\n   \"tool\": \"ArtifactData\",\n   \"args\": {\n    \"action\": \"list\",\n    \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-0000000000ff\",\n    \"collection\": \"requests\",\n    \"query\": {\n     \"limit\": 1000\n    }\n   },\n   \"collection\": \"requests\"\n  },\n  \"result\": \"{\\\"id\\\": \\\"r-1\\\", \\\"data\\\": {\\\"lane\\\": \\\"edit\\\", \\\"text\\\": \\\"Make the lead warmer\\\", \\\"quote\\\": \\\"Hi\\\", \\\"scope\\\": {\\\"part\\\": \\\"home.lead\\\"}, \\\"by\\\": \\\"viewer-1\\\", \\\"at\\\": \\\"2026-11-19T10:00:00Z\\\"}, \\\"version\\\": 3}\"\n }\n]\n",
  "receipt.json": "{\n \"checks\": [\n  {\n   \"name\": \"lead reads warmer\",\n   \"passed\": true,\n   \"evidence\": \"adp.py diff-pages: home.lead changed, nothing else\"\n  }\n ]\n}\n",
  "receipt-failing.json": "{\"checks\": [{\"name\": \"lead reads warmer\", \"passed\": false, \"evidence\": \"not checked\"}]}\n"
 }
}
```

```json vector
{
 "vector": "work-asks-for-its-read",
 "run": [
  "adp.py",
  "work",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1"
 ],
 "exit": 2,
 "stdout": {
  "reads": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "collection": "requests",
     "query": {
      "limit": 1000
     }
    },
    "collection": "requests"
   }
  ]
 }
}
```

```json vector
{
 "vector": "work-inspect",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "path": "requests/r-1",
  "revision": 4,
  "status": null,
  "resolved": false,
  "execution": {
   "schema": "adp-work/1",
   "origin": {
    "host": "claude",
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   },
   "actor": "agent-a",
   "token": "tok-1",
   "attempt": 1,
   "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
   "claimedAt": "<time>",
   "state": "working",
   "leaseUntil": "<time>",
   "updatedAt": "<time>"
  },
  "foreign": false
 }
}
```

```json vector
{
 "vector": "work-claim",
 "run": [
  "adp.py",
  "work",
  "{lease}/open.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "claim",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp-work-plan/1",
  "path": "requests/r-1",
  "action": "claim",
  "leaseToken": "<uuid>",
  "calls": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "batch",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "writes": [
      {
       "op": "set",
       "collection": "requests",
       "doc_id": "r-1",
       "data": {
        "lane": "edit",
        "text": "Make the lead warmer",
        "quote": "Hi",
        "scope": {
         "part": "home.lead"
        },
        "by": "viewer-1",
        "at": "<time>",
        "ackBy": "agent-a",
        "ackAt": "<time>",
        "execution": {
         "schema": "adp-work/1",
         "origin": {
          "host": "claude",
          "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
         },
         "actor": "agent-a",
         "token": "<uuid>",
         "attempt": 1,
         "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
         "claimedAt": "<time>",
         "state": "working",
         "leaseUntil": "<time>",
         "updatedAt": "<time>"
        },
        "state": "working",
        "delivery": "acknowledged"
       },
       "if_version": 3
      }
     ]
    },
    "keys": [
     "requests/r-1"
    ],
    "atomic": true
   }
  ],
  "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
  "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
 }
}
```

```json vector
{
 "vector": "work-claim-while-a-lease-is-live",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "claim",
  "--by",
  "agent-b",
  "--raw"
 ],
 "exit": 1,
 "stderr_text": [
  "Work has an active lease; inspect it instead of starting duplicate work"
 ]
}
```

```json vector
{
 "vector": "work-claim-after-the-lease-expired",
 "run": [
  "adp.py",
  "work",
  "{lease}/expired.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "claim",
  "--by",
  "agent-b",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp-work-plan/1",
  "path": "requests/r-1",
  "action": "claim",
  "leaseToken": "<uuid>",
  "calls": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "batch",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "writes": [
      {
       "op": "set",
       "collection": "requests",
       "doc_id": "r-1",
       "data": {
        "lane": "edit",
        "text": "Make the lead warmer",
        "quote": "Hi",
        "scope": {
         "part": "home.lead"
        },
        "by": "viewer-1",
        "at": "<time>",
        "state": "working",
        "execution": {
         "schema": "adp-work/1",
         "origin": {
          "host": "claude",
          "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
         },
         "actor": "agent-b",
         "token": "<uuid>",
         "attempt": 2,
         "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
         "claimedAt": "<time>",
         "state": "working",
         "leaseUntil": "<time>",
         "updatedAt": "<time>"
        },
        "ackBy": "agent-b",
        "ackAt": "<time>",
        "delivery": "acknowledged"
       },
       "if_version": 4
      }
     ]
    },
    "keys": [
     "requests/r-1"
    ],
    "atomic": true
   }
  ],
  "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
  "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
 }
}
```

```json vector
{
 "vector": "work-progress",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "progress",
  "--token",
  "tok-1",
  "--text",
  "Drafting",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp-work-plan/1",
  "path": "requests/r-1",
  "action": "progress",
  "leaseToken": "tok-1",
  "calls": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "batch",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "writes": [
      {
       "op": "set",
       "collection": "requests",
       "doc_id": "r-1",
       "data": {
        "lane": "edit",
        "text": "Make the lead warmer",
        "quote": "Hi",
        "scope": {
         "part": "home.lead"
        },
        "by": "viewer-1",
        "at": "<time>",
        "state": "working",
        "execution": {
         "schema": "adp-work/1",
         "origin": {
          "host": "claude",
          "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
         },
         "actor": "agent-a",
         "token": "tok-1",
         "attempt": 1,
         "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
         "claimedAt": "<time>",
         "state": "working",
         "leaseUntil": "<time>",
         "updatedAt": "<time>"
        },
        "progress": [
         {
          "at": "<time>",
          "text": "Drafting",
          "by": "agent-a"
         }
        ],
        "delivery": "acknowledged"
       },
       "if_version": 4
      }
     ]
    },
    "keys": [
     "requests/r-1"
    ],
    "atomic": true
   }
  ],
  "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
  "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
 }
}
```

```json vector
{
 "vector": "work-progress-with-the-wrong-token",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "progress",
  "--token",
  "tok-2",
  "--text",
  "Drafting",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 1,
 "stderr_text": [
  "Lease expired, changed input or wrong claimant; reread and reclaim before work"
 ]
}
```

```json vector
{
 "vector": "work-block",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "block",
  "--token",
  "tok-1",
  "--text",
  "Which tone: warm or formal?",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp-work-plan/1",
  "path": "requests/r-1",
  "action": "block",
  "leaseToken": "tok-1",
  "calls": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "batch",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "writes": [
      {
       "op": "set",
       "collection": "requests",
       "doc_id": "r-1",
       "data": {
        "lane": "edit",
        "text": "Make the lead warmer",
        "quote": "Hi",
        "scope": {
         "part": "home.lead"
        },
        "by": "viewer-1",
        "at": "<time>",
        "state": "ack",
        "execution": {
         "schema": "adp-work/1",
         "origin": {
          "host": "claude",
          "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
         },
         "actor": "agent-a",
         "token": "tok-1",
         "attempt": 1,
         "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
         "claimedAt": "<time>",
         "state": "blocked",
         "leaseUntil": "<time>",
         "updatedAt": "<time>",
         "reason": "Which tone: warm or formal?"
        },
        "progress": [
         {
          "at": "<time>",
          "text": "Which tone: warm or formal?",
          "by": "agent-a"
         }
        ],
        "delivery": "acknowledged"
       },
       "if_version": 4
      }
     ]
    },
    "keys": [
     "requests/r-1"
    ],
    "atomic": true
   }
  ],
  "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
  "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
 }
}
```

```json vector
{
 "vector": "work-complete",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "complete",
  "--token",
  "tok-1",
  "--text",
  "The lead now greets.",
  "--receipt",
  "{lease}/receipt.json",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp-work-plan/1",
  "path": "requests/r-1",
  "action": "complete",
  "leaseToken": "tok-1",
  "calls": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "batch",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "writes": [
      {
       "op": "set",
       "collection": "requests",
       "doc_id": "r-1",
       "data": {
        "lane": "edit",
        "text": "Make the lead warmer",
        "quote": "Hi",
        "scope": {
         "part": "home.lead"
        },
        "by": "viewer-1",
        "at": "<time>",
        "state": "done",
        "execution": {
         "schema": "adp-work/1",
         "origin": {
          "host": "claude",
          "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
         },
         "actor": "agent-a",
         "token": "tok-1",
         "attempt": 1,
         "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
         "claimedAt": "<time>",
         "state": "done",
         "leaseUntil": "<time>",
         "updatedAt": "<time>",
         "receipt": {
          "checks": [
           {
            "name": "lead reads warmer",
            "passed": true,
            "evidence": "adp.py diff-pages: home.lead changed, nothing else"
           }
          ]
         },
         "result": "The lead now greets."
        },
        "progress": [
         {
          "at": "<time>",
          "text": "The lead now greets.",
          "by": "agent-a"
         }
        ],
        "response": "The lead now greets.",
        "status": "done",
        "doneAt": "<time>",
        "delivery": "completed"
       },
       "if_version": 4
      }
     ]
    },
    "keys": [
     "requests/r-1"
    ],
    "atomic": true
   }
  ],
  "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
  "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
 }
}
```

```json vector
{
 "vector": "work-complete-with-a-failing-check",
 "run": [
  "adp.py",
  "work",
  "{lease}/held.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "complete",
  "--token",
  "tok-1",
  "--text",
  "x",
  "--receipt",
  "{lease}/receipt-failing.json",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 1,
 "stderr_text": [
  "Every completion check must pass and carry evidence"
 ]
}
```

```json vector
{
 "vector": "work-a-read-of-another-artifact",
 "run": [
  "adp.py",
  "work",
  "{lease}/other-artifact.json",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
  "--path",
  "requests/r-1",
  "--action",
  "claim",
  "--by",
  "agent-a",
  "--raw"
 ],
 "exit": 1,
 "stderr_text": [
  "Work read belongs to another artifact"
 ]
}
```

## Contract: the rest of `hold`, `record`, `config`, `requests` and `work`

```json fixture
{"fixture": "rec2", "base": "rec", "files": {
 "holds.json": "{\"home.lead\": \"agent-b\", \"page.header\": {\"holder\": \"agent-a\", \"hold_until\": \"2026-11-19T12:00:00Z\"}, \"home\": \"agent-a\"}",
 "holds-partial.json": "{\"home.lead\": \"agent-b\"}",
 "require-hold.json": "{\"schema\": \"adp-config/1\", \"values\": {\"edit.require-hold\": true}, \"changed\": {}}"}}
```

```json fixture
{"fixture": "page-a3", "base": "page-a", "files": {
 "index.html": "<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hello</p><!-- /part:home.lead --><!-- part:home.cta --><a data-part=\"home.cta\" data-comment-target>Go</a><!-- /part:home.cta --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"}}
```

```json vector
{
 "vector": "record-adds-removes-and-holds",
 "steps": [
  {
   "run": [
    "adp.py",
    "record",
    "{rec2}/old.json",
    "{page-a3}",
    "--seq",
    "8",
    "--by",
    "agent-a",
    "--summary",
    "Lead: wording, a call to action, no header",
    "--version",
    "8",
    "--config",
    "{rec2}/require-hold.json",
    "--holds",
    "{rec2}/holds.json",
    "--pins",
    "{rec2}/pins.json",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "stdout": {
    "batches": [
     [
      {
       "op": "update",
       "collection": "parts",
       "doc_id": "home",
       "file_path": "<tmp>/out/parts__home.json",
       "if_version": 2
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "home.cta",
       "file_path": "<tmp>/out/parts__home.cta.json"
      },
      {
       "op": "update",
       "collection": "parts",
       "doc_id": "home.lead",
       "file_path": "<tmp>/out/parts__home.lead.json",
       "if_version": 3
      },
      {
       "op": "delete",
       "collection": "parts",
       "doc_id": "page.header"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "000008",
       "file_path": "<tmp>/out/changes__000008.json"
      },
      {
       "op": "update",
       "collection": "agents",
       "doc_id": "agent-a",
       "file_path": "<tmp>/out/agents__agent-a.json",
       "if_version": 1
      },
      {
       "op": "set",
       "collection": "manifest",
       "doc_id": "current",
       "file_path": "<tmp>/out/manifest__current.json",
       "if_version": 7
      }
     ]
    ],
    "docs_dir": "<tmp>/out",
    "needs_pin": [
     "parts/page.header"
    ]
   },
   "files_out": {
    "{out}/parts__home.json": {
     "hash": "1963b028634f",
     "version": "8",
     "at": "<time>",
     "by": "agent-a",
     "summary": "Lead: wording, a call to action, no header",
     "file": "index.html",
     "holder": "",
     "hold_until": ""
    },
    "{out}/parts__home.lead.json": {
     "hash": "8e7c2ba46ff4",
     "version": "8",
     "at": "<time>",
     "by": "agent-a",
     "summary": "Lead: wording, a call to action, no header",
     "file": "index.html"
    },
    "{out}/parts__home.cta.json": {
     "hash": "d149068a4cf5",
     "version": "8",
     "at": "<time>",
     "by": "agent-a",
     "summary": "added: Lead: wording, a call to action, no header",
     "file": "index.html",
     "title": "home.cta",
     "parent": "home",
     "holder": "",
     "hold_until": ""
    }
   }
  },
  {
   "run": [
    "adp.py",
    "record",
    "{rec2}/old.json",
    "{page-a3}",
    "--seq",
    "8",
    "--by",
    "agent-a",
    "--summary",
    "S",
    "--config",
    "{rec2}/require-hold.json",
    "--out",
    "{out}"
   ],
   "exit": 2,
   "stdout": {
    "error": "unheld",
    "parts": [
     "home.lead",
     "page.header"
    ],
    "note": "edit.require-hold needs --holds"
   }
  },
  {
   "run": [
    "adp.py",
    "record",
    "{rec2}/old.json",
    "{page-a3}",
    "--seq",
    "8",
    "--by",
    "agent-a",
    "--summary",
    "S",
    "--config",
    "{rec2}/require-hold.json",
    "--holds",
    "{rec2}/holds-partial.json",
    "--out",
    "{out}"
   ],
   "exit": 2,
   "stdout": {
    "error": "unheld",
    "parts": [
     "page.header"
    ]
   }
  }
 ]
}
```

```json vector
{
 "vector": "config-set-validates",
 "steps": [
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "Bad.Key",
    "x",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "Bad.Key: keys are group.name, lower case, dashes allowed"
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "edit.locked",
    "yes",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "edit.locked: expected bool, got \"yes\""
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "look.mode",
    "neon",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "look.mode: expected one of auto/light/dark, got \"neon\""
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "links.repo",
    "http://x",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "links.repo: expected url, got \"http://x\""
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "edit.until",
    "2026-13-01",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "edit.until: expected datetime, got \"2026-13-01\""
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "parts.locked",
    "[1]",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "parts.locked: expected list, got [1]"
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "look.theme",
    "Dark Mode",
    "--out",
    "{out}"
   ],
   "exit": 1,
   "stderr_text": [
    "look.theme: expected name, got \"Dark Mode\""
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "edit.locked",
    "false",
    "--doc",
    "{asks}/config.json",
    "--by",
    "agent-a",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "files_out": {
    "{out}/config__current.json": {
     "schema": "adp-config/1",
     "at": "<time>",
     "by": "agent-a",
     "values": {
      "look.theme": "default"
     },
     "changed": {
      "edit.locked": {
       "by": "agent-a",
       "at": "<time>"
      }
     }
    }
   }
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "look.theme",
    "default",
    "--doc",
    "{asks}/config.json",
    "--by",
    "agent-a",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "files_out": {
    "{out}/config__current.json": {
     "schema": "adp-config/1",
     "at": "<time>",
     "by": "agent-a",
     "values": {
      "edit.locked": false,
      "look.theme": "default"
     },
     "changed": {
      "look.theme": {
       "by": "agent-a",
       "at": "<time>"
      }
     }
    }
   }
  }
 ]
}
```

```json vector
{
 "vector": "protocol-usage",
 "steps": [
  {
   "run": [
    "adp.py",
    "hold",
    "{page-a}"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py hold DIR ID ... --by NAME [--hours H (at most 2)] [--pins P.json] [--config C.json] [--unlock ID] [--out DIR]"
   ]
  },
  {
   "run": [
    "adp.py",
    "record",
    "{rec}/old.json",
    "{page-a}"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py record OLD.json DIR --seq N --by NAME --summary S [--version V] [--threads T,..] [--holds H.json] [--pins P.json] [--config C.json] [--unlock ID] [--out DIR]"
   ]
  },
  {
   "run": [
    "adp.py",
    "config",
    "set",
    "edit.locked"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py config [set SWITCH VALUE] [--doc C.json] [--by NAME] [--pins P.json] [--out DIR]"
   ]
  },
  {
   "run": [
    "adp.py",
    "requests"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py requests DUMP.json [--ack RID | --progress RID --text T | --done RID --response FILE [--changed a,b] [--version V] [--turns TURNS.json]] [--by NAME] [--pins P.json] [--out DIR]"
   ]
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks}/dump.json",
    "--ack"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py requests DUMP.json [--ack RID | --progress RID --text T | --done RID --response FILE [--changed a,b] [--version V] [--turns TURNS.json]] [--by NAME] [--pins P.json] [--out DIR]"
   ]
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks}/dump.json",
    "--ack",
    "r-1",
    "--progress",
    "r-1"
   ],
   "exit": 1,
   "stderr_text": [
    "one of --ack, --progress, --done"
   ]
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks}/dump.json",
    "--progress",
    "r-1"
   ],
   "exit": 1,
   "stderr_text": [
    "--progress needs --text T"
   ]
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks}/dump.json",
    "--done",
    "r-1"
   ],
   "exit": 1,
   "stderr_text": [
    "--done needs --response FILE (Markdown)"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "--host",
    "claude"
   ],
   "exit": 1,
   "stderr_text": [
    "work needs --host claude --artifact ID --path requests/ID|incoming/ID"
   ]
  }
 ]
}
```

```json fixture
{"fixture": "asks2", "base": "asks", "files": {
 "turns.json": "{\"0001\": {\"by\": \"claude\", \"at\": \"2026-11-19T12:00:00Z\", \"text\": \"first\"}, \"0002\": {\"by\": \"viewer-1\", \"at\": \"2026-11-19T12:05:00Z\", \"text\": \"and?\"}}",
 "bare.json": "{\"documents\": [{\"id\": \"r-5\", \"lane\": \"edit\", \"text\": \"Bare\", \"by\": \"viewer-1\", \"at\": \"2026-11-19T09:00:00Z\"}]}"}}
```

```json vector
{
 "vector": "requests-turns-and-dump-forms",
 "steps": [
  {
   "run": [
    "adp.py",
    "requests",
    "{asks2}/bare.json"
   ],
   "exit": 0,
   "stdout": {
    "open": [
     {
      "id": "r-5",
      "lane": "edit",
      "state": "queue",
      "scope": {},
      "project": "",
      "text": "Bare",
      "quote": "",
      "by": "viewer-1",
      "at": "<time>",
      "reopened": false,
      "last_progress": "",
      "resolved": false,
      "lease": null
     }
    ],
    "count": 1,
    "trailer": "· adp request {<rid>} · lane <lane> · scope part:<id>|page"
   }
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks2}/bare.json",
    "--ack",
    "r-5",
    "--by",
    "agent-a",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "stdout": {
    "request": "r-5",
    "state": "ack",
    "batches": [
     [
      {
       "op": "update",
       "collection": "requests",
       "doc_id": "r-5",
       "file_path": "<tmp>/out/requests__r-5.json"
      },
      {
       "op": "set",
       "collection": "presence",
       "doc_id": "agent-a",
       "file_path": "<tmp>/out/presence__agent-a.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/out",
    "needs_pin": [
     "requests/r-5"
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks2}/dump.json",
    "--done",
    "r-1",
    "--response",
    "{asks2}/answer.md",
    "--turns",
    "{asks2}/turns.json",
    "--by",
    "agent-a",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "files_out": {
    "{out}/requests~r-1~turns__0003.json": {
     "by": "claude",
     "at": "<time>",
     "text": "The lead now says Hello."
    },
    "{out}/requests__r-1.json": {
     "status": "done",
     "doneAt": "<time>",
     "changed": [],
     "version": ""
    }
   }
  }
 ]
}
```

The work vectors below read files in the form `[{collection, id, data, revision}]` (no `--raw`). In `n.json`: `r-1` holds a live lease (`tok-1`, `agent-a`), `r-2` an expired one, `r-3` is blocked, `r-4` is done, `r-5` holds a live lease but its text changed since, `r-6` a live lease with no origin, `r-7` a live lease made in another artifact, `r-8` a live lease on a request that already has a response, `r-9` is unclaimed. `inc.json` has three proposals: `p-1` without an approval, `p-2` approved, `p-3` approved and leased. The `rc-pub*` files are publication receipts.

```json fixture
{
 "fixture": "wk",
 "base": "lease",
 "files": {
  "n.json": "[{\"collection\":\"requests\",\"id\":\"r-1\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-2\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2026-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-3\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"blocked\",\"leaseUntil\":\"2026-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-4\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"status\":\"done\"},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-5\",\"data\":{\"text\":\"Make the lead colder\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-6\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-7\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000f\"},\"actor\":\"agent-c\",\"token\":\"tok-9\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-8\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"},\"response\":\"Old answer.\"},\"revision\":4},{\"collection\":\"requests\",\"id\":\"r-9\",\"data\":{\"text\":\"Make the lead warmer\",\"quote\":\"Hi\",\"scope\":{\"part\":\"home.lead\"}},\"revision\":4}]",
  "inc.json": "[{\"collection\":\"incoming\",\"id\":\"p-1\",\"data\":{\"files\":[{\"path\":\"parts/app.js\",\"content\":\"\"},{\"path\":\"parts/old.js\",\"content\":null}],\"parts\":[],\"base\":{\"version\":\"7\"},\"status\":\"proposed\"},\"revision\":4},{\"collection\":\"incoming\",\"id\":\"p-2\",\"data\":{\"files\":[{\"path\":\"parts/app.js\",\"content\":\"\"},{\"path\":\"parts/old.js\",\"content\":null}],\"parts\":[],\"base\":{\"version\":\"7\"},\"status\":\"proposed\",\"publishRequest\":{\"inputHash\":\"sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805\"}},\"revision\":4},{\"collection\":\"incoming\",\"id\":\"p-3\",\"data\":{\"files\":[{\"path\":\"parts/app.js\",\"content\":\"\"},{\"path\":\"parts/old.js\",\"content\":null}],\"parts\":[],\"base\":{\"version\":\"7\"},\"status\":\"proposed\",\"publishRequest\":{\"inputHash\":\"sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805\"},\"execution\":{\"schema\":\"adp-work/1\",\"origin\":{\"host\":\"claude\",\"artifact\":\"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b\"},\"actor\":\"agent-a\",\"token\":\"tok-1\",\"attempt\":1,\"inputHash\":\"sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805\",\"claimedAt\":\"2026-11-20T10:00:00Z\",\"state\":\"working\",\"leaseUntil\":\"2099-01-01T00:00:00Z\",\"updatedAt\":\"2026-11-20T10:00:00Z\"}},\"revision\":4}]",
  "rc-pub.json": "{\"checks\":[{\"name\":\"published\",\"passed\":true,\"evidence\":\"deployment 8 read back\"}],\"deployment\":{\"status\":\"succeeded\",\"id\":\"8\",\"version_id\":\"v-8\",\"project_id\":\"site-1\"},\"source\":{\"commit_sha\":\"0123456789abcdef0123456789abcdef01234567\",\"version_id\":\"v-8\",\"project_id\":\"site-1\",\"shas\":{\"parts/app.js\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"}},\"manifest\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\",\"files\":{\"parts/app.js\":\"e3b0c44298fc\"}}},\"change\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\"}},\"readback\":{\"shas\":{\"parts/app.js\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"},\"removed\":{\"parts/old.js\":true}}}",
  "rc-pub-failed.json": "{\"checks\":[{\"name\":\"published\",\"passed\":true,\"evidence\":\"deployment 8 read back\"}],\"deployment\":{\"status\":\"failed\",\"id\":\"8\",\"version_id\":\"v-8\",\"project_id\":\"site-1\"},\"source\":{\"commit_sha\":\"0123456789abcdef0123456789abcdef01234567\",\"version_id\":\"v-8\",\"project_id\":\"site-1\",\"shas\":{\"parts/app.js\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"}},\"manifest\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\",\"files\":{\"parts/app.js\":\"e3b0c44298fc\"}}},\"change\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\"}},\"readback\":{\"shas\":{\"parts/app.js\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"},\"removed\":{\"parts/old.js\":true}}}",
  "rc-pub-badhash.json": "{\"checks\":[{\"name\":\"published\",\"passed\":true,\"evidence\":\"deployment 8 read back\"}],\"deployment\":{\"status\":\"succeeded\",\"id\":\"8\",\"version_id\":\"v-8\",\"project_id\":\"site-1\"},\"source\":{\"commit_sha\":\"0123456789abcdef0123456789abcdef01234567\",\"version_id\":\"v-8\",\"project_id\":\"site-1\",\"shas\":{\"parts/app.js\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\"}},\"manifest\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\",\"files\":{\"parts/app.js\":\"e3b0c44298fc\"}}},\"change\":{\"exists\":true,\"revision\":1,\"data\":{\"version\":\"8\"}},\"readback\":{\"shas\":{\"parts/app.js\":\"0000000000000000000000000000000000000000000000000000000000000000\"},\"removed\":{\"parts/old.js\":true}}}",
  "rc-reply.json": "{\"checks\":[{\"name\":\"lead reads warmer\",\"passed\":true,\"evidence\":\"turn 0002 read back\"}],\"reply\":{\"path\":\"requests/r-8/turns/0002\",\"exists\":true,\"revision\":1,\"data\":{\"text\":\"Fixed\",\"by\":\"agent-a\",\"at\":\"2026-11-20T11:00:00Z\"}}}",
  "ckpt.json": "{\"step\":2}"
 }
}
```

```json vector
{
 "vector": "work-refusals",
 "steps": [
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/a b",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "work needs --host claude --artifact ID --path requests/ID|incoming/ID"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-9",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "work accepts one native read file"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-9",
    "--action",
    "zap",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "work needs --by NAME and --action claim|progress|checkpoint|block|complete"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-9",
    "--action",
    "claim"
   ],
   "exit": 1,
   "stderr_text": [
    "work needs --by NAME and --action claim|progress|checkpoint|block|complete"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-9",
    "--action",
    "claim",
    "--by",
    "agent-a",
    "--lease-seconds",
    "5"
   ],
   "exit": 1,
   "stderr_text": [
    "Lease must be between 30 and 7200 seconds"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-4",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Work is already closed; reread before starting another operation"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-3",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Blocked work needs new user input or a renewed publication request"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-6",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Legacy unbound lease is still active; wait for expiry before a fresh claim"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-1",
    "--action",
    "progress",
    "--token",
    "tok-1",
    "--by",
    "agent-b",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "Lease expired, changed input or wrong claimant; reread and reclaim before work"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-2",
    "--action",
    "progress",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "Lease expired, changed input or wrong claimant; reread and reclaim before work"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-5",
    "--action",
    "progress",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "Lease expired, changed input or wrong claimant; reread and reclaim before work"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-7",
    "--action",
    "progress",
    "--token",
    "tok-9",
    "--by",
    "agent-c",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "Lease expired, changed input or wrong claimant; reread and reclaim before work"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-1",
    "--action",
    "progress",
    "--token",
    "tok-1",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Describe the progress, blocker or verified result with --text"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-1",
    "--action",
    "checkpoint",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "checkpoint needs --checkpoint JSON_FILE"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-1",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "Completion needs --receipt JSON_FILE with verified evidence"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-0",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Read the existing work record and its native revision first"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "work-checkpoint-and-foreign-claim",
 "steps": [
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-1",
    "--action",
    "checkpoint",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Step 2 done",
    "--checkpoint",
    "{wk}/ckpt.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-work-plan/1",
    "path": "requests/r-1",
    "action": "checkpoint",
    "leaseToken": "tok-1",
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "requests",
         "doc_id": "r-1",
         "data": {
          "text": "Make the lead warmer",
          "quote": "Hi",
          "scope": {
           "part": "home.lead"
          },
          "execution": {
           "schema": "adp-work/1",
           "origin": {
            "host": "claude",
            "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
           },
           "actor": "agent-a",
           "token": "tok-1",
           "attempt": 1,
           "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
           "claimedAt": "<time>",
           "state": "working",
           "leaseUntil": "<time>",
           "updatedAt": "<time>",
           "checkpoint": {
            "step": 2
           }
          },
          "progress": [
           {
            "at": "<time>",
            "text": "Step 2 done",
            "by": "agent-a"
           }
          ],
          "state": "working",
          "delivery": "acknowledged"
         },
         "if_version": 4
        }
       ]
      },
      "atomic": true,
      "keys": [
       "requests/r-1"
      ]
     }
    ],
    "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
    "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
   }
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-7"
   ],
   "exit": 0,
   "stdout": {
    "path": "requests/r-7",
    "revision": 4,
    "status": null,
    "resolved": false,
    "execution": {
     "schema": "adp-work/1",
     "origin": {
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000f"
     },
     "actor": "agent-c",
     "token": "tok-9",
     "attempt": 1,
     "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
     "claimedAt": "<time>",
     "state": "working",
     "leaseUntil": "<time>",
     "updatedAt": "<time>"
    },
    "foreign": true
   }
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-7",
    "--action",
    "claim",
    "--by",
    "agent-b"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-work-plan/1",
    "path": "requests/r-7",
    "action": "claim",
    "leaseToken": "<uuid>",
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "requests",
         "doc_id": "r-7",
         "data": {
          "text": "Make the lead warmer",
          "quote": "Hi",
          "scope": {
           "part": "home.lead"
          },
          "execution": {
           "schema": "adp-work/1",
           "origin": {
            "host": "claude",
            "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
           },
           "actor": "agent-b",
           "token": "<uuid>",
           "attempt": 1,
           "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
           "claimedAt": "<time>",
           "state": "working",
           "leaseUntil": "<time>",
           "updatedAt": "<time>"
          },
          "executionProvenance": [
           {
            "schema": "adp-work/1",
            "origin": {
             "host": "claude",
             "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000f"
            },
            "actor": "agent-c",
            "token": "tok-9",
            "attempt": 1,
            "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
            "claimedAt": "<time>",
            "state": "working",
            "leaseUntil": "<time>",
            "updatedAt": "<time>"
           }
          ],
          "ackBy": "agent-b",
          "ackAt": "<time>",
          "state": "working",
          "delivery": "acknowledged"
         },
         "if_version": 4
        }
       ]
      },
      "atomic": true,
      "keys": [
       "requests/r-7"
      ]
     }
    ],
    "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
    "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
   }
  }
 ]
}
```

```json vector
{
 "vector": "work-reopened-request",
 "steps": [
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-8",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Fixed",
    "--receipt",
    "{wk}/receipt.json"
   ],
   "exit": 1,
   "stderr_text": [
    "Reopened request needs a verified new native reply turn; preserve the original response"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/n.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "requests/r-8",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Fixed",
    "--receipt",
    "{wk}/rc-reply.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-work-plan/1",
    "path": "requests/r-8",
    "action": "complete",
    "leaseToken": "tok-1",
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "requests",
         "doc_id": "r-8",
         "data": {
          "text": "Make the lead warmer",
          "quote": "Hi",
          "scope": {
           "part": "home.lead"
          },
          "execution": {
           "schema": "adp-work/1",
           "origin": {
            "host": "claude",
            "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
           },
           "actor": "agent-a",
           "token": "tok-1",
           "attempt": 1,
           "inputHash": "sha256:967c0e67cbb65035fcf25215e53d38925b564d3c2954147b11402a985034196e",
           "claimedAt": "<time>",
           "state": "done",
           "leaseUntil": "<time>",
           "updatedAt": "<time>",
           "receipt": {
            "checks": [
             {
              "name": "lead reads warmer",
              "passed": true,
              "evidence": "turn 0002 read back"
             }
            ],
            "reply": {
             "path": "requests/r-8/turns/0002",
             "exists": true,
             "revision": 1,
             "data": {
              "text": "Fixed",
              "by": "agent-a",
              "at": "<time>"
             }
            }
           },
           "result": "Fixed"
          },
          "response": "Old answer.",
          "progress": [
           {
            "at": "<time>",
            "text": "Fixed",
            "by": "agent-a"
           }
          ],
          "status": "done",
          "doneAt": "<time>",
          "state": "done",
          "delivery": "completed"
         },
         "if_version": 4
        }
       ]
      },
      "atomic": true,
      "keys": [
       "requests/r-8"
      ]
     }
    ],
    "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
    "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
   }
  }
 ]
}
```

```json vector
{
 "vector": "work-incoming-proposal",
 "steps": [
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/inc.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "incoming/p-1",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 1,
   "stderr_text": [
    "Publication needs editor approval bound to the current proposal (sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805)"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/inc.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "incoming/p-2",
    "--action",
    "claim",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-work-plan/1",
    "path": "incoming/p-2",
    "action": "claim",
    "leaseToken": "<uuid>",
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "incoming",
         "doc_id": "p-2",
         "data": {
          "files": [
           {
            "path": "parts/app.js",
            "content": ""
           },
           {
            "path": "parts/old.js",
            "content": null
           }
          ],
          "parts": [],
          "base": {
           "version": "7"
          },
          "status": "proposed",
          "publishRequest": {
           "inputHash": "sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805"
          },
          "ackBy": "agent-a",
          "ackAt": "<time>",
          "execution": {
           "schema": "adp-work/1",
           "origin": {
            "host": "claude",
            "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
           },
           "actor": "agent-a",
           "token": "<uuid>",
           "attempt": 1,
           "inputHash": "sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805",
           "claimedAt": "<time>",
           "state": "working",
           "leaseUntil": "<time>",
           "updatedAt": "<time>"
          }
         },
         "if_version": 4
        }
       ]
      },
      "atomic": true,
      "keys": [
       "incoming/p-2"
      ]
     }
    ],
    "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
    "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
   }
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/inc.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "incoming/p-3",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Published",
    "--receipt",
    "{wk}/rc-pub-failed.json"
   ],
   "exit": 1,
   "stderr_text": [
    "Completion needs a successful native deployment receipt"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/inc.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "incoming/p-3",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Published",
    "--receipt",
    "{wk}/rc-pub-badhash.json"
   ],
   "exit": 1,
   "stderr_text": [
    "Proposal, deployed source and recorded manifest hashes must match"
   ]
  },
  {
   "run": [
    "adp.py",
    "work",
    "{wk}/inc.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--path",
    "incoming/p-3",
    "--action",
    "complete",
    "--token",
    "tok-1",
    "--by",
    "agent-a",
    "--text",
    "Published",
    "--receipt",
    "{wk}/rc-pub.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-work-plan/1",
    "path": "incoming/p-3",
    "action": "complete",
    "leaseToken": "tok-1",
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "incoming",
         "doc_id": "p-3",
         "data": {
          "files": [
           {
            "path": "parts/app.js",
            "content": ""
           },
           {
            "path": "parts/old.js",
            "content": null
           }
          ],
          "parts": [],
          "base": {
           "version": "7"
          },
          "status": "applied",
          "publishRequest": {
           "inputHash": "sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805"
          },
          "execution": {
           "schema": "adp-work/1",
           "origin": {
            "host": "claude",
            "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
           },
           "actor": "agent-a",
           "token": "tok-1",
           "attempt": 1,
           "inputHash": "sha256:46967d59c4da522d9fe8a12dc2a53973506529ca54b3ecb198fb31e86c4c5805",
           "claimedAt": "<time>",
           "state": "done",
           "leaseUntil": "<time>",
           "updatedAt": "<time>",
           "receipt": {
            "checks": [
             {
              "name": "published",
              "passed": true,
              "evidence": "deployment 8 read back"
             }
            ],
            "deployment": {
             "status": "succeeded",
             "id": "8",
             "version_id": "v-8",
             "project_id": "site-1"
            },
            "source": {
             "commit_sha": "<commit>",
             "version_id": "v-8",
             "project_id": "site-1",
             "shas": {
              "parts/app.js": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
             }
            },
            "manifest": {
             "exists": true,
             "revision": 1,
             "data": {
              "version": "8",
              "files": {
               "parts/app.js": "e3b0c44298fc"
              }
             }
            },
            "change": {
             "exists": true,
             "revision": 1,
             "data": {
              "version": "8"
             }
            },
            "readback": {
             "shas": {
              "parts/app.js": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
             },
             "removed": {
              "parts/old.js": true
             }
            }
           },
           "result": "Published"
          },
          "progress": [
           {
            "at": "<time>",
            "text": "Published",
            "by": "agent-a"
           }
          ],
          "applied": {
           "version": "8",
           "at": "<time>"
          },
          "decided": {
           "by": "agent-a",
           "at": "<time>",
           "reason": "Published"
          }
         },
         "if_version": 4
        }
       ]
      },
      "atomic": true,
      "keys": [
       "incoming/p-3"
      ]
     }
    ],
    "next": "Execute the guarded call and verify its native readback before any side effect. On unknown outcome inspect; never blindly retry.",
    "verification": "Evidence is supplied by the authorized executor; this planner does not independently attest host receipts."
   }
  }
 ]
}
```

A request whose `progress`, `scope` or `execution.origin` is null lists and takes a progress step as if it were empty or missing, and an option that takes a value but comes last has no value.

```json fixture
{"fixture": "asks-null", "files": {"dump.json": "[{\"id\": \"r-1\", \"version\": 2, \"data\": {\"lane\": \"edit\", \"text\": \"Null progress\", \"by\": \"viewer-1\", \"at\": \"2026-11-19T09:00:00Z\", \"progress\": null, \"scope\": null, \"execution\": {\"actor\": \"agent-a\", \"state\": \"working\", \"origin\": null}}}, {\"id\": \"r-2\", \"version\": 1, \"data\": {\"lane\": \"ask\", \"text\": \"Null last step\", \"by\": \"viewer-2\", \"at\": \"2026-11-19T10:00:00Z\", \"progress\": [{\"at\": \"2026-11-19T10:05:00Z\", \"text\": \"first\"}, null]}}]"}}
```

```json vector
{
 "vector": "requests-null-fields",
 "steps": [
  {
   "run": [
    "adp.py",
    "requests",
    "{asks-null}/dump.json"
   ],
   "exit": 0,
   "stdout": {
    "open": [
     {
      "id": "r-1",
      "lane": "edit",
      "state": "queue",
      "scope": {},
      "project": "",
      "text": "Null progress",
      "quote": "",
      "by": "viewer-1",
      "at": "<time>",
      "reopened": false,
      "last_progress": "",
      "resolved": false,
      "lease": {
       "actor": "agent-a",
       "state": "working",
       "until": null,
       "attempt": null,
       "host": null
      }
     },
     {
      "id": "r-2",
      "lane": "ask",
      "state": "queue",
      "scope": {},
      "project": "",
      "text": "Null last step",
      "quote": "",
      "by": "viewer-2",
      "at": "<time>",
      "reopened": false,
      "last_progress": "",
      "resolved": false,
      "lease": null
     }
    ],
    "count": 2,
    "trailer": "· adp request {<rid>} · lane <lane> · scope part:<id>|page"
   }
  },
  {
   "run": [
    "adp.py",
    "requests",
    "{asks-null}/dump.json",
    "--progress",
    "r-1",
    "--text",
    "Drafting",
    "--by",
    "agent-a",
    "--out",
    "{out}"
   ],
   "exit": 0,
   "stdout": {
    "request": "r-1",
    "state": "working",
    "batches": [
     [
      {
       "op": "update",
       "collection": "requests",
       "doc_id": "r-1",
       "file_path": "<tmp>/out/requests__r-1.json",
       "if_version": 2
      },
      {
       "op": "set",
       "collection": "presence",
       "doc_id": "agent-a",
       "file_path": "<tmp>/out/presence__agent-a.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/out"
   }
  },
  {
   "run": [
    "adp.py",
    "hold",
    "{page-a}",
    "home.lead",
    "--out",
    "{out}",
    "--by"
   ],
   "exit": 0,
   "stdout": {
    "hold_until": "<time>",
    "batches": [
     [
      {
       "op": "update",
       "collection": "parts",
       "doc_id": "home.lead",
       "file_path": "<tmp>/out/parts__home.lead.json"
      },
      {
       "op": "set",
       "collection": "agents",
       "doc_id": "agent",
       "file_path": "<tmp>/out/agents__agent.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/out",
    "needs_pin": [
     "parts/home.lead"
    ]
   }
  }
 ]
}
```
