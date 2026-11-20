# Vectors: adp-minimal-packing

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

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
    "adp.py unpack: Destination is not empty: <tmp>/page-a2"
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
  "bytes": 3086,
  "skipped_empty": [],
  "next": "publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database"
 },
 "files_out": {
  "{page-a}/seed.json": {
   "schema": "adp-seed/2",
   "version": "1",
   "by": "agent-a",
   "at": "<time>",
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
   "overrides": []
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
       "_rest:index.html": "ee2d7cd8fa75",
       "_rest:parts/app.js": "e3b0c44298fc",
       "_rest:styles/page.css": "e3b0c44298fc",
       "home": "081b78b8f894",
       "home.lead": "c6a82a517ff8",
       "page.header": "0d957e9aee8d",
       "page.script.app": "35c146f76e12",
       "page.style": "997faceca260"
      },
      "elements": {
       "_rest:index.html": 2,
       "_rest:parts/app.js": 0,
       "_rest:styles/page.css": 0,
       "home": 1,
       "home.lead": 1,
       "page.header": 1,
       "page.script.app": 0,
       "page.style": 0
      },
      "files": {
       "index.html": "bd002c3d502b",
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
     }
    }
   ]
  }
 }
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
  "the read does not cover parts, content, changes, decisions, config, agents, incoming, requests: a bundle from it would silently drop them; read them again"
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
     "docs": 4,
     "collections": {
      "changes": 1,
      "decisions": 1,
      "manifest": 1,
      "parts": 1
     },
     "packs": [
      "seed/pack-001.json"
     ],
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
     }
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": null,
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
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
     "guard": null,
     "exists": false,
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
      "keys": [
       "changes/000008",
       "decisions/lead-tone",
       "parts/home.lead",
       "manifest/current"
      ],
      "atomic": true
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
          "summary": "Imported 4 records from claude:https://claude.ai/artifact/00000000-0000-4000-8000-00000000000a (bundle b-38cea1308050)",
          "parts": [],
          "threads": [],
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:986feea4c7e5d4e9e580e7f574a23a75f0d53a823620dcda9e1bb5bb1b4b173a",
      "guard": null,
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
      "action": "hold",
      "baseHash": null,
      "liveHash": "sha256:a91136edf9d534db55b8978caa3e79cb53249e7263b3c582c315bd56b16920a7",
      "incomingHash": "sha256:0d4e6c46b46c6bc7b8b7752646737dffc1c35759886f102e3f312f4a9a8a020b",
      "guard": 2,
      "why": "both sides changed, or the target differs and no import was recorded"
     },
     {
      "key": "parts/home.lead",
      "class": "new",
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:8d9f211de076f89b72ce509d679de3c1f75a41661d2dca5ceb325765f244f069",
      "guard": null,
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
      "action": "create",
      "baseHash": null,
      "liveHash": null,
      "incomingHash": "sha256:ef2b4b7d35a46b03f277193198f57141e8515fd4a22c375226f000cdee6fd635",
      "guard": null,
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
     "guard": null,
     "exists": false,
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
    "next": "CAT_URL=<url> CAT_VERMAP=<tmp>/page-a.adp/vermap.json make catalog, then publish catalog.json to the same url"
   },
   "files_out": {
    "{page-a}.adp/vermap.json": {
     "parts/app.js": "ver-1",
     "styles/page.css": "ver-2"
    }
   }
  }
 ]
}
```
