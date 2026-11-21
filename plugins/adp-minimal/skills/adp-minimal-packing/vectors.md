# Vectors: adp-minimal-packing

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them, against the tools built from the skills.

## Contract: `files`, `files --host single`, `unpack`, `seed`

```json vector
{
 "vector": "files-publish-args",
 "run": [
  "adp.py",
  "files",
  "{page-a}"
 ],
 "exit": 0,
 "stdout": {
  "file_path": "<tmp>/page-a/index.html",
  "root": "<tmp>/page-a",
  "files": {
   "parts/app.js": "parts/app.js",
   "styles/page.css": "styles/page.css"
  }
 }
}
```

```json vector
{
 "vector": "files-since-a-manifest",
 "run": [
  "adp.py",
  "files",
  "{page-a2}",
  "--since",
  "{rec}/old.json"
 ],
 "exit": 0,
 "stdout": {
  "file_path": "<tmp>/page-a2/index.html",
  "root": "<tmp>/page-a2",
  "files": {},
  "page_changed": true
 }
}
```

```json vector
{
 "vector": "pack-and-unpack-round-trip",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-a}",
    "--host",
    "single",
    "--out",
    "{out}/one.html"
   ],
   "exit": 0,
   "stdout": {
    "host": "single",
    "out": "<tmp>/out/one.html",
    "files": 3,
    "bytes": 2903,
    "fragment": false
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{out}/one.html",
    "{out}/back"
   ],
   "exit": 0,
   "stdout": {
    "dest": "<tmp>/out/back",
    "files": 3,
    "bytes": 471
   }
  },
  {
   "same_tree": [
    "{page-a}",
    "{out}/back"
   ]
  },
  {
   "same_tree": [
    "{out}/back",
    "{page-a}"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "unpack-refuses-a-non-empty-folder",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-a}",
    "--host",
    "single",
    "--out",
    "{out}/one.html"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{out}/one.html",
    "{page-a2}"
   ],
   "exit": 1,
   "stdout_text": [],
   "stderr_text": [
    "unpack: <tmp>/page-a2 is not empty"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "seed-dry-run",
 "run": [
  "adp.py",
  "seed",
  "{page-a}",
  "--by",
  "agent-a",
  "--dry-run"
 ],
 "exit": 0,
 "stdout": {
  "collections": {
   "parts": 5,
   "changes": 1,
   "agents": 1,
   "manifest": 1
  },
  "docs": 8,
  "batches": 1,
  "skipped_empty": [],
  "bytes": 2541
 }
}
```

`ADP_PACK` sets the byte size at which `seed` starts another pack:

```json vector
{
 "vector": "seed-pack-size-from-the-environment",
 "run": [
  "adp.py",
  "seed",
  "{page-a}",
  "--by",
  "agent-a",
  "--version",
  "1"
 ],
 "env": {
  "ADP_PACK": "700"
 },
 "exit": 0,
 "stdout": {
  "seed": "<tmp>/page-a/seed.json",
  "written": true,
  "docs": 8,
  "collections": {
   "parts": 5,
   "changes": 1,
   "agents": 1,
   "manifest": 1
  },
  "packs": [
   "seed/pack-001.json",
   "seed/pack-002.json",
   "seed/pack-003.json",
   "seed/pack-004.json",
   "seed/pack-005.json"
  ],
  "bytes": 3246,
  "skipped_empty": [],
  "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
 }
}
```

```json vector
{
 "vector": "seed-files",
 "run": [
  "adp.py",
  "seed",
  "{page-a}",
  "--by",
  "agent-a",
  "--version",
  "1"
 ],
 "exit": 0,
 "stdout": {
  "seed": "<tmp>/page-a/seed.json",
  "written": true,
  "docs": 8,
  "collections": {
   "parts": 5,
   "changes": 1,
   "agents": 1,
   "manifest": 1
  },
  "packs": [
   "seed/pack-001.json"
  ],
  "bytes": 3030,
  "skipped_empty": [],
  "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
 },
 "files_out": {
  "{page-a}/seed.json": {
   "schema": "adp-seed/2",
   "at": "<time>",
   "version": "1",
   "by": "agent-a",
   "overrides": [],
   "docs": 8,
   "collections": {
    "parts": 5,
    "changes": 1,
    "agents": 1,
    "manifest": 1
   },
   "packs": [
    "seed/pack-001.json"
   ]
  },
  "{page-a}/seed/pack-001.json": {
   "schema": "adp-seed/2",
   "pack": 1,
   "of": 1,
   "docs": [
    {
     "collection": "parts",
     "id": "home",
     "data": {
      "title": "home",
      "parent": "",
      "hash": "081b78b8f894",
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "added in the first build",
      "holder": "",
      "hold_until": "",
      "file": "index.html"
     }
    },
    {
     "collection": "parts",
     "id": "home.lead",
     "data": {
      "title": "home.lead",
      "parent": "home",
      "hash": "c6a82a517ff8",
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "added in the first build",
      "holder": "",
      "hold_until": "",
      "file": "index.html"
     }
    },
    {
     "collection": "parts",
     "id": "page.header",
     "data": {
      "title": "page.header",
      "parent": "",
      "hash": "0d957e9aee8d",
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "added in the first build",
      "holder": "",
      "hold_until": "",
      "file": "index.html"
     }
    },
    {
     "collection": "parts",
     "id": "page.script.app",
     "data": {
      "title": "page.script.app",
      "parent": "",
      "hash": "35c146f76e12",
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "added in the first build",
      "holder": "",
      "hold_until": "",
      "file": "parts/app.js"
     }
    },
    {
     "collection": "parts",
     "id": "page.style",
     "data": {
      "title": "page.style",
      "parent": "",
      "hash": "997faceca260",
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "added in the first build",
      "holder": "",
      "hold_until": "",
      "file": "styles/page.css"
     }
    },
    {
     "collection": "changes",
     "id": "000001",
     "data": {
      "version": "1",
      "at": "<time>",
      "by": "agent-a",
      "summary": "adp/2 adopted: first build",
      "parts": [
       {
        "id": "home",
        "from": "",
        "to": "081b78b8f894"
       },
       {
        "id": "home.lead",
        "from": "",
        "to": "c6a82a517ff8"
       },
       {
        "id": "page.header",
        "from": "",
        "to": "0d957e9aee8d"
       },
       {
        "id": "page.script.app",
        "from": "",
        "to": "35c146f76e12"
       },
       {
        "id": "page.style",
        "from": "",
        "to": "997faceca260"
       }
      ],
      "threads": []
     }
    },
    {
     "collection": "agents",
     "id": "agent-a",
     "data": {
      "role": "",
      "session": "",
      "last_seen": "<time>",
      "holds": []
     }
    },
    {
     "collection": "manifest",
     "id": "current",
     "data": {
      "schema": "adp/2",
      "version": "1",
      "page_hash": "7f4556515dd9",
      "parts": {
       "page.header": "0d957e9aee8d",
       "home.lead": "c6a82a517ff8",
       "home": "081b78b8f894",
       "_rest:index.html": "ee2d7cd8fa75",
       "page.script.app": "35c146f76e12",
       "_rest:parts/app.js": "e3b0c44298fc",
       "page.style": "997faceca260",
       "_rest:styles/page.css": "e3b0c44298fc"
      },
      "elements": {
       "page.header": 1,
       "home.lead": 1,
       "home": 1,
       "_rest:index.html": 2,
       "page.script.app": 0,
       "_rest:parts/app.js": 0,
       "page.style": 0,
       "_rest:styles/page.css": 0
      },
      "files": {
       "index.html": "bd002c3d502b",
       "parts/app.js": "574c60bebc47",
       "styles/page.css": "56ee869c6a7b"
      },
      "part_file": {
       "page.header": "index.html",
       "home.lead": "index.html",
       "home": "index.html",
       "_rest:index.html": "index.html",
       "page.script.app": "parts/app.js",
       "_rest:parts/app.js": "parts/app.js",
       "page.style": "styles/page.css",
       "_rest:styles/page.css": "styles/page.css"
      },
      "content": {},
      "at": "<time>",
      "by": "agent-a"
     }
    }
   ]
  }
 }
}
```

## Contract: records from raw reads, a return trip and a selection

