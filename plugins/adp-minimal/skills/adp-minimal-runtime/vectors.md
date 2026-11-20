# Vectors: adp-minimal-runtime

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

## Contract: the pure section of `adp.js`

```json vector
{
 "vector": "adp-js-hash-single",
 "run": [
  "adp.js",
  "hash",
  "{one}/page.html"
 ],
 "exit": 0,
 "stdout": {
  "parts": {
   "a.two": "f67648d6310e",
   "a.one": "6193e96bef72",
   "page.script": "aad7378dfeb8",
   "_rest": "67ea429e991b"
  },
  "parents": {
   "a.two": "a.one",
   "a.one": "",
   "page.script": ""
  },
  "page_hash": "0eaae72148c3",
  "bad": []
 }
}
```

```json vector
{
 "vector": "adp-js-hash-shell",
 "run": [
  "adp.js",
  "hash",
  "{page-a}/index.html"
 ],
 "exit": 0,
 "stdout": {
  "parts": {
   "page.header": "0d957e9aee8d",
   "home.lead": "c6a82a517ff8",
   "home": "081b78b8f894",
   "_rest": "ee2d7cd8fa75"
  },
  "parents": {
   "page.header": "",
   "home.lead": "home",
   "home": ""
  },
  "page_hash": "dc667bf14bd1",
  "bad": []
 }
}
```

```json vector
{
 "vector": "adp-js-hash-problems",
 "run": [
  "adp.js",
  "hash",
  "{bad}/twice.html"
 ],
 "exit": 0,
 "stdout": {
  "parts": {
   "x": "696402e55b12",
   "_rest": "696402e55b12"
  },
  "parents": {
   "x": "x"
  },
  "page_hash": "5b3bcc7a6165",
  "bad": [
   "part x opened twice",
   "part x never closed"
  ]
 }
}
```

## Contract: connecting, seeding and switches

```json fixture
{"fixture": "host", "files": {
 "empty.json": "{\"docs\": {}}",
 "seeded.json": "{\"docs\": {\"manifest/current\": {\"schema\": \"adp/2\", \"version\": \"3\"}}}",
 "no-files.json": "{\"docs\": {}, \"seedFiles\": false}",
 "invalid.json": "{\"docs\": {}, \"provider\": \"invalid\"}",
 "locked-log-off.json": "{\"docs\": {\"config/current\": {\"schema\": \"adp-config/1\", \"values\": {\"log.data-changes\": false, \"look.mode\": \"dark\"}, \"changed\": {}}}}"}}
```

```json fixture
{"fixture": "page-a-pack-missing", "base": "page-a", "files": {
 "seed.json": "{\"schema\": \"adp-seed/2\", \"version\": \"1\", \"by\": \"agent-a\", \"docs\": 8, \"packs\": [\"seed/pack-001.json\"]}"}}
```

```json vector
{
 "vector": "runtime-an-editor-seeds-an-empty-record",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--by",
    "agent-a",
    "--version",
    "1"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.js",
    "boot",
    "{page-a}",
    "{host}/empty.json"
   ],
   "exit": 0,
   "stdout": {
    "host": {
     "protocol": "adp-host/1",
     "id": "test",
     "status": "connected",
     "records": true,
     "comments": false,
     "seedFiles": true,
     "agent": false,
     "publish": false,
     "ask": false
    },
    "seeded": {
     "state": "done",
     "from": "seed.json",
     "version": "1",
     "by": "agent-a",
     "opened_by": "agent-a",
     "docs": 8,
     "packs": 1,
     "at": "<time>"
    },
    "writes": [
     "set parts/home",
     "set parts/home.lead",
     "set parts/page.header",
     "set parts/page.script.app",
     "set parts/page.style",
     "set changes/000001",
     "set agents/agent-a",
     "set manifest/current",
     "set status/seed"
    ],
    "docs": [
     "agents/agent-a",
     "changes/000001",
     "manifest/current",
     "parts/home",
     "parts/home.lead",
     "parts/page.header",
     "parts/page.script.app",
     "parts/page.style",
     "status/seed"
    ]
   }
  }
 ]
}
```

```json vector
{
 "vector": "runtime-a-viewer-seeds-nothing",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--by",
    "agent-a",
    "--version",
    "1"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.js",
    "boot",
    "{page-a}",
    "{host}/empty.json",
    "viewer"
   ],
   "exit": 0,
   "stdout": {
    "host": {
     "protocol": "adp-host/1",
     "id": "test",
     "status": "connected",
     "records": true,
     "comments": false,
     "seedFiles": true,
     "agent": false,
     "publish": false,
     "ask": false
    },
    "seeded": null,
    "writes": [],
    "docs": []
   }
  }
 ]
}
```

