# Vectors: adp-minimal-protocol

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

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
   "holder": "",
   "hold_until": "",
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