```json fixture
{"fixture": "raw", "files": {
 "all.json": "[{\"call\": {\"collection\": \"manifest\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"parts\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"content\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"changes\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"decisions\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"config\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"agents\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"incoming\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"requests\"}, \"result\": \"{\\\"id\\\": \\\"r1\\\", \\\"data\\\": {\\\"title\\\": \\\"Q\\\"}, \\\"version\\\": 3}\"}]",
 "turns.json": "[{\"call\": {\"collection\": \"manifest\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"parts\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"content\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"changes\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"decisions\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"config\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"agents\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"incoming\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"requests\"}, \"result\": \"{\\\"id\\\": \\\"r1\\\", \\\"data\\\": {\\\"title\\\": \\\"Q\\\"}, \\\"version\\\": 3}\"}, {\"call\": {\"collection\": \"requests/r1/turns\"}, \"result\": \"{\\\"id\\\": \\\"t1\\\", \\\"data\\\": {\\\"text\\\": \\\"Hi\\\"}, \\\"version\\\": 1}\"}, {\"call\": {\"collection\": \"notes\"}, \"result\": \"{\\\"id\\\": \\\"n1\\\", \\\"data\\\": {\\\"text\\\": \\\"Note\\\"}, \\\"version\\\": 2}\"}]",
 "more-pages.json": "[{\"call\": {\"collection\": \"manifest\"}, \"result\": \"{\\\"id\\\": \\\"current\\\", \\\"data\\\": {}, \\\"version\\\": 1}\\nnext_cursor: abc\"}]",
 "target-empty.json": "[{\"call\": {\"collection\": \"changes\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"decisions\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"imports\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"manifest\"}, \"result\": \"\"}, {\"call\": {\"collection\": \"parts\"}, \"result\": \"\"}]",
 "receipts-ok.json": "[{\"call\": {\"keys\": [\"changes/000008\", \"decisions/lead-tone\", \"parts/home.lead\", \"manifest/current\"]}, \"result\": \"- set \\\"changes\\\"/\\\"000008\\\" (version 1)\\n- set \\\"decisions\\\"/\\\"lead-tone\\\" (version 1)\\n- set \\\"parts\\\"/\\\"home.lead\\\" (version 1)\\n- set \\\"manifest\\\"/\\\"current\\\" (version 1)\"}]",
 "receipts-bad.json": "[{\"call\": {\"keys\": [\"changes/000008\", \"decisions/lead-tone\", \"parts/home.lead\", \"manifest/current\"]}, \"result\": \"db batch write failed: if_version mismatch\"}]",
 "receipts-unknown.json": "[{\"call\": {\"keys\": [\"changes/000008\", \"decisions/lead-tone\", \"parts/home.lead\", \"manifest/current\"]}, \"result\": \"timed out\"}]"}}
```

```json fixture
{"fixture": "move2", "files": {
 "ancestor.json": "{\"docs\": [{\"collection\": \"decisions\", \"id\": \"lead-tone\", \"data\": {\"text\": \"Instruct, briefly.\", \"by\": \"someone\"}, \"revision\": 2}]}",
 "target-no-revision.json": "{\"docs\": [{\"collection\": \"decisions\", \"id\": \"lead-tone\", \"data\": {\"text\": \"Instruct, briefly.\", \"by\": \"someone\"}}]}"}}
```

```json vector
{
 "vector": "bundle-from-raw-reads",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--collections",
    "notes"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "manifest",
       "query": {
        "limit": 1000
       }
      },
      "collection": "manifest"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "parts",
       "query": {
        "limit": 1000
       }
      },
      "collection": "parts"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "content",
       "query": {
        "limit": 1000
       }
      },
      "collection": "content"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "changes",
       "query": {
        "limit": 1000
       }
      },
      "collection": "changes"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "decisions",
       "query": {
        "limit": 1000
       }
      },
      "collection": "decisions"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "config",
       "query": {
        "limit": 1000
       }
      },
      "collection": "config"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "agents",
       "query": {
        "limit": 1000
       }
      },
      "collection": "agents"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "incoming",
       "query": {
        "limit": 1000
       }
      },
      "collection": "incoming"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "requests",
       "query": {
        "limit": 1000
       }
      },
      "collection": "requests"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "notes",
       "query": {
        "limit": 1000
       }
      },
      "collection": "notes"
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{raw}/all.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--raw"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
       "collection": "requests/r1/turns",
       "query": {
        "limit": 1000
       }
      },
      "collection": "requests/r1/turns"
     }
    ]
   },
   "stderr_text": [
    "append the results of these reads to the same file and run bundle again"
   ]
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{raw}/turns.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--raw",
    "--collections",
    "notes",
    "--version",
    "3"
   ],
   "exit": 0,
   "stdout": {
    "bundle": "b-aa0e5bfe8b50",
    "docs": 3,
    "dir": "<tmp>/out/b"
   },
   "files_out": {
    "{out}/b/seed.json": {
     "schema": "adp-seed/2",
     "version": "3",
     "by": "adp",
     "at": "<time>",
     "overrides": [],
     "source": {
      "id": "b-aa0e5bfe8b50",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "3",
      "exportedAt": "<time>",
      "by": "adp"
     },
     "revisions": {
      "notes/n1": 2,
      "requests/r1": 3,
      "requests/r1/turns/t1": 1
     },
     "docs": 3,
     "collections": {
      "notes": 1,
      "requests": 1,
      "requests/r1/turns": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{raw}/more-pages.json",
    "{out}/c",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--raw"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/raw/more-pages.json: the read is incomplete (manifest: more pages (next_cursor)): read again before planning"
   ]
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "--host",
    "sites",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a"
   ],
   "exit": 1,
   "stderr_text": [
    "--host names the adapter: claude"
   ]
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "--host",
    "claude"
   ],
   "exit": 1,
   "stderr_text": [
    "--artifact names the source artifact"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "move-return-trip-with-a-base-and-a-selection",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8",
    "--by",
    "agent-a"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{move2}/ancestor.json",
    "{out}/a",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-differs.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--base",
    "{out}/a"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 4,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [],
    "ops": [
     {
      "key": "changes/000008",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "changes",
      "id": "000008",
      "data": {
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording",
       "parts": [
        {
         "id": "home.lead",
         "from": "c6a82a517ff8",
         "to": "8e7c2ba46ff4"
        }
       ]
      }
     },
     {
      "key": "decisions/lead-tone",
      "class": "ours",
      "baseHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "liveHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": 2,
      "action": "replace",
      "op": "replace",
      "collection": "decisions",
      "id": "lead-tone",
      "data": {
       "text": "Greet, do not instruct.",
       "by": "owner"
      }
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "parts",
      "id": "home.lead",
      "data": {
       "hash": "8e7c2ba46ff4",
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording"
      }
     },
     {
      "key": "manifest/current",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "manifest",
      "id": "current",
      "data": {
       "schema": "adp/2",
       "version": "8",
       "page_hash": "c125279381ff",
       "parts": {
        "home": "f98716c9ddf4",
        "home.lead": "8e7c2ba46ff4"
       }
      }
     }
    ],
    "held": [],
    "counts": {
     "create": 3,
     "replace": 1,
     "skip": 0,
     "hold": 0
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {
      "decisions/lead-tone": {
       "hash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7"
      }
     }
    },
    "order": {
     "last": "manifest/current",
     "rule": "run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current"
    },
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "000008",
         "data": {
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording",
          "parts": [
           {
            "id": "home.lead",
            "from": "c6a82a517ff8",
            "to": "8e7c2ba46ff4"
           }
          ]
         }
        },
        {
         "op": "set",
         "collection": "decisions",
         "doc_id": "lead-tone",
         "data": {
          "text": "Greet, do not instruct.",
          "by": "owner"
         },
         "if_version": 2
        },
        {
         "op": "set",
         "collection": "parts",
         "doc_id": "home.lead",
         "data": {
          "hash": "8e7c2ba46ff4",
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording"
         }
        },
        {
         "op": "set",
         "collection": "manifest",
         "doc_id": "current",
         "data": {
          "schema": "adp/2",
          "version": "8",
          "page_hash": "c125279381ff",
          "parts": {
           "home": "f98716c9ddf4",
           "home.lead": "8e7c2ba46ff4"
          }
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "changes/000008",
       "decisions/lead-tone",
       "parts/home.lead",
       "manifest/current"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move2}/target-no-revision.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--base",
    "{out}/a"
   ],
   "exit": 2,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 4,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [],
    "ops": [
     {
      "key": "changes/000008",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "changes",
      "id": "000008",
      "data": {
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording",
       "parts": [
        {
         "id": "home.lead",
         "from": "c6a82a517ff8",
         "to": "8e7c2ba46ff4"
        }
       ]
      }
     },
     {
      "key": "decisions/lead-tone",
      "class": "ours",
      "baseHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "liveHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": null,
      "action": "hold",
      "why": "target has no revision to guard the write with"
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "parts",
      "id": "home.lead",
      "data": {
       "hash": "8e7c2ba46ff4",
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording"
      }
     },
     {
      "key": "manifest/current",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "manifest",
      "id": "current",
      "data": {
       "schema": "adp/2",
       "version": "8",
       "page_hash": "c125279381ff",
       "parts": {
        "home": "f98716c9ddf4",
        "home.lead": "8e7c2ba46ff4"
       }
      }
     }
    ],
    "held": [
     "decisions/lead-tone"
    ],
    "counts": {
     "create": 3,
     "replace": 0,
     "skip": 0,
     "hold": 1
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {
      "decisions/lead-tone": {
       "hash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7"
      }
     }
    },
    "order": {
     "last": "manifest/current",
     "rule": "run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--only",
    "decisions,parts"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "decisions",
       "query": {
        "limit": 1000
       }
      },
      "collection": "decisions"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "imports",
       "query": {
        "limit": 1000
       }
      },
      "collection": "imports"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "parts",
       "query": {
        "limit": 1000
       }
      },
      "collection": "parts"
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--only",
    "decisions",
    "--out",
    "{out}/plan.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 1,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [
     "decisions"
    ],
    "ops": [
     {
      "key": "decisions/lead-tone",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "decisions",
      "id": "lead-tone",
      "data": {
       "text": "Greet, do not instruct.",
       "by": "owner"
      }
     }
    ],
    "held": [],
    "counts": {
     "create": 1,
     "replace": 0,
     "skip": 0,
     "hold": 0
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {}
    },
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "decisions",
         "doc_id": "lead-tone",
         "data": {
          "text": "Greet, do not instruct.",
          "by": "owner"
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "decisions/lead-tone"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{move}/receipts-all.json",
    "--host",
    "claude",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "applied": 1,
    "failed": [],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {
           "decisions/lead-tone": {
            "hash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
            "revision": 1
           }
          },
          "only": [
           "decisions"
          ]
         }
        },
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "d-<ms>",
         "data": {
          "version": "",
          "at": "<time>",
          "by": "agent-a",
          "parts": [],
          "threads": [],
          "summary": "Imported 1 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "data": [
           {
            "doc": "decisions/lead-tone"
           },
           {
            "doc": "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
           }
          ]
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
       "changes/d-<ms>"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{page-a}",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/page-a is not a bundle (adp.py bundle writes one)"
   ]
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/a",
    "{move}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--base",
    "{page-a}"
   ],
   "exit": 1,
   "stderr_text": [
    "--base <tmp>/page-a is not a bundle (adp.py bundle writes one)"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--base",
    "{page-a}"
   ],
   "exit": 2
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/c",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--at",
    "at-given"
   ],
   "exit": 0,
   "files_out": {
    "{out}/c/seed.json": {
     "schema": "adp-seed/2",
     "version": "1",
     "by": "adp",
     "at": "at-given",
     "overrides": [],
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "",
      "exportedAt": "at-given",
      "by": "adp"
     },
     "revisions": {
      "changes/000008": 1,
      "decisions/lead-tone": 1,
      "manifest/current": 9,
      "parts/home.lead": 4
     },
     "docs": 4,
     "collections": {
      "changes": 1,
      "decisions": 1,
      "manifest": 1,
      "parts": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    }
   }
  }
 ]
}
```