```json vector
{
 "vector": "runtime-a-written-record-is-not-seeded-again",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--by",
    "agent-a",
    "--version",
    "1"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.js",
    "boot",
    "{page-a}",
    "{host}/seeded.json"
   ],
   "exit": 0,
   "stdout": {
    "host": {
     "protocol": "adp-host/1",
     "id": "test",
     "status": "connected",
     "records": true,
     "comments": false,
     "seedFiles": true,
     "agent": false,
     "publish": false,
     "ask": false
    },
    "seeded": null,
    "writes": [],
    "docs": [
     "manifest/current"
    ]
   }
  }
 ]
}
```

```json vector
{
 "vector": "runtime-a-host-without-files-seeds-nothing",
 "steps": [
  {
   "run": [
    "adp.py",
    "seed",
    "{page-a}",
    "--by",
    "agent-a",
    "--version",
    "1"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.js",
    "boot",
    "{page-a}",
    "{host}/no-files.json"
   ],
   "exit": 0,
   "stdout": {
    "host": {
     "protocol": "adp-host/1",
     "id": "test",
     "status": "connected",
     "records": true,
     "comments": false,
     "seedFiles": false,
     "agent": false,
     "publish": false,
     "ask": false
    },
    "seeded": null,
    "writes": [],
    "docs": []
   }
  }
 ]
}
```

```json vector
{
 "vector": "runtime-a-missing-pack-writes-nothing",
 "run": [
  "adp.js",
  "boot",
  "{page-a-pack-missing}",
  "{host}/empty.json"
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "writes": [],
  "docs": []
 }
}
```

```json vector
{
 "vector": "runtime-an-invalid-provider-fails-closed",
 "run": [
  "adp.js",
  "boot",
  "{page-a}",
  "{host}/invalid.json"
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "",
   "status": "failed"
  },
  "seeded": null,
  "writes": [],
  "docs": []
 }
}
```

```json vector
{
 "vector": "runtime-config-set",
 "run": [
  "adp.js",
  "config-set",
  "{page-a}",
  "{host}/seeded.json",
  "look.mode",
  "\"dark\""
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "result": "ok",
  "value": "dark",
  "writes": [
   "set config/current",
   "set changes/d-<ms>"
  ],
  "config": {
   "schema": "adp-config/1",
   "at": "<time>",
   "by": "agent-a",
   "values": {
    "look.mode": "dark"
   },
   "changed": {
    "look.mode": {
     "by": "agent-a",
     "at": "<time>"
    }
   }
  },
  "changes": [
   {
    "version": "",
    "at": "<time>",
    "by": "agent-a",
    "summary": "Set look.mode = \"dark\"",
    "parts": [],
    "threads": [],
    "data": [
     {
      "doc": "config/current"
     }
    ]
   }
  ]
 }
}
```

```json vector
{
 "vector": "runtime-config-set-the-default-removes-it",
 "run": [
  "adp.js",
  "config-set",
  "{page-a}",
  "{host}/locked-log-off.json",
  "look.mode",
  "\"auto\""
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "result": "ok",
  "value": "auto",
  "writes": [
   "set config/current"
  ],
  "config": {
   "schema": "adp-config/1",
   "at": "<time>",
   "by": "agent-a",
   "values": {
    "log.data-changes": false
   },
   "changed": {
    "look.mode": {
     "by": "agent-a",
     "at": "<time>"
    }
   }
  },
  "changes": []
 }
}
```

```json vector
{
 "vector": "runtime-config-set-a-wrong-value",
 "run": [
  "adp.js",
  "config-set",
  "{page-a}",
  "{host}/seeded.json",
  "look.mode",
  "\"purple\""
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "result": "error: look.mode needs one of auto, light, dark",
  "value": "auto",
  "writes": [],
  "config": null,
  "changes": []
 }
}
```

```json vector
{
 "vector": "runtime-config-set-an-unknown-switch",
 "run": [
  "adp.js",
  "config-set",
  "{page-a}",
  "{host}/seeded.json",
  "look.nope",
  "1"
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "result": "error: Unknown setting look.nope",
  "writes": [],
  "config": null,
  "changes": []
 }
}
```

```json vector
{
 "vector": "runtime-config-set-by-a-viewer",
 "run": [
  "adp.js",
  "config-set",
  "{page-a}",
  "{host}/seeded.json",
  "look.mode",
  "\"dark\"",
  "viewer"
 ],
 "exit": 0,
 "stdout": {
  "host": {
   "protocol": "adp-host/1",
   "id": "test",
   "status": "connected",
   "records": true,
   "comments": false,
   "seedFiles": true,
   "agent": false,
   "publish": false,
   "ask": false
  },
  "seeded": null,
  "result": "error: Settings cannot be saved: you cannot edit this artifact.",
  "value": "auto",
  "writes": [],
  "config": null,
  "changes": []
 }
}
```
