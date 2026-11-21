# Vectors: adp-minimal-runtime

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are run against the tools assembled from the fragments.

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

```json fixture
{"fixture": "seed-inline", "files": {
 "seed.json": "{\"schema\": \"adp-seed/1\", \"version\": \"2\", \"by\": \"agent-b\", \"docs\": [{\"collection\": \"c\", \"id\": \"01\", \"data\": {\"n\": 1}}, {\"collection\": \"c\", \"id\": \"02\", \"data\": {\"n\": 2}}, {\"collection\": \"c\", \"id\": \"03\", \"data\": {\"n\": 3}}, {\"collection\": \"c\", \"id\": \"04\", \"data\": {\"n\": 4}}, {\"collection\": \"c\", \"id\": \"05\", \"data\": {\"n\": 5}}, {\"collection\": \"c\", \"id\": \"06\", \"data\": {\"n\": 6}}, {\"collection\": \"c\", \"id\": \"07\", \"data\": {\"n\": 7}}, {\"collection\": \"c\", \"id\": \"08\", \"data\": {\"n\": 8}}, {\"collection\": \"c\", \"id\": \"09\", \"data\": {\"n\": 9}}, {\"collection\": \"c\", \"id\": \"10\", \"data\": {\"n\": 10}}, {\"collection\": \"c\", \"id\": \"11\", \"data\": {\"n\": 11}}, {\"collection\": \"c\", \"id\": \"12\", \"data\": {\"n\": 12}}, {\"collection\": \"c\", \"id\": \"13\", \"data\": {\"n\": 13}}, {\"collection\": \"c\", \"id\": \"14\", \"data\": {\"n\": 14}}, {\"collection\": \"c\", \"id\": \"15\", \"data\": {\"n\": 15}}, {\"collection\": \"c\", \"id\": \"16\", \"data\": {\"n\": 16}}, {\"collection\": \"c\", \"id\": \"17\", \"data\": {\"n\": 17}}, {\"collection\": \"c\", \"id\": \"18\", \"data\": {\"n\": 18}}, {\"collection\": \"c\", \"id\": \"19\", \"data\": {\"n\": 19}}, {\"collection\": \"c\", \"id\": \"20\", \"data\": {\"n\": 20}}, {\"collection\": \"c\", \"id\": \"21\", \"data\": {\"n\": 21}}, {\"collection\": \"c\", \"id\": \"22\", \"data\": {\"n\": 22}}, {\"collection\": \"c\", \"id\": \"23\", \"data\": {\"n\": 23}}, {\"collection\": \"c\", \"id\": \"24\", \"data\": {\"n\": 24}}, {\"collection\": \"c\", \"id\": \"25\", \"data\": {\"n\": 25}}, {\"collection\": \"manifest\", \"id\": \"current\", \"data\": {\"schema\": \"adp/2\"}}]}"}}
```

```json fixture
{"fixture": "seed-unknown", "files": {
 "seed.json": "{\"schema\": \"adp-seed/9\", \"docs\": [{\"collection\": \"c\", \"id\": \"01\", \"data\": {\"n\": 1}}]}"}}
```

An inline `adp-seed/1` seed of 26 documents is written six at a time with a progress record after the 25th, `manifest/current` last; a
`seed.json` of an unknown schema writes nothing.

```json vector
{
 "vector": "runtime-seed-inline-and-unknown",
 "steps": [
  {
   "run": [
    "adp.js",
    "boot",
    "{seed-inline}",
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
     "version": "2",
     "by": "agent-b",
     "opened_by": "agent-a",
     "docs": 26,
     "packs": 0,
     "at": "<time>"
    },
    "writes": [
     "set c/01",
     "set c/02",
     "set c/03",
     "set c/04",
     "set c/05",
     "set c/06",
     "set c/07",
     "set c/08",
     "set c/09",
     "set c/10",
     "set c/11",
     "set c/12",
     "set c/13",
     "set c/14",
     "set c/15",
     "set c/16",
     "set c/17",
     "set c/18",
     "set c/19",
     "set c/20",
     "set c/21",
     "set c/22",
     "set c/23",
     "set c/24",
     "set c/25",
     "set status/seed",
     "set manifest/current",
     "set status/seed"
    ],
    "docs": [
     "c/01",
     "c/02",
     "c/03",
     "c/04",
     "c/05",
     "c/06",
     "c/07",
     "c/08",
     "c/09",
     "c/10",
     "c/11",
     "c/12",
     "c/13",
     "c/14",
     "c/15",
     "c/16",
     "c/17",
     "c/18",
     "c/19",
     "c/20",
     "c/21",
     "c/22",
     "c/23",
     "c/24",
     "c/25",
     "manifest/current",
     "status/seed"
    ]
   }
  },
  {
   "run": [
    "adp.js",
    "boot",
    "{seed-unknown}",
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
 ]
}
```

A page script may register a switch with no description at all (`{x: null}`): it is a text switch whose default is empty.

```json vector
{
 "vector": "runtime-config-define-a-bare-switch",
 "run": [
  "adp.js",
  "config-define",
  "g",
  "{\"x\": null}"
 ],
 "exit": 0,
 "stdout": {
  "x": {
   "group": "g",
   "name": "x",
   "type": "text",
   "level": "page",
   "default": "",
   "value": "",
   "changed": null
  }
 }
}
```

Each switch type refuses a wrong value, a list of strings is accepted, and a page without a database refuses every write.

```json vector
{
 "vector": "runtime-config-set-checks-each-type",
 "steps": [
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "edit.locked",
    "\"yes\""
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
    "result": "error: edit.locked needs a bool value",
    "value": false,
    "writes": [],
    "config": null,
    "changes": []
   }
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "parts.locked",
    "[\"home\", 1]"
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
    "result": "error: parts.locked needs a list value",
    "value": [],
    "writes": [],
    "config": null,
    "changes": []
   }
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "parts.locked",
    "[\"home\"]"
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
    "value": [
     "home"
    ],
    "writes": [
     "set config/current",
     "set changes/d-<ms>"
    ],
    "config": {
     "schema": "adp-config/1",
     "at": "<time>",
     "by": "agent-a",
     "values": {
      "parts.locked": [
       "home"
      ]
     },
     "changed": {
      "parts.locked": {
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
      "summary": "Set parts.locked = [\"home\"]",
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
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "links.catalog",
    "\"http://example.com\""
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
    "result": "error: links.catalog needs an https:// address or empty",
    "value": "",
    "writes": [],
    "config": null,
    "changes": []
   }
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "edit.until",
    "\"soon\""
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
    "result": "error: edit.until needs a datetime value",
    "value": "",
    "writes": [],
    "config": null,
    "changes": []
   }
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/seeded.json",
    "edit.reason",
    "7"
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
    "result": "error: edit.reason needs text up to 2000 characters",
    "value": "",
    "writes": [],
    "config": null,
    "changes": []
   }
  },
  {
   "run": [
    "adp.js",
    "config-set",
    "{page-a}",
    "{host}/invalid.json",
    "look.mode",
    "\"dark\""
   ],
   "exit": 0,
   "stdout": {
    "host": {
     "protocol": "adp-host/1",
     "id": "",
     "status": "failed"
    },
    "seeded": null,
    "result": "error: Settings cannot be saved here: this page has no database.",
    "value": "auto",
    "writes": [],
    "config": null,
    "changes": []
   }
  }
 ]
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