```json vector
{
 "vector": "move-through-the-raw-adapter",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8",
    "--by",
    "agent-a"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/raw-manifest-only.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--raw"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/move/raw-manifest-only.json: the read does not cover changes, decisions, imports, parts: read them again before planning"
   ]
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{raw}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--raw",
    "--out",
    "{out}/plan.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 4,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [],
    "ops": [
     {
      "key": "changes/000008",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "changes",
      "id": "000008",
      "data": {
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording",
       "parts": [
        {
         "id": "home.lead",
         "from": "c6a82a517ff8",
         "to": "8e7c2ba46ff4"
        }
       ]
      }
     },
     {
      "key": "decisions/lead-tone",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "decisions",
      "id": "lead-tone",
      "data": {
       "text": "Greet, do not instruct.",
       "by": "owner"
      }
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "parts",
      "id": "home.lead",
      "data": {
       "hash": "8e7c2ba46ff4",
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording"
      }
     },
     {
      "key": "manifest/current",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "manifest",
      "id": "current",
      "data": {
       "schema": "adp/2",
       "version": "8",
       "page_hash": "c125279381ff",
       "parts": {
        "home": "f98716c9ddf4",
        "home.lead": "8e7c2ba46ff4"
       }
      }
     }
    ],
    "held": [],
    "counts": {
     "create": 4,
     "replace": 0,
     "skip": 0,
     "hold": 0
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {}
    },
    "order": {
     "last": "manifest/current",
     "rule": "run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current"
    },
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "000008",
         "data": {
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording",
          "parts": [
           {
            "id": "home.lead",
            "from": "c6a82a517ff8",
            "to": "8e7c2ba46ff4"
           }
          ]
         }
        },
        {
         "op": "set",
         "collection": "decisions",
         "doc_id": "lead-tone",
         "data": {
          "text": "Greet, do not instruct.",
          "by": "owner"
         }
        },
        {
         "op": "set",
         "collection": "parts",
         "doc_id": "home.lead",
         "data": {
          "hash": "8e7c2ba46ff4",
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording"
         }
        },
        {
         "op": "set",
         "collection": "manifest",
         "doc_id": "current",
         "data": {
          "schema": "adp/2",
          "version": "8",
          "page_hash": "c125279381ff",
          "parts": {
           "home": "f98716c9ddf4",
           "home.lead": "8e7c2ba46ff4"
          }
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "changes/000008",
       "decisions/lead-tone",
       "parts/home.lead",
       "manifest/current"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{raw}/receipts-ok.json",
    "--host",
    "claude",
    "--raw",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "applied": 4,
    "failed": [],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {
           "changes/000008": {
            "hash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
            "revision": 1
           },
           "decisions/lead-tone": {
            "hash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
            "revision": 1
           },
           "parts/home.lead": {
            "hash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
            "revision": 1
           },
           "manifest/current": {
            "hash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
            "revision": 1
           }
          }
         }
        },
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "d-<ms>",
         "data": {
          "version": "",
          "at": "<time>",
          "by": "agent-a",
          "parts": [],
          "threads": [],
          "summary": "Imported 4 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "data": [
           {
            "doc": "changes/000008"
           },
           {
            "doc": "decisions/lead-tone"
           },
           {
            "doc": "parts/home.lead"
           },
           {
            "doc": "manifest/current"
           },
           {
            "doc": "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
           }
          ]
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
       "changes/d-<ms>"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{raw}/receipts-bad.json",
    "--host",
    "claude",
    "--raw"
   ],
   "exit": 2,
   "stdout": {
    "applied": 0,
    "failed": [
     {
      "key": "changes/000008",
      "outcome": "rejected",
      "error": "db batch write failed: if_version mismatch"
     },
     {
      "key": "decisions/lead-tone",
      "outcome": "rejected",
      "error": "db batch write failed: if_version mismatch"
     },
     {
      "key": "parts/home.lead",
      "outcome": "rejected",
      "error": "db batch write failed: if_version mismatch"
     },
     {
      "key": "manifest/current",
      "outcome": "rejected",
      "error": "db batch write failed: if_version mismatch"
     }
    ],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {}
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{raw}/receipts-unknown.json",
    "--host",
    "claude",
    "--raw"
   ],
   "exit": 2,
   "stdout": {
    "applied": 0,
    "failed": [
     {
      "key": "changes/000008",
      "outcome": "unknown",
      "error": null
     },
     {
      "key": "decisions/lead-tone",
      "outcome": "unknown",
      "error": null
     },
     {
      "key": "parts/home.lead",
      "outcome": "unknown",
      "error": null
     },
     {
      "key": "manifest/current",
      "outcome": "unknown",
      "error": null
     }
    ],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {}
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
      ]
     }
    ]
   }
  }
 ]
}
```

## Contract: moving records (`bundle`, `import-plan`, `import-ack`)

```json fixture
{"fixture": "seed-data", "files": {
 "docs.json": "{\"docs\": [{\"collection\": \"parts\", \"id\": \"home.lead\", \"data\": {\"title\": \"Lead (custom)\"}}, {\"collection\": \"decisions\", \"id\": \"tone\", \"data\": {\"text\": \"Instruct.\"}}, {\"collection\": \"decisions\", \"doc_id\": \"form\", \"file_path\": \"seed-data/form.json\"}]}",
 "form.json": "{\"text\": \"From a file.\"}"}}
```

```json fixture
{"fixture": "seed-dir", "files": {
 "decisions/tone.json": "{\"text\": \"Instruct.\"}",
 "requests/r1/turns/t1.json": "{\"text\": \"Hi\"}",
 "requests~r2~turns__t2.json": "{\"text\": \"Hello\"}"}}
```

```json fixture
{"fixture": "page-empty", "base": "page-a", "files": {"content.js": "window.ADP_CONTENT = {\"home.lead\": {\"title\": \"Lead\", \"html\": \"\"}};"}}
```

```json fixture
{"fixture": "seed-dir-odd", "files": {"a/b/c.json": "{}"}}
```

```json fixture
{"fixture": "seed-dir-bad", "files": {"loose.json": "{}"}}
```

```json fixture
{"fixture": "page-seed-v1", "base": "page-a", "files": {"seed.json": "{\"schema\": \"adp-seed/1\", \"version\": \"2\", \"by\": \"ana\", \"at\": \"2026-01-01T00:00:00Z\", \"docs\": [{\"collection\": \"decisions\", \"id\": \"tone\", \"data\": {\"text\": \"Instruct.\"}}]}"}}
```

```json vector
{
 "vector": "seed-keeps-what-it-was-given",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--by",
    "ana",
    "--version",
    "3",
    "--role",
    "editor",
    "--summary",
    "first",
    "--data",
    "{seed-data}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "seed": "<tmp>/page-a/seed.json",
    "written": true,
    "docs": 10,
    "collections": {
     "decisions": 2,
     "parts": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "packs": [
     "seed/pack-001.json"
    ],
    "bytes": 3138,
    "skipped_empty": [],
    "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
   },
   "files_out": {
    "{page-a}/seed.json": {
     "schema": "adp-seed/2",
     "at": "<time>",
     "version": "3",
     "by": "ana",
     "role": "editor",
     "summary": "first",
     "overrides": [
      {
       "collection": "parts",
       "id": "home.lead",
       "data": {
        "title": "Lead (custom)"
       }
      }
     ],
     "docs": 10,
     "collections": {
      "decisions": 2,
      "parts": 5,
      "changes": 1,
      "agents": 1,
      "manifest": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    },
    "{page-a}/seed/pack-001.json": {
     "schema": "adp-seed/2",
     "pack": 1,
     "of": 1,
     "docs": [
      {
       "collection": "decisions",
       "id": "tone",
       "data": {
        "text": "Instruct."
       }
      },
      {
       "collection": "decisions",
       "id": "form",
       "data": {
        "text": "From a file."
       }
      },
      {
       "collection": "parts",
       "id": "home",
       "data": {
        "title": "home",
        "parent": "",
        "hash": "081b78b8f894",
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "added in the first build",
        "holder": "",
        "hold_until": "",
        "file": "index.html"
       }
      },
      {
       "collection": "parts",
       "id": "home.lead",
       "data": {
        "title": "Lead (custom)",
        "parent": "home",
        "hash": "c6a82a517ff8",
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "added in the first build",
        "holder": "",
        "hold_until": "",
        "file": "index.html"
       }
      },
      {
       "collection": "parts",
       "id": "page.header",
       "data": {
        "title": "page.header",
        "parent": "",
        "hash": "0d957e9aee8d",
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "added in the first build",
        "holder": "",
        "hold_until": "",
        "file": "index.html"
       }
      },
      {
       "collection": "parts",
       "id": "page.script.app",
       "data": {
        "title": "page.script.app",
        "parent": "",
        "hash": "35c146f76e12",
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "added in the first build",
        "holder": "",
        "hold_until": "",
        "file": "parts/app.js"
       }
      },
      {
       "collection": "parts",
       "id": "page.style",
       "data": {
        "title": "page.style",
        "parent": "",
        "hash": "997faceca260",
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "added in the first build",
        "holder": "",
        "hold_until": "",
        "file": "styles/page.css"
       }
      },
      {
       "collection": "changes",
       "id": "000001",
       "data": {
        "version": "3",
        "at": "<time>",
        "by": "ana",
        "summary": "first",
        "parts": [
         {
          "id": "home",
          "from": "",
          "to": "081b78b8f894"
         },
         {
          "id": "home.lead",
          "from": "",
          "to": "c6a82a517ff8"
         },
         {
          "id": "page.header",
          "from": "",
          "to": "0d957e9aee8d"
         },
         {
          "id": "page.script.app",
          "from": "",
          "to": "35c146f76e12"
         },
         {
          "id": "page.style",
          "from": "",
          "to": "997faceca260"
         }
        ],
        "threads": []
       }
      },
      {
       "collection": "agents",
       "id": "ana",
       "data": {
        "role": "editor",
        "session": "",
        "last_seen": "<time>",
        "holds": []
       }
      },
      {
       "collection": "manifest",
       "id": "current",
       "data": {
        "schema": "adp/2",
        "version": "3",
        "page_hash": "7f4556515dd9",
        "parts": {
         "page.header": "0d957e9aee8d",
         "home.lead": "c6a82a517ff8",
         "home": "081b78b8f894",
         "_rest:index.html": "ee2d7cd8fa75",
         "page.script.app": "35c146f76e12",
         "_rest:parts/app.js": "e3b0c44298fc",
         "page.style": "997faceca260",
         "_rest:styles/page.css": "e3b0c44298fc"
        },
        "elements": {
         "page.header": 1,
         "home.lead": 1,
         "home": 1,
         "_rest:index.html": 2,
         "page.script.app": 0,
         "_rest:parts/app.js": 0,
         "page.style": 0,
         "_rest:styles/page.css": 0
        },
        "files": {
         "index.html": "bd002c3d502b",
         "parts/app.js": "574c60bebc47",
         "styles/page.css": "56ee869c6a7b"
        },
        "part_file": {
         "page.header": "index.html",
         "home.lead": "index.html",
         "home": "index.html",
         "_rest:index.html": "index.html",
         "page.script.app": "parts/app.js",
         "_rest:parts/app.js": "parts/app.js",
         "page.style": "styles/page.css",
         "_rest:styles/page.css": "styles/page.css"
        },
        "content": {},
        "at": "<time>",
        "by": "ana"
       }
      }
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}"
   ],
   "exit": 0,
   "stdout": {
    "seed": "<tmp>/page-a/seed.json",
    "written": false,
    "docs": 10,
    "collections": {
     "decisions": 2,
     "parts": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "packs": [
     "seed/pack-001.json"
    ],
    "bytes": 3138,
    "skipped_empty": [],
    "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
   },
   "files_out": {
    "{page-a}/seed.json": {
     "schema": "adp-seed/2",
     "at": "<time>",
     "version": "3",
     "by": "ana",
     "role": "editor",
     "summary": "first",
     "overrides": [
      {
       "collection": "parts",
       "id": "home.lead",
       "data": {
        "title": "Lead (custom)"
       }
      }
     ],
     "docs": 10,
     "collections": {
      "decisions": 2,
      "parts": 5,
      "changes": 1,
      "agents": 1,
      "manifest": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-dir}",
    "--dry-run"
   ],
   "exit": 0,
   "stdout": {
    "collections": {
     "decisions": 2,
     "requests/r2/turns": 1,
     "requests/r1/turns": 1,
     "parts": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "docs": 12,
    "batches": 1,
    "skipped_empty": [],
    "bytes": 2578
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{out}/nothing"
   ],
   "exit": 1,
   "stderr_text": [
    "--data: no file or directory <tmp>/out/nothing"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-dir-bad}"
   ],
   "exit": 1,
   "stderr_text": [
    "--data <tmp>/seed-dir-bad: loose.json is not collection/id.json"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{out}/nothing"
   ],
   "exit": 1,
   "stderr_text": [
    "seed: <tmp>/out/nothing is not a directory (adp.py new makes one)"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-dir-odd}"
   ],
   "exit": 1,
   "stderr_text": [
    "--data <tmp>/seed-dir-odd: a/b/c.json is not collection/id.json"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--version",
    "4",
    "--at",
    "at-given"
   ],
   "exit": 0,
   "files_out": {
    "{page-a}/seed.json": {
     "schema": "adp-seed/2",
     "at": "at-given",
     "version": "4",
     "by": "ana",
     "role": "editor",
     "summary": "first",
     "overrides": [
      {
       "collection": "parts",
       "id": "home.lead",
       "data": {
        "title": "Lead (custom)"
       }
      }
     ],
     "docs": 10,
     "collections": {
      "decisions": 2,
      "parts": 5,
      "changes": 1,
      "agents": 1,
      "manifest": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-empty}",
    "--batches",
    "--out",
    "{out}/e"
   ],
   "exit": 0,
   "stdout": {
    "skipped_empty": [
     "home.lead"
    ],
    "batches": [
     [
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "home",
       "file_path": "<tmp>/out/e/parts__home.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "home.lead",
       "file_path": "<tmp>/out/e/parts__home.lead.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.header",
       "file_path": "<tmp>/out/e/parts__page.header.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.script.app",
       "file_path": "<tmp>/out/e/parts__page.script.app.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.style",
       "file_path": "<tmp>/out/e/parts__page.style.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "000001",
       "file_path": "<tmp>/out/e/changes__000001.json"
      },
      {
       "op": "set",
       "collection": "agents",
       "doc_id": "adp",
       "file_path": "<tmp>/out/e/agents__adp.json"
      },
      {
       "op": "set",
       "collection": "manifest",
       "doc_id": "current",
       "file_path": "<tmp>/out/e/manifest__current.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/out/e"
   }
  }
 ]
}
```

```json vector
{
 "vector": "seed-reads-an-adp-seed-1-and-prints-batches",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-seed-v1}",
    "--batches",
    "--out",
    "{out}/b"
   ],
   "exit": 0,
   "stdout": {
    "batches": [
     [
      {
       "op": "set",
       "collection": "decisions",
       "doc_id": "tone",
       "file_path": "<tmp>/out/b/decisions__tone.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "home",
       "file_path": "<tmp>/out/b/parts__home.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "home.lead",
       "file_path": "<tmp>/out/b/parts__home.lead.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.header",
       "file_path": "<tmp>/out/b/parts__page.header.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.script.app",
       "file_path": "<tmp>/out/b/parts__page.script.app.json"
      },
      {
       "op": "set",
       "collection": "parts",
       "doc_id": "page.style",
       "file_path": "<tmp>/out/b/parts__page.style.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "000001",
       "file_path": "<tmp>/out/b/changes__000001.json"
      },
      {
       "op": "set",
       "collection": "agents",
       "doc_id": "ana",
       "file_path": "<tmp>/out/b/agents__ana.json"
      },
      {
       "op": "set",
       "collection": "manifest",
       "doc_id": "current",
       "file_path": "<tmp>/out/b/manifest__current.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/out/b"
   },
   "files_out": {
    "{out}/b/decisions__tone.json": {
     "text": "Instruct."
    }
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-seed-v1}"
   ],
   "exit": 0,
   "stdout": {
    "seed": "<tmp>/page-seed-v1/seed.json",
    "written": true,
    "docs": 9,
    "collections": {
     "decisions": 1,
     "parts": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "packs": [
     "seed/pack-001.json"
    ],
    "bytes": 3072,
    "skipped_empty": [],
    "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
   },
   "files_out": {
    "{page-seed-v1}/seed.json": {
     "schema": "adp-seed/2",
     "at": "<time>",
     "version": "2",
     "by": "ana",
     "overrides": [],
     "docs": 9,
     "collections": {
      "decisions": 1,
      "parts": 5,
      "changes": 1,
      "agents": 1,
      "manifest": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    }
   }
  }
 ]
}
```

## Contract: `files` after a removal, and a page's kit references

```json fixture
{"fixture": "since", "files": {"doc.json": "{\"id\": \"current\", \"data\": {\"files\": {\"index.html\": \"bd002c3d502b\", \"parts/app.js\": \"574c60bebc47\", \"styles/page.css\": \"56ee869c6a7b\", \"gone.js\": \"aaaaaaaaaaaa\"}}, \"version\": 7}"}}
```

```json fixture
{"fixture": "page-kit", "base": "page-a", "files": {"installed.json": "{\"schema\": \"installed/1\", \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000002\", \"take\": [\"viz.meter\"], \"entries\": [{\"id\": \"kit.badge\"}, {\"id\": \"viz.meter\", \"requires\": [\"kit.badge\"]}]}"}}
```

```json vector
{
 "vector": "files-removals-and-kit-references",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-a}",
    "--since",
    "{since}/doc.json"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-a/index.html",
    "root": "<tmp>/page-a",
    "files": {
     "gone.js": null
    },
    "page_changed": false,
    "note": "index.html is unchanged: publish with url and the changed files, still passing file_path (the tool requires it; the page is re-sent as is)"
   }
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-kit}"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-kit/index.html",
    "root": "<tmp>/page-kit",
    "files": {
     "installed.json": "installed.json",
     "parts/app.js": "parts/app.js",
     "styles/page.css": "styles/page.css"
    },
    "kit_refs": {
     "error": "index not fetched",
     "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "fetch": {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "catalog.json",
      "out_dir": "<tmp>/home/catalog",
      "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
     },
     "next": "adp.py catalog fetches your whole kit (My Own Kit)"
    }
   }
  },
  {
   "copy": [
    "{catalog-built}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-kit}"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-kit/index.html",
    "root": "<tmp>/page-kit",
    "files": {
     "installed.json": "installed.json",
     "parts/app.js": "parts/app.js",
     "styles/page.css": "styles/page.css",
     "kit/badge.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/badge.js"
     },
     "kit/badge.css": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/badge.css"
     },
     "kit/viz/meter.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/viz/meter.js"
     },
     "kit/viz/meter.css": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/viz/meter.css"
     },
     "kit/samples/viz.json": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/samples/viz.json"
     }
    },
    "kit_refs": 5
   }
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-kit}",
    "--batch",
    "3"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-kit/index.html",
    "root": "<tmp>/page-kit",
    "kit_refs": 5,
    "batches": [
     {
      "parts/app.js": "parts/app.js",
      "installed.json": "installed.json",
      "styles/page.css": "styles/page.css"
     },
     {
      "kit/badge.js": {
       "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
       "path": "kit/badge.js"
      },
      "kit/badge.css": {
       "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
       "path": "kit/badge.css"
      },
      "kit/viz/meter.js": {
       "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
       "path": "kit/viz/meter.js"
      }
     },
     {
      "kit/viz/meter.css": {
       "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
       "path": "kit/viz/meter.css"
      },
      "kit/samples/viz.json": {
       "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
       "path": "kit/samples/viz.json"
      }
     }
    ],
    "batch_files": [
     "<tmp>/page-kit.adp/publish-1.json",
     "<tmp>/page-kit.adp/publish-2.json",
     "<tmp>/page-kit.adp/publish-3.json"
    ],
    "note": "8 files: publish the page with batches[0] (new artifact: add capabilities, icon), then each other batch to the same url; every publish passes file_path and root, the tool refuses files without them; note every version id, then adp.py pins"
   }
  }
 ]
}
```

## Contract: refusals of `files --host single` and `unpack`

```json fixture
{"fixture": "page-linked", "base": "page-a", "files": {"link.txt": {"link": "index.html"}}}
```

```json fixture
{"fixture": "page-spaced", "base": "page-a", "files": {"my file.js": "1\n"}}
```

```json fixture
{"fixture": "page-big", "files": {"index.html": "<p>big</p>\n", "big.txt": {"fill": 17000000}}}
```

```json fixture
{"fixture": "pack-bad", "files": {
 "tampered.html": "<script type=\"application/adp-file\" data-adp-file=\"a.txt\" data-type=\"text/plain\" data-enc=\"utf8\" data-sha256=\"0000000000000000000000000000000000000000000000000000000000000000\" data-bytes=\"3\">abc</script>",
 "unsafe.html": "<script type=\"application/adp-file\" data-adp-file=\"../x.txt\" data-type=\"text/plain\" data-enc=\"utf8\" data-sha256=\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\" data-bytes=\"3\">abc</script>",
 "empty.html": "<p>no packed files</p>",
 "other.json": "{\"schema\": \"other\"}",
 "catalog-pack-01.json": "{\"schema\": \"adp-catalog-pack/1\", \"files\": {\"kit/a.js\": \"x\", \"kit/b.css\": \"y\"}}"}}
```

```json vector
{
 "vector": "pack-refusals-and-catalog-pack",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-linked}",
    "--host",
    "single",
    "--out",
    "{out}/x.html"
   ],
   "exit": 1,
   "stderr_text": [
    "files --host single: <tmp>/page-linked/link.txt is a symlink, and symlinks are not packed"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-spaced}",
    "--host",
    "single",
    "--out",
    "{out}/x.html"
   ],
   "exit": 1,
   "stderr_text": [
    "files --host single: my file.js has an unsupported name (use A-Z a-z 0-9 . _ / @ + -)"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-big}",
    "--host",
    "single",
    "--out",
    "{out}/x.html"
   ],
   "exit": 1,
   "stderr_text": [
    "files --host single: the packed page is 17001786 bytes, over the 16 MB page limit"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{out}/empty",
    "--host",
    "single",
    "--out",
    "{out}/x.html"
   ],
   "exit": 1,
   "stderr_text": [
    "files --host single: the folder needs an index.html"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-a}",
    "--host",
    "sites",
    "--out",
    "{out}/x.html"
   ],
   "exit": 1,
   "stderr_text": [
    "files: --host is claude or single, not sites"
   ]
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-bad}/tampered.html",
    "{out}/t"
   ],
   "exit": 1,
   "stderr_text": [
    "unpack: a.txt does not match its sha256"
   ],
   "files_out": {
    "{out}/t/a.txt": null
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-bad}/unsafe.html",
    "{out}/t"
   ],
   "exit": 1,
   "stderr_text": [
    "unpack: unsafe path ../x.txt"
   ],
   "files_out": {
    "{out}/x.txt": null
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-bad}/empty.html",
    "{out}/t"
   ],
   "exit": 1,
   "stderr_text": [
    "unpack: no packed files found"
   ]
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-bad}/other.json",
    "{out}/t"
   ],
   "exit": 1,
   "stderr_text": [
    "unpack: not an ADP pack"
   ]
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-bad}/catalog-pack-01.json",
    "{out}/c"
   ],
   "exit": 0,
   "stdout": {
    "dest": "<tmp>/out/c",
    "files": 2,
    "bytes": 2
   },
   "files_out": {
    "{out}/c/kit/a.js": "x",
    "{out}/c/kit/b.css": "y"
   }
  }
 ]
}
```

## Contract: moving records (`bundle`, `import-plan`, `import-ack`)

```json fixture
{
 "fixture": "move",
 "files": {
  "source.json": "{\n \"docs\": [\n  {\n   \"collection\": \"manifest\",\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"version\": \"8\",\n    \"page_hash\": \"c125279381ff\",\n    \"parts\": {\n     \"home\": \"f98716c9ddf4\",\n     \"home.lead\": \"8e7c2ba46ff4\"\n    }\n   },\n   \"revision\": 9\n  },\n  {\n   \"collection\": \"parts\",\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"8e7c2ba46ff4\",\n    \"version\": \"8\",\n    \"by\": \"agent-a\",\n    \"summary\": \"Lead: wording\"\n   },\n   \"revision\": 4\n  },\n  {\n   \"collection\": \"changes\",\n   \"id\": \"000008\",\n   \"data\": {\n    \"version\": \"8\",\n    \"by\": \"agent-a\",\n    \"summary\": \"Lead: wording\",\n    \"parts\": [\n     {\n      \"id\": \"home.lead\",\n      \"from\": \"c6a82a517ff8\",\n      \"to\": \"8e7c2ba46ff4\"\n     }\n    ]\n   },\n   \"revision\": 1\n  },\n  {\n   \"collection\": \"decisions\",\n   \"id\": \"lead-tone\",\n   \"data\": {\n    \"text\": \"Greet, do not instruct.\",\n    \"by\": \"owner\"\n   },\n   \"revision\": 1\n  },\n  {\n   \"collection\": \"presence\",\n   \"id\": \"agent-a\",\n   \"data\": {\n    \"doing\": \"\"\n   },\n   \"revision\": 12\n  }\n ]\n}\n",
  "target-empty.json": "{\"docs\": []}\n",
  "target-differs.json": "{\n \"docs\": [\n  {\n   \"collection\": \"decisions\",\n   \"id\": \"lead-tone\",\n   \"data\": {\n    \"text\": \"Instruct, briefly.\",\n    \"by\": \"someone\"\n   },\n   \"revision\": 2\n  }\n ]\n}\n",
  "receipts-all.json": "[\n {\n  \"collection\": \"changes\",\n  \"id\": \"000008\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n },\n {\n  \"collection\": \"decisions\",\n  \"id\": \"lead-tone\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n },\n {\n  \"collection\": \"parts\",\n  \"id\": \"home.lead\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n },\n {\n  \"collection\": \"manifest\",\n  \"id\": \"current\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n }\n]\n",
  "receipts-one-rejected.json": "[\n {\n  \"collection\": \"changes\",\n  \"id\": \"000008\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n },\n {\n  \"collection\": \"decisions\",\n  \"id\": \"lead-tone\",\n  \"outcome\": \"rejected\",\n  \"error\": \"if_version mismatch\"\n },\n {\n  \"collection\": \"parts\",\n  \"id\": \"home.lead\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n },\n {\n  \"collection\": \"manifest\",\n  \"id\": \"current\",\n  \"outcome\": \"applied\",\n  \"revision\": 1\n }\n]\n",
  "raw-empty.json": "[]",
  "raw-manifest-only.json": "[\n {\n  \"call\": {\n   \"tool\": \"ArtifactData\",\n   \"collection\": \"manifest\"\n  },\n  \"result\": \"{\\\"id\\\": \\\"current\\\", \\\"data\\\": {\\\"schema\\\": \\\"adp/2\\\", \\\"version\\\": \\\"8\\\", \\\"page_hash\\\": \\\"c125279381ff\\\", \\\"parts\\\": {\\\"home\\\": \\\"f98716c9ddf4\\\", \\\"home.lead\\\": \\\"8e7c2ba46ff4\\\"}}, \\\"version\\\": 9}\"\n }\n]\n"
 }
}
```

```json vector
{
 "vector": "bundle-asks-for-its-reads",
 "run": [
  "adp.py",
  "bundle",
  "--host",
  "claude",
  "--artifact",
  "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a"
 ],
 "exit": 2,
 "stdout": {
  "reads": [
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "manifest",
     "query": {
      "limit": 1000
     }
    },
    "collection": "manifest"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "parts",
     "query": {
      "limit": 1000
     }
    },
    "collection": "parts"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "content",
     "query": {
      "limit": 1000
     }
    },
    "collection": "content"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "changes",
     "query": {
      "limit": 1000
     }
    },
    "collection": "changes"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "decisions",
     "query": {
      "limit": 1000
     }
    },
    "collection": "decisions"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "config",
     "query": {
      "limit": 1000
     }
    },
    "collection": "config"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "agents",
     "query": {
      "limit": 1000
     }
    },
    "collection": "agents"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
     "collection": "incoming",
     "query": {
      "limit": 1000
     }
    },
    "collection": "incoming"
   },
   {
    "tool": "ArtifactData",
    "args": {
     "action": "list",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
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
 "vector": "bundle-refuses-an-incomplete-raw-read",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/raw-manifest-only.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--raw"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/move/raw-manifest-only.json: the read does not cover parts, content, changes, decisions, config, agents, incoming, requests: a bundle from it would silently drop them; read them again"
   ]
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/raw-empty.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--raw"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/move/raw-empty.json: the read is incomplete (no read results): read again before planning"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "move-records-to-an-empty-artifact",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "bundle": "b-38cea1308050",
    "docs": 4,
    "dir": "<tmp>/out/b"
   },
   "files_out": {
    "{out}/b/seed.json": {
     "schema": "adp-seed/2",
     "version": "8",
     "by": "agent-a",
     "at": "<time>",
     "overrides": [],
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     },
     "revisions": {
      "changes/000008": 1,
      "decisions/lead-tone": 1,
      "manifest/current": 9,
      "parts/home.lead": 4
     },
     "docs": 4,
     "collections": {
      "changes": 1,
      "decisions": 1,
      "manifest": 1,
      "parts": 1
     },
     "packs": [
      "seed/pack-001.json"
     ]
    },
    "{out}/b/seed/pack-001.json": {
     "schema": "adp-seed/2",
     "pack": 1,
     "of": 1,
     "docs": [
      {
       "collection": "changes",
       "id": "000008",
       "data": {
        "version": "8",
        "by": "agent-a",
        "summary": "Lead: wording",
        "parts": [
         {
          "id": "home.lead",
          "from": "c6a82a517ff8",
          "to": "8e7c2ba46ff4"
         }
        ]
       }
      },
      {
       "collection": "decisions",
       "id": "lead-tone",
       "data": {
        "text": "Greet, do not instruct.",
        "by": "owner"
       }
      },
      {
       "collection": "manifest",
       "id": "current",
       "data": {
        "schema": "adp/2",
        "version": "8",
        "page_hash": "c125279381ff",
        "parts": {
         "home": "f98716c9ddf4",
         "home.lead": "8e7c2ba46ff4"
        }
       }
      },
      {
       "collection": "parts",
       "id": "home.lead",
       "data": {
        "hash": "8e7c2ba46ff4",
        "version": "8",
        "by": "agent-a",
        "summary": "Lead: wording"
       }
      }
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "changes",
       "query": {
        "limit": 1000
       }
      },
      "collection": "changes"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "decisions",
       "query": {
        "limit": 1000
       }
      },
      "collection": "decisions"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "imports",
       "query": {
        "limit": 1000
       }
      },
      "collection": "imports"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "manifest",
       "query": {
        "limit": 1000
       }
      },
      "collection": "manifest"
     },
     {
      "tool": "ArtifactData",
      "args": {
       "action": "list",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "collection": "parts",
       "query": {
        "limit": 1000
       }
      },
      "collection": "parts"
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--out",
    "{out}/plan.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 4,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [],
    "ops": [
     {
      "key": "changes/000008",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "changes",
      "id": "000008",
      "data": {
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording",
       "parts": [
        {
         "id": "home.lead",
         "from": "c6a82a517ff8",
         "to": "8e7c2ba46ff4"
        }
       ]
      }
     },
     {
      "key": "decisions/lead-tone",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "decisions",
      "id": "lead-tone",
      "data": {
       "text": "Greet, do not instruct.",
       "by": "owner"
      }
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "parts",
      "id": "home.lead",
      "data": {
       "hash": "8e7c2ba46ff4",
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording"
      }
     },
     {
      "key": "manifest/current",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "manifest",
      "id": "current",
      "data": {
       "schema": "adp/2",
       "version": "8",
       "page_hash": "c125279381ff",
       "parts": {
        "home": "f98716c9ddf4",
        "home.lead": "8e7c2ba46ff4"
       }
      }
     }
    ],
    "held": [],
    "counts": {
     "create": 4,
     "replace": 0,
     "skip": 0,
     "hold": 0
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {}
    },
    "order": {
     "last": "manifest/current",
     "rule": "run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current"
    },
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "000008",
         "data": {
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording",
          "parts": [
           {
            "id": "home.lead",
            "from": "c6a82a517ff8",
            "to": "8e7c2ba46ff4"
           }
          ]
         }
        },
        {
         "op": "set",
         "collection": "decisions",
         "doc_id": "lead-tone",
         "data": {
          "text": "Greet, do not instruct.",
          "by": "owner"
         }
        },
        {
         "op": "set",
         "collection": "parts",
         "doc_id": "home.lead",
         "data": {
          "hash": "8e7c2ba46ff4",
          "version": "8",
          "by": "agent-a",
          "summary": "Lead: wording"
         }
        },
        {
         "op": "set",
         "collection": "manifest",
         "doc_id": "current",
         "data": {
          "schema": "adp/2",
          "version": "8",
          "page_hash": "c125279381ff",
          "parts": {
           "home": "f98716c9ddf4",
           "home.lead": "8e7c2ba46ff4"
          }
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "changes/000008",
       "decisions/lead-tone",
       "parts/home.lead",
       "manifest/current"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{move}/receipts-all.json",
    "--host",
    "claude",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "applied": 4,
    "failed": [],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {
           "changes/000008": {
            "hash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
            "revision": 1
           },
           "decisions/lead-tone": {
            "hash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
            "revision": 1
           },
           "parts/home.lead": {
            "hash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
            "revision": 1
           },
           "manifest/current": {
            "hash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
            "revision": 1
           }
          }
         }
        },
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "d-<ms>",
         "data": {
          "version": "",
          "at": "<time>",
          "by": "agent-a",
          "parts": [],
          "threads": [],
          "summary": "Imported 4 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "data": [
           {
            "doc": "changes/000008"
           },
           {
            "doc": "decisions/lead-tone"
           },
           {
            "doc": "parts/home.lead"
           },
           {
            "doc": "manifest/current"
           },
           {
            "doc": "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
           }
          ]
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
       "changes/d-<ms>"
      ]
     }
    ]
   }
  }
 ]
}
```

```json vector
{
 "vector": "move-holds-a-record-the-target-changed",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-differs.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   ],
   "exit": 2,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 4,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "adp"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [],
    "ops": [
     {
      "key": "changes/000008",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "changes",
      "id": "000008",
      "data": {
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording",
       "parts": [
        {
         "id": "home.lead",
         "from": "c6a82a517ff8",
         "to": "8e7c2ba46ff4"
        }
       ]
      }
     },
     {
      "key": "decisions/lead-tone",
      "class": "held",
      "baseHash": null,
      "liveHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": 2,
      "action": "hold",
      "why": "both sides changed, or the target differs and no import was recorded"
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "parts",
      "id": "home.lead",
      "data": {
       "hash": "8e7c2ba46ff4",
       "version": "8",
       "by": "agent-a",
       "summary": "Lead: wording"
      }
     },
     {
      "key": "manifest/current",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
      "action": "create",
      "op": "create",
      "collection": "manifest",
      "id": "current",
      "data": {
       "schema": "adp/2",
       "version": "8",
       "page_hash": "c125279381ff",
       "parts": {
        "home": "f98716c9ddf4",
        "home.lead": "8e7c2ba46ff4"
       }
      }
     }
    ],
    "held": [
     "decisions/lead-tone"
    ],
    "counts": {
     "create": 3,
     "replace": 0,
     "skip": 0,
     "hold": 1
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": null,
     "records": {}
    },
    "order": {
     "last": "manifest/current",
     "rule": "run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current"
    }
   }
  }
 ]
}
```

```json vector
{
 "vector": "move-ack-a-partial-import",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move}/target-empty.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--out",
    "{out}/plan.json"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "{move}/receipts-one-rejected.json",
    "--host",
    "claude",
    "--by",
    "agent-a"
   ],
   "exit": 2,
   "stdout": {
    "applied": 3,
    "failed": [
     {
      "key": "decisions/lead-tone",
      "outcome": "rejected",
      "error": "if_version mismatch"
     }
    ],
    "warnings": [
     "manifest/current was applied while another record failed: the import is partial, do not trust the artifact as synced"
    ],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "adp"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {
           "changes/000008": {
            "hash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
            "revision": 1
           },
           "parts/home.lead": {
            "hash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
            "revision": 1
           },
           "manifest/current": {
            "hash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
            "revision": 1
           }
          }
         }
        },
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "d-<ms>",
         "data": {
          "version": "",
          "at": "<time>",
          "by": "agent-a",
          "summary": "Imported 3 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "parts": [],
          "threads": [],
          "data": [
           {
            "doc": "changes/000008"
           },
           {
            "doc": "parts/home.lead"
           },
           {
            "doc": "manifest/current"
           },
           {
            "doc": "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
           }
          ]
         }
        }
       ]
      },
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
       "changes/d-<ms>"
      ],
      "atomic": true
     }
    ]
   }
  }
 ]
}
```

## Contract: publishing in batches (`files --batch`, `pins`)

```json vector
{
 "vector": "files-in-batches-then-pins",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-a}",
    "--batch",
    "1"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-a/index.html",
    "root": "<tmp>/page-a",
    "batches": [
     {
      "parts/app.js": "parts/app.js"
     },
     {
      "styles/page.css": "styles/page.css"
     }
    ],
    "batch_files": [
     "<tmp>/page-a.adp/publish-1.json",
     "<tmp>/page-a.adp/publish-2.json"
    ],
    "note": "2 files: publish the page with batches[0] (new artifact: add capabilities, icon), then each other batch to the same url; every publish passes file_path and root, the tool refuses files without them; note every version id, then adp.py pins"
   },
   "files_out": {
    "{page-a}.adp/publish-1.json": {
     "parts/app.js": "parts/app.js"
    },
    "{page-a}.adp/publish-2.json": {
     "styles/page.css": "styles/page.css"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "pins",
    "{page-a}.adp/publish-1.json=ver-1",
    "{page-a}.adp/publish-2.json=ver-2"
   ],
   "exit": 0,
   "stdout": {
    "pinned": 2,
    "vermap": "<tmp>/page-a.adp/vermap.json",
    "next": "reference each file in catalog.json at the version <tmp>/page-a.adp/vermap.json gives it, then publish catalog.json to the same url"
   },
   "files_out": {
    "{page-a}.adp/vermap.json": {
     "parts/app.js": "ver-1",
     "styles/page.css": "ver-2"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "pins"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py pins publish-1.json=VERSION_ID ... [--out vermap.json]"
   ]
  }
 ]
}
```

## Contract: the edges of `files`, `unpack`, `seed`, `bundle`, `import-plan` and `import-ack`

```json fixture
{"fixture": "page-tree", "files": {"index.html": "<link rel=\"stylesheet\" href=\"z.css\"><script src=\"a.js\"></script><script src=\"https://x.example/c.js\"></script>\n", "a.js": "1\n", "z.css": "b{}\n", "m.txt": "m\n", "parts/.keep.txt": "k\n", "__pycache__/x.pyc": "x\n", ".git/c": "c\n"}}
```

```json fixture
{"fixture": "page-script-ws", "files": {"index.html": "<script src=\"app.js\">\n</script>\n", "app.js": "1\n"}}
```

```json fixture
{"fixture": "page-script-adj", "files": {"index.html": "<script src=\"app.js\"></script>\n", "app.js": "1\n"}}
```

```json fixture
{"fixture": "pack-edge", "files": {"cat.json": "{\"schema\": \"adp-catalog-pack/1\", \"files\": {\"ok.json\": \"{}\", \"../x\": \"bad\", \"/abs\": \"bad\", \"n.txt\": 5}}", "empty.json": "{\"schema\": \"adp-catalog-pack/1\", \"files\": {}}"}}
```

```json fixture
{"fixture": "page-seed-gap", "base": "page-a", "files": {"seed.json": "{\"schema\": \"adp-seed/2\", \"version\": \"2\", \"by\": \"ana\", \"at\": \"2026-01-01T00:00:00Z\", \"docs\": 3, \"collections\": {}, \"packs\": [\"seed/pack-001.json\"]}"}}
```

```json fixture
{"fixture": "seed-data-bad", "files": {"nodata.json": "[{\"collection\": \"parts\", \"id\": \"x\"}]", "nolist.json": "{\"x\": 1}", "nocoll.json": "[{\"id\": \"a\", \"data\": {}}]"}}
```

```json fixture
{"fixture": "move-absent", "base": "move", "files": {"target-absent.json": "{\"docs\": [{\"collection\": \"imports\", \"id\": \"claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a\", \"exists\": false, \"revision\": 2}, {\"collection\": \"decisions\", \"id\": \"lead-tone\", \"exists\": false, \"revision\": 5}, {\"collection\": \"config\", \"id\": \"current\"}]}"}}
```

```json vector
{
 "vector": "files-and-unpack-edges",
 "steps": [
  {
   "run": [
    "adp.py",
    "files",
    "{page-tree}",
    "--batch",
    "2",
    "--out",
    "{out}/new/dir"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/page-tree/index.html",
    "root": "<tmp>/page-tree",
    "batches": [
     {
      "z.css": "z.css",
      "a.js": "a.js"
     },
     {
      "m.txt": "m.txt",
      "parts/.keep.txt": "parts/.keep.txt"
     }
    ],
    "batch_files": [
     "<tmp>/out/new/dir/publish-1.json",
     "<tmp>/out/new/dir/publish-2.json"
    ],
    "note": "4 files: publish the page with batches[0] (new artifact: add capabilities, icon), then each other batch to the same url; every publish passes file_path and root, the tool refuses files without them; note every version id, then adp.py pins"
   }
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-script-ws}",
    "--host",
    "single",
    "--out",
    "{out}/ws.html"
   ],
   "exit": 0,
   "stdout": {
    "host": "single",
    "out": "<tmp>/out/ws.html",
    "files": 2,
    "bytes": 1844,
    "fragment": false
   }
  },
  {
   "run": [
    "adp.py",
    "files",
    "{page-script-adj}",
    "--host",
    "single",
    "--out",
    "{out}/adj.html"
   ],
   "exit": 0,
   "stdout": {
    "host": "single",
    "out": "<tmp>/out/adj.html",
    "files": 2,
    "bytes": 1844,
    "fragment": false
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-edge}/cat.json",
    "{out}/c"
   ],
   "exit": 0,
   "stdout": {
    "dest": "<tmp>/out/c",
    "files": 1,
    "bytes": 2
   },
   "files_out": {
    "{out}/c/ok.json": {}
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-edge}/empty.json",
    "{out}/e"
   ],
   "exit": 0,
   "stdout": {
    "dest": "<tmp>/out/e",
    "files": 0,
    "bytes": 0
   }
  },
  {
   "run": [
    "adp.py",
    "unpack",
    "{pack-edge}/cat.json"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py unpack PACK DEST"
   ]
  },
  {
   "run": [
    "adp.py",
    "files"
   ],
   "exit": 2,
   "stderr_text": [
    "usage: adp.py files DIR [--since MANIFEST.json] [--batch N] [--out DIR]"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "seed-tolerates-a-missing-pack-and-refuses-bad-data",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-seed-gap}"
   ],
   "exit": 0,
   "stdout": {
    "seed": "<tmp>/page-seed-gap/seed.json",
    "written": true,
    "docs": 8,
    "collections": {
     "parts": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "packs": [
     "seed/pack-001.json"
    ],
    "bytes": 2998,
    "skipped_empty": [],
    "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-data-bad}/nodata.json"
   ],
   "exit": 1,
   "stderr_text": [
    "--data <tmp>/seed-data-bad/nodata.json: a doc needs collection, id and data (an object)"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-data-bad}/nocoll.json"
   ],
   "exit": 1,
   "stderr_text": [
    "--data <tmp>/seed-data-bad/nocoll.json: a doc needs collection, id and data (an object)"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--data",
    "{seed-data-bad}/nolist.json"
   ],
   "exit": 1,
   "stderr_text": [
    "--data <tmp>/seed-data-bad/nolist.json: a list of docs or {docs: [...]}"
   ]
  },
  {
   "run": [
    "adp.py",
    "seed"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py seed DIR [--by NAME] [--version V] [--data FILE|DIR]... [--summary S] [--role R] [--at TIME] [--batches] [--dry-run]"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "move-absent-snapshots-and-option-first-ack",
 "steps": [
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "{out}/b",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
    "--version",
    "8",
    "--by",
    "agent-a"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "{out}/b",
    "{move-absent}/target-absent.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
    "--only",
    "decisions",
    "--out",
    "{out}/plan.json"
   ],
   "exit": 0,
   "stdout": {
    "schema": "adp-import-plan/1",
    "bundle": {
     "id": "b-38cea1308050",
     "schema": "adp-seed/2",
     "docs": 1,
     "source": {
      "id": "b-38cea1308050",
      "host": "claude",
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
      "version": "8",
      "exportedAt": "<time>",
      "by": "agent-a"
     }
    },
    "target": {
     "host": "claude",
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
     "readAt": "<time>"
    },
    "only": [
     "decisions"
    ],
    "ops": [
     {
      "key": "decisions/lead-tone",
      "class": "new",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": 5,
      "action": "create",
      "op": "create",
      "collection": "decisions",
      "id": "lead-tone",
      "data": {
       "text": "Greet, do not instruct.",
       "by": "owner"
      }
     }
    ],
    "held": [],
    "counts": {
     "create": 1,
     "replace": 0,
     "skip": 0,
     "hold": 0
    },
    "provenance": {
     "collection": "imports",
     "id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
     "exists": false,
     "guard": 2,
     "records": {}
    },
    "calls": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "decisions",
         "doc_id": "lead-tone",
         "data": {
          "text": "Greet, do not instruct.",
          "by": "owner"
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "decisions/lead-tone"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "--host",
    "claude",
    "{out}/plan.json",
    "{move}/receipts-all.json"
   ],
   "exit": 0,
   "stdout": {
    "applied": 1,
    "failed": [],
    "warnings": [],
    "record": [
     {
      "tool": "ArtifactData",
      "args": {
       "action": "batch",
       "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
       "writes": [
        {
         "op": "set",
         "collection": "imports",
         "doc_id": "claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
         "data": {
          "schema": "adp-import/1",
          "source": {
           "id": "b-38cea1308050",
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a",
           "version": "8",
           "exportedAt": "<time>",
           "by": "agent-a"
          },
          "bundle": "b-38cea1308050",
          "at": "<time>",
          "target": {
           "host": "claude",
           "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b",
           "readAt": "<time>"
          },
          "records": {
           "decisions/lead-tone": {
            "hash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
            "revision": 1
           }
          },
          "only": [
           "decisions"
          ]
         }
        },
        {
         "op": "set",
         "collection": "changes",
         "doc_id": "d-<ms>",
         "data": {
          "version": "",
          "at": "<time>",
          "by": "adp",
          "parts": [],
          "threads": [],
          "summary": "Imported 1 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "data": [
           {
            "doc": "decisions/lead-tone"
           },
           {
            "doc": "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a"
           }
          ]
         }
        }
       ]
      },
      "atomic": true,
      "keys": [
       "imports/claude-https:-claude.ai-artifact-00000000-0000-4000-8000-00000000000a",
       "changes/d-<ms>"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "import-ack",
    "{out}/plan.json",
    "--host",
    "claude"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py import-ack PLAN.json RECEIPTS.json --host H [--by NAME] [--raw]"
   ]
  },
  {
   "run": [
    "adp.py",
    "import-plan",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000b"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py import-plan BUNDLE [TARGET.json] --host H --artifact DST [--only C,...] [--base BUNDLE] [--out PLAN.json] [--raw]"
   ]
  },
  {
   "run": [
    "adp.py",
    "bundle",
    "{move}/source.json",
    "--host",
    "claude",
    "--artifact",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py bundle [DOCS.json OUT_DIR] --host H --artifact SRC [--version V] [--by NAME] [--collections C,...] [--at TIME] [--raw]"
   ]
  }
 ]
}
```
