# Vectors: adp-delta

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-rebuild](../adp-rebuild/SKILL.md) reads them.

## Contract: `classify`, in `adp.py` and `adp.js`

```json fixture
{"fixture": "three", "files": {
 "base.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"000000000002\", \"theirs\": \"000000000003\", \"both\": \"000000000004\", \"agree\": \"000000000005\", \"old\": \"000000000006\", \"dropped\": \"000000000007\", \"p\": \"000000000008\", \"p.c\": \"000000000009\"}, \"files\": {\"index.html\": \"aaaaaaaaaaaa\"}, \"parents\": {\"p.c\": \"p\"}}",
 "live.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"000000000002\", \"theirs\": \"00000000000c\", \"both\": \"00000000000d\", \"agree\": \"00000000000e\", \"old\": \"000000000006\", \"dropped\": \"000000000007\", \"p\": \"000000000008\", \"p.c\": \"00000000000f\", \"livenew\": \"000000000010\"}, \"files\": {\"index.html\": \"aaaaaaaaaaaa\"}, \"parents\": {\"p.c\": \"p\"}}",
 "incoming.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"00000000001b\", \"theirs\": \"000000000003\", \"both\": \"00000000001d\", \"agree\": \"00000000000e\", \"p\": \"000000000018\", \"p.c\": \"000000000019\", \"fresh\": \"000000000020\"}, \"files\": {\"index.html\": \"bbbbbbbbbbbb\"}, \"parents\": {\"p.c\": \"p\"}, \"retired\": {\"old\": \"replaced by fresh\"}}"}}
```

The ids in the `three` fixture cover every class. `same` is unchanged on every side, so it appears in no class. `mine` and the file
`index.html` are `ours`; `theirs`, and `livenew` (present only in live), are `theirs`; `agree` is `applied`, since live and incoming reach the same
hash; `fresh` is `new`; `old` is `retired`, deleted with a reason. `both` is `held` because each side changed it differently, and `dropped` is `held`
because incoming deletes it without a reason. `p.c` is `held` for the same reason as `both`; its parent `p` would be `ours`, and the closure holds it.

```json vector
{
 "vector": "classify-every-class",
 "run": [
  "adp.py",
  "classify",
  "{three}/base.json",
  "{three}/live.json",
  "{three}/incoming.json"
 ],
 "exit": 0,
 "stdout": {
  "new": [
   "fresh"
  ],
  "ours": [
   "index.html",
   "mine"
  ],
  "theirs": [
   "livenew",
   "theirs"
  ],
  "applied": [
   "agree"
  ],
  "held": [
   {
    "id": "both",
    "base": "000000000004",
    "live": "00000000000d",
    "incoming": "00000000001d"
   },
   {
    "id": "dropped",
    "base": "000000000007",
    "live": "000000000007",
    "incoming": null
   },
   {
    "id": "p",
    "base": "000000000008",
    "live": "000000000008",
    "incoming": "000000000018"
   },
   {
    "id": "p.c",
    "base": "000000000009",
    "live": "00000000000f",
    "incoming": "000000000019"
   }
  ],
  "retired": [
   "old"
  ]
 }
}
```

```json vector
{
 "vector": "classify-in-adp-js",
 "run": [
  "adp.js",
  "classify",
  "{three}/base.json",
  "{three}/live.json",
  "{three}/incoming.json"
 ],
 "exit": 0,
 "stdout": {
  "new": [
   "fresh"
  ],
  "ours": [
   "index.html",
   "mine"
  ],
  "theirs": [
   "livenew",
   "theirs"
  ],
  "applied": [
   "agree"
  ],
  "held": [
   {
    "id": "both",
    "base": "000000000004",
    "live": "00000000000d",
    "incoming": "00000000001d"
   },
   {
    "id": "dropped",
    "base": "000000000007",
    "live": "000000000007",
    "incoming": null
   },
   {
    "id": "p",
    "base": "000000000008",
    "live": "000000000008",
    "incoming": "000000000018"
   },
   {
    "id": "p.c",
    "base": "000000000009",
    "live": "00000000000f",
    "incoming": "000000000019"
   }
  ],
  "retired": [
   "old"
  ]
 }
}
```

## Contract: the loop (export, propose, ack, gate)

```json fixture
{
 "fixture": "loop",
 "files": {
  "work/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "work.adp/incoming/files/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "work/parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "work.adp/incoming/files/parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "work/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n",
  "work.adp/incoming/files/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n",
  "live-8/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hello</p><!-- /part:home.lead --><p>new, unmarked</p></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "live-8/parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "live-8/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n",
  "mine/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Howdy</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "mine/parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "mine/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n",
  "listing.json": "{\n \"files\": [\n  {\n   \"path\": \"index.html\",\n   \"sha256\": \"bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3\",\n   \"bytes\": 336\n  },\n  {\n   \"path\": \"parts/app.js\",\n   \"sha256\": \"574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df\",\n   \"bytes\": 71\n  },\n  {\n   \"path\": \"styles/page.css\",\n   \"sha256\": \"56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc\",\n   \"bytes\": 64\n  }\n ]\n}\n",
  "listing-8.json": "{\n \"files\": [\n  {\n   \"path\": \"index.html\",\n   \"sha256\": \"a56efc30baaf2b0092ef447bc5c901d1f809d2f64b4052f2d65dfb69c7b56694\",\n   \"bytes\": 359\n  },\n  {\n   \"path\": \"parts/app.js\",\n   \"sha256\": \"574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df\",\n   \"bytes\": 71\n  },\n  {\n   \"path\": \"styles/page.css\",\n   \"sha256\": \"56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc\",\n   \"bytes\": 64\n  }\n ]\n}\n",
  "docs.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ]\n}\n",
  "docs-8.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"c125279381ff\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"f98716c9ddf4\",\n     \"home.lead\": \"8e7c2ba46ff4\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"a56efc30baaf\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 2,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"8\"\n   },\n   \"version\": 9\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"f98716c9ddf4\"\n   },\n   \"version\": 3\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"8e7c2ba46ff4\"\n   },\n   \"version\": 4\n  }\n ]\n}\n",
  "hook-pinned.json": "{\"tool_name\": \"mcp__claude_ai__ArtifactData\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"action\": \"batch\", \"writes\": [{\"op\": \"update\", \"collection\": \"parts\", \"doc_id\": \"home\", \"if_version\": 2}]}}\n",
  "hook-stale.json": "{\"tool_name\": \"mcp__claude_ai__ArtifactData\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"action\": \"batch\", \"writes\": [{\"op\": \"update\", \"collection\": \"parts\", \"doc_id\": \"home\", \"if_version\": 1}]}}\n",
  "hook-answer.json": "{\"tool_name\": \"mcp__claude_ai__ArtifactData\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"action\": \"batch\", \"writes\": [{\"op\": \"update\", \"collection\": \"requests\", \"doc_id\": \"r-1\"}]}}\n",
  "hook-unmanaged.json": "{\"tool_name\": \"Artifact\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-0000000000ff\", \"action\": \"publish\"}}\n",
  "written.json": "{\"results\": [{\"collection\": \"parts\", \"doc_id\": \"home\", \"version\": 5}, {\"collection\": \"parts\", \"doc_id\": \"home.lead\", \"version\": 6}]}\n"
 }
}
```

```json vector
{
 "vector": "loop-export-asks-for-its-reads",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "Artifact",
      "action": "list",
      "scope": "files",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "save_to": "<tmp>/loop/work.adp/listing.json",
      "save": "the result as the tool returned it, text or JSON"
     }
    ],
    "then": "adp.py export <tmp>/loop/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 --files-listing <tmp>/loop/work.adp/listing.json"
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json"
   ],
   "exit": 2,
   "stdout": {
    "reads": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "paths": [
       "index.html",
       "parts/app.js",
       "styles/page.css"
      ],
      "out_dir": "<tmp>/loop/work.adp/incoming/files"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "manifest"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "parts"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "content"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "changes"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "config"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "requests"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "presence"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "agents"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "decisions"
     },
     {
      "tool": "ArtifactData",
      "action": "list",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
      "collection": "incoming"
     }
    ],
    "save_docs_to": "<tmp>/loop/work.adp/docs.json",
    "docs_shape": "{collection: [{id, data, version}, ...]}",
    "then": "adp.py export <tmp>/loop/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 --files-listing <tmp>/loop/listing.json --docs <tmp>/loop/work.adp/docs.json"
   }
  }
 ]
}
```

```json vector
{
 "vector": "loop-the-first-export-is-the-import",
 "run": [
  "adp.py",
  "export",
  "{loop}/work",
  "--url",
  "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
  "--files-listing",
  "{loop}/listing.json",
  "--docs",
  "{loop}/docs.json"
 ],
 "exit": 0,
 "stdout": {
  "report": {
   "new": [],
   "ours": [],
   "theirs": [],
   "applied": [],
   "held": [],
   "retired": []
  },
  "merged": true,
  "state": "<tmp>/loop/work.adp/state.json",
  "next": "clean: nothing to send"
 },
 "files_out": {
  "{loop}/home/artifacts.json": null
 }
}
```

```json vector
{
 "vector": "loop-ours-is-proposed-and-acknowledged",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{loop}/mine",
    "{loop}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [
      "home",
      "home.lead",
      "index.html"
     ],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "adp.py propose <tmp>/loop/work --by NAME --summary S"
   }
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{loop}/work",
    "--by",
    "agent-a",
    "--summary",
    "Lead: greeting"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/loop/work.adp/propose-<pid>.json",
    "parts": 2,
    "files": 1,
    "chunks": 0,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/loop/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/loop/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/loop/work.adp/propose-<pid>"
   },
   "files_out": {
    "{loop}/work.adp/propose-*.json": {
     "by": "agent-a",
     "at": "<time>",
     "summary": "Lead: greeting",
     "threads": [],
     "base": {
      "version": "7",
      "page_hash": "7f4556515dd9",
      "docs": {
       "manifest/current": 7,
       "parts/home": 2,
       "parts/home.lead": 3
      }
     },
     "parts": [
      {
       "id": "home",
       "from": "081b78b8f894",
       "to": "321732a04e94",
       "html": "",
       "retired": false,
       "reason": ""
      },
      {
       "id": "home.lead",
       "from": "c6a82a517ff8",
       "to": "31d186af845c",
       "html": "",
       "retired": false,
       "reason": ""
      }
     ],
     "files": [
      {
       "path": "index.html",
       "ifMatch": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
       "contentType": "text/html",
       "content": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Howdy</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"
      }
     ],
     "live_files": {
      "index.html": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
      "parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
      "styles/page.css": "56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc"
     },
     "classified": {
      "new": [],
      "ours": [
       "home",
       "home.lead",
       "index.html"
      ],
      "theirs": [],
      "applied": [],
      "held": [],
      "retired": []
     },
     "status": "new",
     "decided": {
      "by": "",
      "at": "",
      "reason": ""
     },
     "applied": {
      "version": "",
      "at": ""
     }
    }
   }
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-pinned.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "additionalContext": "adp: inbox clear"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{loop}/work",
    "--result",
    "{loop}/written.json"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "parts/home",
     "parts/home.lead"
    ],
    "live": {
     "at": "<time>",
     "version": "7"
    },
    "incoming": {
     "held": [],
     "unacked": [],
     "pending_replies": []
    }
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{loop}/work",
    "--proposal",
    "p-1000000000000-abcd"
   ],
   "exit": 1,
   "stderr_text": [
    "<pid>: status unknown in the last export read; ack it once applied or declined"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "loop-propose-before-any-export",
 "run": [
  "adp.py",
  "propose",
  "{loop}/work",
  "--by",
  "agent-a",
  "--summary",
  "x"
 ],
 "exit": 2,
 "stdout": {
  "error": "no export yet",
  "next": "adp.py export <tmp>/loop/work --url URL"
 }
}
```

```json vector
{
 "vector": "loop-propose-with-nothing-changed",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{loop}/work",
    "--by",
    "agent-a",
    "--summary",
    "x"
   ],
   "exit": 0,
   "stdout": {
    "nothing": "work equals live",
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    }
   }
  }
 ]
}
```

```json vector
{
 "vector": "loop-theirs-lands-in-the-folder",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{loop}/live-8",
    "{loop}/work.adp/incoming/files"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing-8.json",
    "--docs",
    "{loop}/docs-8.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [
      "home",
      "home.lead",
      "index.html"
     ],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  },
  {
   "same_tree": [
    "{loop}/live-8",
    "{loop}/work"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "loop-both-sides-changed-is-held",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{loop}/mine",
    "{loop}/work"
   ]
  },
  {
   "copy": [
    "{loop}/live-8",
    "{loop}/work.adp/incoming/files"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing-8.json",
    "--docs",
    "{loop}/docs-8.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [
      {
       "id": "home",
       "base": "081b78b8f894",
       "live": "f98716c9ddf4",
       "incoming": "321732a04e94"
      },
      {
       "id": "home.lead",
       "base": "c6a82a517ff8",
       "live": "8e7c2ba46ff4",
       "incoming": "31d186af845c"
      },
      {
       "id": "index.html",
       "base": "bd002c3d502b",
       "live": "a56efc30baaf",
       "incoming": "ad5fdf7d9aeb"
      }
     ],
     "retired": []
    },
    "merged": false,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "held: 3; show both versions to the owner, nobody writes"
   }
  },
  {
   "same_tree": [
    "{loop}/mine",
    "{loop}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{loop}/work",
    "--by",
    "agent-a",
    "--summary",
    "x"
   ],
   "exit": 2,
   "stdout": {
    "refused": [
     {
      "error": "merge conflict with live",
      "detail": [
       "CONFLICT (content): Merge conflict in db/parts/home.json",
       "CONFLICT (content): Merge conflict in db/parts/home.lead.json",
       "CONFLICT (content): Merge conflict in files/index.html"
      ]
     },
     {
      "error": "held",
      "held": [
       {
        "id": "home",
        "base": "081b78b8f894",
        "live": "f98716c9ddf4",
        "incoming": "321732a04e94"
       },
       {
        "id": "home.lead",
        "base": "c6a82a517ff8",
        "live": "8e7c2ba46ff4",
        "incoming": "31d186af845c"
       },
       {
        "id": "index.html",
        "base": "bd002c3d502b",
        "live": "a56efc30baaf",
        "incoming": "ad5fdf7d9aeb"
       }
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-pinned.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "permissionDecision": "deny",
     "permissionDecisionReason": "adp: the inbox has held: home, home.lead, index.html. Run adp.py export <tmp>/loop/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 and resolve them first"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-answer.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "permissionDecision": "deny",
     "permissionDecisionReason": "adp: the inbox has held: home, home.lead, index.html. Run adp.py export <tmp>/loop/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 and resolve them first"
    }
   }
  }
 ]
}
```

```json vector
{
 "vector": "loop-gate-decisions",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-pinned.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "additionalContext": "adp: inbox clear"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-stale.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "permissionDecision": "deny",
     "permissionDecisionReason": "adp: a batch not derived from the last export: parts/home pinned at 1, read at 2. Re-export, then rebuild it"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{loop}/hook-unmanaged.json"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "additionalContext": "adp: no state for this url, an artifact ADP does not manage"
    }
   }
  }
 ]
}
```

```json fixture
{
 "fixture": "refusals",
 "base": "loop",
 "files": {
  "listing.txt": "no rows here\n"
 }
}
```

```json vector
{
 "vector": "loop-refusals",
 "steps": [
  {
   "run": [
    "adp.py",
    "classify",
    "{refusals}/listing.txt",
    "{refusals}/listing.txt"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py classify BASE.json LIVE.json INCOMING.json"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{refusals}/work"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py export DIR --url URL [--files-listing F] [--docs D] [--version V]"
   ]
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{refusals}/work",
    "--result",
    "{refusals}/written.json"
   ],
   "exit": 2,
   "stdout": {
    "error": "no export yet",
    "next": "adp.py export <tmp>/refusals/work --url URL"
   }
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{refusals}/work",
    "--summary",
    "x"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py propose DIR --by NAME --summary S [--retire ID --reason R ...]  (every deleted part id needs its own --retire ID --reason R pair, paired in order)"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{refusals}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{refusals}/listing.txt"
   ],
   "exit": 1,
   "stderr_text": [
    "<tmp>/refusals/listing.txt: no file rows (- \"path\"  type  N bytes) and not JSON: save the Artifact list result as it came"
   ]
  }
 ]
}
```

```json fixture
{
 "fixture": "shapes",
 "base": "loop",
 "files": {
  "work/index.html": null,
  "work/parts/app.js": null,
  "work/styles/page.css": null,
  "work.adp/incoming/files/index.html": "<!doctype html><html><head><meta charset=utf8><title>x</title><style>b{}</style></head><body>\n<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n\n</body></html>\n",
  "listing.txt": "- \"index.html\"  text/html  336 bytes\n- \"parts/app.js\"  text/javascript  71 bytes\n- \"styles/page.css\"  text/css  64 bytes\n- \"seed.json\"  application/json  10 bytes\n",
  "docs.json": "{\n \"manifest\": {\n  \"current\": {\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n },\n \"parts\": [\n  {\n   \"doc_id\": \"parts/home\",\n   \"hash\": \"081b78b8f894\",\n   \"version\": 2\n  },\n  {\n   \"doc_id\": \"parts/home.lead\",\n   \"hash\": \"c6a82a517ff8\",\n   \"version\": 3\n  }\n ],\n \"content\": [\n  {\n   \"id\": \"home.lead\",\n   \"html\": \"<p>Hi</p>\",\n   \"version\": 1\n  }\n ]\n}\n",
  "mine/content.js": "window.ADP_CONTENT = {\"home.lead\": {\"part\": \"home.lead\", \"title\": \"Lead\", \"html\": \"<p>Howdy</p>\"}};\n"
 }
}
```

```json vector
{
 "vector": "loop-export-reads-every-input-shape",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{shapes}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{shapes}/listing.txt",
    "--docs",
    "{shapes}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/shapes/work.adp/state.json",
    "next": "clean: nothing to send"
   },
   "files_out": {
    "{home}/artifacts.json": {
     "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001": {
      "dir": "<tmp>/shapes/work",
      "name": "work"
     }
    },
    "{shapes}/work.adp/incoming/files.json": [
     {
      "path": "index.html",
      "sha256": "",
      "bytes": 336,
      "ref": null
     },
     {
      "path": "parts/app.js",
      "sha256": "",
      "bytes": 71,
      "ref": null
     },
     {
      "path": "styles/page.css",
      "sha256": "",
      "bytes": 64,
      "ref": null
     }
    ],
    "{shapes}/work.adp/incoming/report.json": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "{shapes}/work.adp/incoming/live-manifest.json": {
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
     "parents": {
      "_rest:index.html": "",
      "_rest:parts/app.js": "",
      "_rest:styles/page.css": "",
      "home": "",
      "home.lead": "home",
      "page.header": "",
      "page.script.app": "",
      "page.style": ""
     },
     "files": {
      "index.html": "bd002c3d502b",
      "parts/app.js": "574c60bebc47",
      "styles/page.css": "56ee869c6a7b"
     },
     "page_hash": "7f4556515dd9"
    },
    "{shapes}/work.adp/incoming/db/manifest/current.json": {
     "schema": "adp/2",
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
     "files": {
      "index.html": "bd002c3d502b",
      "parts/app.js": "574c60bebc47",
      "styles/page.css": "56ee869c6a7b"
     },
     "parents": {
      "_rest:index.html": "",
      "_rest:parts/app.js": "",
      "_rest:styles/page.css": "",
      "home": "",
      "home.lead": "home",
      "page.header": "",
      "page.script.app": "",
      "page.style": ""
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
     "version": "7"
    },
    "{shapes}/work.adp/state.json": {
     "base": {
      "manifest": {
       "files": {
        "index.html": "bd002c3d502b",
        "parts/app.js": "574c60bebc47",
        "styles/page.css": "56ee869c6a7b"
       },
       "parents": {
        "_rest:index.html": "",
        "_rest:parts/app.js": "",
        "_rest:styles/page.css": "",
        "home": "",
        "home.lead": "home",
        "page.header": "",
        "page.script.app": "",
        "page.style": ""
       },
       "parts": {
        "_rest:index.html": "ee2d7cd8fa75",
        "_rest:parts/app.js": "e3b0c44298fc",
        "_rest:styles/page.css": "e3b0c44298fc",
        "home": "081b78b8f894",
        "home.lead": "c6a82a517ff8",
        "page.header": "0d957e9aee8d",
        "page.script.app": "35c146f76e12",
        "page.style": "997faceca260"
       }
      },
      "version": "7"
     },
     "capabilities": {},
     "catalog": {
      "url": "",
      "vermap": {}
     },
     "commits": {
      "live": "<commit>",
      "work": "<commit>"
     },
     "docs": {
      "content/home.lead": 1,
      "manifest/current": 7,
      "parts/home": 2,
      "parts/home.lead": 3
     },
     "exported_at": "<time>",
     "files": {
      "index.html": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
      "parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
      "styles/page.css": "56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc"
     },
     "incoming": {
      "acked": [],
      "held": [],
      "pending_replies": [],
      "proposed": {},
      "unacked": []
     },
     "live": {
      "at": "<time>",
      "version": "7"
     },
     "live_manifest": {
      "files": {
       "index.html": "bd002c3d502b",
       "parts/app.js": "574c60bebc47",
       "styles/page.css": "56ee869c6a7b"
      },
      "parents": {
       "_rest:index.html": "",
       "_rest:parts/app.js": "",
       "_rest:styles/page.css": "",
       "home": "",
       "home.lead": "home",
       "page.header": "",
       "page.script.app": "",
       "page.style": ""
      },
      "parts": {
       "_rest:index.html": "ee2d7cd8fa75",
       "_rest:parts/app.js": "e3b0c44298fc",
       "_rest:styles/page.css": "e3b0c44298fc",
       "home": "081b78b8f894",
       "home.lead": "c6a82a517ff8",
       "page.header": "0d957e9aee8d",
       "page.script.app": "35c146f76e12",
       "page.style": "997faceca260"
      }
     },
     "name": "work",
     "page_hash": "7f4556515dd9",
     "refs": {},
     "schema": "adp-state/1",
     "src_copy": {},
     "status": {},
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001"
    },
    "{shapes}/work/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"
   }
  },
  {
   "same_tree": [
    "{shapes}/work",
    "{loop}/work"
   ]
  },
  {
   "copy": [
    "{shapes}/mine",
    "{shapes}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{shapes}/work",
    "--by",
    "agent-a",
    "--summary",
    "Lead: howdy"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/shapes/work.adp/propose-<pid>.json",
    "parts": 3,
    "files": 2,
    "chunks": 0,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/shapes/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/shapes/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/shapes/work.adp/propose-<pid>"
   },
   "files_out": {
    "{shapes}/work.adp/propose-*.json": {
     "by": "agent-a",
     "at": "<time>",
     "summary": "Lead: howdy",
     "threads": [],
     "base": {
      "version": "7",
      "page_hash": "7f4556515dd9",
      "docs": {
       "content/home.lead": 1,
       "manifest/current": 7,
       "parts/home": 2,
       "parts/home.lead": 3
      }
     },
     "parts": [
      {
       "id": "home",
       "from": "081b78b8f894",
       "to": "321732a04e94",
       "html": "",
       "retired": false,
       "reason": ""
      },
      {
       "id": "home.lead",
       "from": "c6a82a517ff8",
       "to": "31d186af845c",
       "html": "<p>Howdy</p>",
       "retired": false,
       "reason": ""
      },
      {
       "id": "home.lead",
       "kind": "content",
       "from": "9c655e84ab91",
       "to": "8412217bfb89",
       "html": "<p>Howdy</p>",
       "retired": false,
       "reason": ""
      }
     ],
     "files": [
      {
       "path": "content.js",
       "ifMatch": null,
       "contentType": "text/javascript",
       "content": "window.ADP_CONTENT = {\"home.lead\": {\"part\": \"home.lead\", \"title\": \"Lead\", \"html\": \"<p>Howdy</p>\"}};\n"
      },
      {
       "path": "index.html",
       "ifMatch": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
       "contentType": "text/html",
       "content": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Howdy</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"
      }
     ],
     "live_files": {
      "index.html": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
      "parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
      "styles/page.css": "56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc"
     },
     "classified": {
      "new": [
       "content.js"
      ],
      "ours": [
       "home",
       "home.lead",
       "index.html"
      ],
      "theirs": [],
      "applied": [],
      "held": [],
      "retired": []
     },
     "status": "new",
     "decided": {
      "by": "",
      "at": "",
      "reason": ""
     },
     "applied": {
      "version": "",
      "at": ""
     }
    }
   }
  }
 ]
}
```

```json fixture
{
 "fixture": "content",
 "base": "loop",
 "files": {
  "work/content/home.lead.html": "Hi copy",
  "work/content/page.header.html": "Board copy",
  "docs.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ],\n \"content\": [\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"html\": \"Hi copy\"\n   },\n   \"version\": 1\n  },\n  {\n   \"id\": \"page.header\",\n   \"data\": {\n    \"html\": \"Board copy\"\n   },\n   \"version\": 1\n  }\n ]\n}\n",
  "docs-2.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ],\n \"content\": [\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"html\": \"Hi live 2\"\n   },\n   \"version\": 1\n  },\n  {\n   \"id\": \"page.header\",\n   \"data\": {\n    \"html\": \"Board copy\"\n   },\n   \"version\": 1\n  }\n ]\n}\n",
  "docs-3.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ],\n \"content\": [\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"html\": \"Hi live 3\"\n   },\n   \"version\": 1\n  },\n  {\n   \"id\": \"page.header\",\n   \"data\": {\n    \"html\": \"Board copy\"\n   },\n   \"version\": 1\n  }\n ]\n}\n",
  "mine2/index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board!</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "mine2/parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "mine2/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n",
  "mine2/content/home.lead.html": "Hi copy",
  "mine2/content/page.header.html": "Board! copy"
 }
}
```

```json vector
{
 "vector": "loop-content-merges-over-base",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{content}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{content}/listing.json",
    "--docs",
    "{content}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/content/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{content}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{content}/listing.json",
    "--docs",
    "{content}/docs-2.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/content/work.adp/state.json",
    "next": "clean: nothing to send"
   },
   "files_out": {
    "{content}/work/content/home.lead.html": "Hi live 2"
   }
  },
  {
   "copy": [
    "{content}/mine2",
    "{content}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{content}/work",
    "--by",
    "agent-a",
    "--summary",
    "Header"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/content/work.adp/propose-<pid>.json",
    "parts": 2,
    "files": 1,
    "chunks": 0,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/content/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/content/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/content/work.adp/propose-<pid>"
   },
   "files_out": {
    "{content}/work.adp/propose-*.json": {
     "by": "agent-a",
     "at": "<time>",
     "summary": "Header",
     "threads": [],
     "base": {
      "version": "7",
      "page_hash": "7f4556515dd9",
      "docs": {
       "content/home.lead": 1,
       "content/page.header": 1,
       "manifest/current": 7,
       "parts/home": 2,
       "parts/home.lead": 3
      }
     },
     "parts": [
      {
       "id": "page.header",
       "from": "0d957e9aee8d",
       "to": "2c848a010972",
       "html": "Board! copy",
       "retired": false,
       "reason": ""
      },
      {
       "id": "page.header",
       "kind": "content",
       "from": "6b042a29c9dc",
       "to": "f530f45d304d",
       "html": "Board! copy",
       "retired": false,
       "reason": ""
      }
     ],
     "files": [
      {
       "path": "index.html",
       "ifMatch": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
       "contentType": "text/html",
       "content": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board!</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"
      }
     ],
     "live_files": {
      "index.html": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
      "parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
      "styles/page.css": "56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc"
     },
     "classified": {
      "new": [],
      "ours": [
       "index.html",
       "page.header"
      ],
      "theirs": [],
      "applied": [],
      "held": [],
      "retired": []
     },
     "status": "new",
     "decided": {
      "by": "",
      "at": "",
      "reason": ""
     },
     "applied": {
      "version": "",
      "at": ""
     }
    }
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{content}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{content}/listing.json",
    "--docs",
    "{content}/docs-3.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [
      "index.html",
      "page.header"
     ],
     "theirs": [],
     "applied": [],
     "held": [
      {
       "id": "content/home.lead.html",
       "base": null,
       "live": null,
       "incoming": null
      }
     ],
     "retired": [],
     "merge_conflict": [
      "CONFLICT (content): Merge conflict in content/home.lead.html"
     ]
    },
    "merged": false,
    "state": "<tmp>/content/work.adp/state.json",
    "next": "held: 1; show both versions to the owner, nobody writes"
   }
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{content}/work",
    "--by",
    "agent-a",
    "--summary",
    "Header again"
   ],
   "exit": 2,
   "stdout": {
    "refused": [
     {
      "error": "merge conflict with live",
      "detail": [
       "CONFLICT (content): Merge conflict in content/home.lead.html"
      ]
     }
    ]
   }
  }
 ]
}
```

```json fixture
{
 "fixture": "big",
 "base": "loop",
 "files": {
  "listing-big.json": "{\n \"files\": [\n  {\n   \"path\": \"index.html\",\n   \"sha256\": \"bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3\",\n   \"bytes\": 336\n  },\n  {\n   \"path\": \"parts/app.js\",\n   \"sha256\": \"574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df\",\n   \"bytes\": 71\n  },\n  {\n   \"path\": \"styles/page.css\",\n   \"sha256\": \"56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc\",\n   \"bytes\": 64\n  },\n  {\n   \"path\": \"lib/shared.js\",\n   \"artifact\": \"00000000-0000-4000-8000-000000000002\",\n   \"ver\": \"3\"\n  }\n ]\n}\n",
  "work/lib/shared.js": "export const x = 1;\n",
  "work/data/big.txt": {
   "fill": 300000
  },
  "work/img/dot.png": {
   "base64": "iVBORw0KGgoAAAANSUhEUg=="
  },
  "work/index.html": "<header><h1>Board</h1></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
  "published.json": "{\n \"shas\": {\n  \"data/big.txt\": \"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\"\n },\n \"version_id\": \"9\"\n}\n",
  "notjson.txt": "not json\n"
 }
}
```

```json fixture
{
 "fixture": "big-applied",
 "files": {
  "docs.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ],\n \"incoming\": {\n  \"<pid>\": {\n   \"data\": {\n    \"status\": \"applied\",\n    \"applied\": {\n     \"version\": \"9\",\n     \"at\": \"\"\n    }\n   },\n   \"version\": 1\n  },\n  \"p-1000000000000-abcd\": {\n   \"data\": {\n    \"status\": \"declined\"\n   },\n   \"version\": 1\n  }\n }\n}\n"
 }
}
```

```json vector
{
 "vector": "loop-retire-chunk-and-ack",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{big}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{big}/listing-big.json",
    "--docs",
    "{big}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [
      "data/big.txt",
      "img/dot.png"
     ],
     "ours": [
      "_rest:index.html",
      "index.html"
     ],
     "theirs": [],
     "applied": [],
     "held": [
      {
       "id": "page.header",
       "base": "0d957e9aee8d",
       "live": "0d957e9aee8d",
       "incoming": null
      }
     ],
     "retired": []
    },
    "merged": false,
    "state": "<tmp>/big/work.adp/state.json",
    "next": "held: 1; show both versions to the owner, nobody writes"
   }
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{big}/work",
    "--by",
    "agent-a",
    "--summary",
    "Data",
    "--retire",
    "page.header"
   ],
   "exit": 2,
   "stdout": {
    "refused": [
     {
      "error": "held",
      "held": [
       {
        "id": "page.header",
        "base": "0d957e9aee8d",
        "live": "0d957e9aee8d",
        "incoming": null
       }
      ]
     },
     {
      "error": "deleted without --retire ID --reason R",
      "ids": [
       "page.header"
      ]
     },
     {
      "error": "--retire needs --reason",
      "ids": [
       "page.header"
      ]
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{big}/work",
    "--by",
    "agent-a",
    "--summary",
    "Data",
    "--retire",
    "page.header",
    "--reason",
    "folded into home"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/big/work.adp/propose-<pid>.json",
    "parts": 2,
    "files": 3,
    "chunks": 3,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming/<pid>/chunks",
       "doc_id": "0",
       "file_path": "<tmp>/big/work.adp/propose-<pid>/incoming~<pid>~chunks__0.json"
      },
      {
       "op": "set",
       "collection": "incoming/<pid>/chunks",
       "doc_id": "1",
       "file_path": "<tmp>/big/work.adp/propose-<pid>/incoming~<pid>~chunks__1.json"
      },
      {
       "op": "set",
       "collection": "incoming/<pid>/chunks",
       "doc_id": "2",
       "file_path": "<tmp>/big/work.adp/propose-<pid>/incoming~<pid>~chunks__2.json"
      },
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/big/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/big/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/big/work.adp/propose-<pid>"
   },
   "files_out": {
    "{big}/work.adp/propose-*.json": {
     "by": "agent-a",
     "at": "<time>",
     "summary": "Data",
     "threads": [],
     "base": {
      "version": "7",
      "page_hash": "7f4556515dd9",
      "docs": {
       "manifest/current": 7,
       "parts/home": 2,
       "parts/home.lead": 3
      }
     },
     "parts": [
      {
       "id": "_rest:index.html",
       "from": "ee2d7cd8fa75",
       "to": "0b9c8e0dff05",
       "html": "",
       "retired": false,
       "reason": ""
      },
      {
       "id": "page.header",
       "from": "0d957e9aee8d",
       "to": null,
       "html": "",
       "retired": true,
       "reason": "folded into home"
      }
     ],
     "files": [
      {
       "path": "data/big.txt",
       "ifMatch": null,
       "contentType": "text/plain"
      },
      {
       "path": "img/dot.png",
       "ifMatch": null,
       "contentType": "application/octet-stream",
       "encoding": "base64",
       "content": "iVBORw0KGgoAAAANSUhEUg=="
      },
      {
       "path": "index.html",
       "ifMatch": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
       "contentType": "text/html",
       "content": "<header><h1>Board</h1></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n"
      }
     ],
     "live_files": {
      "index.html": "bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3",
      "parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
      "styles/page.css": "56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc"
     },
     "classified": {
      "new": [
       "data/big.txt",
       "img/dot.png"
      ],
      "ours": [
       "_rest:index.html",
       "index.html"
      ],
      "theirs": [],
      "applied": [],
      "held": [],
      "retired": [
       "page.header"
      ]
     },
     "status": "new",
     "decided": {
      "by": "",
      "at": "",
      "reason": ""
     },
     "applied": {
      "version": "",
      "at": ""
     }
    }
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{big}/work",
    "--result",
    "{big}/published.json"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "files"
    ],
    "live": {
     "at": "<time>",
     "version": "9"
    },
    "incoming": {
     "held": [],
     "pending_replies": [],
     "unacked": []
    }
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{big}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{big}/listing-big.json",
    "--docs",
    "{big-applied}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [
      "data/big.txt",
      "img/dot.png"
     ],
     "ours": [
      "_rest:index.html",
      "index.html"
     ],
     "theirs": [],
     "applied": [],
     "held": [
      {
       "id": "page.header",
       "base": "0d957e9aee8d",
       "live": "0d957e9aee8d",
       "incoming": null
      }
     ],
     "retired": []
    },
    "merged": false,
    "state": "<tmp>/big/work.adp/state.json",
    "next": "held: 1; show both versions to the owner, nobody writes"
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{big}/work",
    "--proposal",
    "<pid>"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "incoming/<pid> applied"
    ],
    "live": {
     "at": "<time>",
     "version": "9"
    },
    "incoming": {
     "held": [
      "page.header"
     ],
     "pending_replies": [],
     "unacked": []
    }
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{big}/work",
    "--proposal",
    "p-1000000000000-abcd"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "incoming/<pid> declined"
    ],
    "live": {
     "at": "<time>",
     "version": "9"
    },
    "incoming": {
     "held": [
      "page.header"
     ],
     "pending_replies": [],
     "unacked": []
    }
   }
  },
  {
   "run": [
    "adp.py",
    "gate"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "permissionDecision": "deny",
     "permissionDecisionReason": "adp: the inbox has held: page.header. Run adp.py export <tmp>/big/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 and resolve them first"
    }
   },
   "stdin": "{\"tool_name\": \"mcp__claude_ai__ArtifactData\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"action\": \"batch\", \"collection\": \"parts\", \"doc_id\": \"home\", \"if_version\": 1}}"
  },
  {
   "run": [
    "adp.py",
    "gate",
    "--input",
    "{big}/notjson.txt"
   ],
   "exit": 1,
   "stderr_text": [
    "--input: <tmp>/big/notjson.txt is not JSON: Expecting value: line 1 column 1 (char 0)"
   ]
  },
  {
   "run": [
    "adp.py",
    "gate"
   ],
   "exit": 0,
   "stdout": {
    "hookSpecificOutput": {
     "hookEventName": "PreToolUse",
     "permissionDecision": "deny",
     "permissionDecisionReason": "adp: the inbox has held: page.header. Run adp.py export <tmp>/big/work --url https://claude.ai/artifact/00000000-0000-4000-8000-000000000001 and resolve them first"
    }
   },
   "stdin": "{\"tool_name\": \"Artifact\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\"}}"
  },
  {
   "run": [
    "adp.py",
    "ack",
    "--hook"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "parts/home"
    ],
    "live": {
     "at": "<time>",
     "version": "9"
    },
    "incoming": {
     "held": [
      "page.header"
     ],
     "pending_replies": [],
     "unacked": []
    }
   },
   "stdin": "{\"tool_name\": \"mcp__claude_ai__ArtifactData\", \"tool_input\": {\"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"action\": \"batch\"}, \"tool_response\": [{\"type\": \"text\", \"text\": \"{\\\"results\\\": [{\\\"collection\\\": \\\"parts\\\", \\\"id\\\": \\\"home\\\", \\\"version\\\": 7}]}\"}]}"
  }
 ]
}
```

The first export fills a folder that holds only dotfiles, a read that was not saved under `incoming/files` is not copied into the folder, a proposal applied without a version leaves the live version as it was, and a state written without `live_manifest` or `status` still proposes (its live manifest is read from `incoming/live-manifest.json`) and refuses to acknowledge a proposal it has no status for.

```json fixture
{
 "fixture": "strays",
 "base": "loop",
 "files": {
  "work/index.html": null,
  "work/parts/app.js": null,
  "work/styles/page.css": null,
  "work/.DS_Store": "x"
 }
}
```

```json fixture
{
 "fixture": "sparse",
 "files": {
  "parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
  "styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n"
 }
}
```

```json fixture
{
 "fixture": "applied-empty",
 "files": {
  "docs.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"parts\": {\n     \"_rest:index.html\": \"ee2d7cd8fa75\",\n     \"_rest:parts/app.js\": \"e3b0c44298fc\",\n     \"_rest:styles/page.css\": \"e3b0c44298fc\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\",\n     \"page.script.app\": \"35c146f76e12\",\n     \"page.style\": \"997faceca260\"\n    },\n    \"files\": {\n     \"index.html\": \"bd002c3d502b\",\n     \"parts/app.js\": \"574c60bebc47\",\n     \"styles/page.css\": \"56ee869c6a7b\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"_rest:parts/app.js\": \"\",\n     \"_rest:styles/page.css\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\",\n     \"page.script.app\": \"\",\n     \"page.style\": \"\"\n    },\n    \"elements\": {\n     \"_rest:index.html\": 2,\n     \"_rest:parts/app.js\": 0,\n     \"_rest:styles/page.css\": 0,\n     \"home\": 1,\n     \"home.lead\": 1,\n     \"page.header\": 1,\n     \"page.script.app\": 0,\n     \"page.style\": 0\n    },\n    \"part_file\": {\n     \"_rest:index.html\": \"index.html\",\n     \"_rest:parts/app.js\": \"parts/app.js\",\n     \"_rest:styles/page.css\": \"styles/page.css\",\n     \"home\": \"index.html\",\n     \"home.lead\": \"index.html\",\n     \"page.header\": \"index.html\",\n     \"page.script.app\": \"parts/app.js\",\n     \"page.style\": \"styles/page.css\"\n    },\n    \"version\": \"7\"\n   },\n   \"version\": 7\n  }\n ],\n \"parts\": [\n  {\n   \"id\": \"home\",\n   \"data\": {\n    \"hash\": \"081b78b8f894\"\n   },\n   \"version\": 2\n  },\n  {\n   \"id\": \"home.lead\",\n   \"data\": {\n    \"hash\": \"c6a82a517ff8\"\n   },\n   \"version\": 3\n  }\n ],\n \"incoming\": {\n  \"<pid>\": {\n   \"data\": {\n    \"status\": \"applied\",\n    \"applied\": {\n     \"version\": \"\",\n     \"at\": \"\"\n    }\n   },\n   \"version\": 1\n  },\n  \"p-1000000000000-abcd\": {\n   \"data\": {\n    \"status\": \"declined\"\n   },\n   \"version\": 1\n  }\n }\n}\n"
 }
}
```

```json fixture
{
 "fixture": "legacy",
 "base": "loop",
 "files": {
  "work.adp/state.json": "{\"schema\": \"adp-state/1\", \"name\": \"work\", \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000001\", \"capabilities\": {}, \"exported_at\": \"2026-11-19T09:00:00Z\", \"catalog\": {\"url\": \"\", \"vermap\": {}}, \"live\": {\"version\": \"7\", \"at\": \"2026-11-19T09:00:00Z\"}, \"docs\": {}, \"files\": {\"index.html\": \"bd002c3d502bcfb11ad737f90788ece3ee82fb00e1fc958c2e3a92809a4fdfc3\", \"parts/app.js\": \"574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df\", \"styles/page.css\": \"56ee869c6a7b0e7d21e0dec5797d620a57125641f1be3303654385ab0c9addbc\"}, \"refs\": {}, \"src_copy\": {}, \"base\": {\"version\": \"7\", \"manifest\": {\"parts\": {\"_rest:index.html\": \"ee2d7cd8fa75\", \"_rest:parts/app.js\": \"e3b0c44298fc\", \"_rest:styles/page.css\": \"e3b0c44298fc\", \"home\": \"081b78b8f894\", \"home.lead\": \"c6a82a517ff8\", \"page.header\": \"0d957e9aee8d\", \"page.script.app\": \"35c146f76e12\", \"page.style\": \"997faceca260\"}, \"parents\": {\"_rest:index.html\": \"\", \"_rest:parts/app.js\": \"\", \"_rest:styles/page.css\": \"\", \"home\": \"\", \"home.lead\": \"home\", \"page.header\": \"\", \"page.script.app\": \"\", \"page.style\": \"\"}, \"files\": {\"index.html\": \"bd002c3d502b\", \"parts/app.js\": \"574c60bebc47\", \"styles/page.css\": \"56ee869c6a7b\"}}}, \"incoming\": {\"held\": [], \"unacked\": [], \"pending_replies\": [], \"proposed\": {}, \"acked\": []}}",
  "work.adp/incoming/live-manifest.json": "{\"parts\": {\"_rest:index.html\": \"ee2d7cd8fa75\", \"_rest:parts/app.js\": \"e3b0c44298fc\", \"_rest:styles/page.css\": \"e3b0c44298fc\", \"home\": \"081b78b8f894\", \"home.lead\": \"c6a82a517ff8\", \"page.header\": \"0d957e9aee8d\", \"page.script.app\": \"35c146f76e12\", \"page.style\": \"997faceca260\"}, \"parents\": {\"_rest:index.html\": \"\", \"_rest:parts/app.js\": \"\", \"_rest:styles/page.css\": \"\", \"home\": \"\", \"home.lead\": \"home\", \"page.header\": \"\", \"page.script.app\": \"\", \"page.style\": \"\"}, \"files\": {\"index.html\": \"bd002c3d502b\", \"parts/app.js\": \"574c60bebc47\", \"styles/page.css\": \"56ee869c6a7b\"}, \"page_hash\": \"7f4556515dd9\"}"
 }
}
```

```json vector
{
 "vector": "loop-import-and-unsaved-reads",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{strays}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{strays}/listing.json",
    "--docs",
    "{strays}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/strays/work.adp/state.json",
    "next": "clean: nothing to send"
   },
   "files_out": {
    "{strays}/work/styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n"
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  },
  {
   "copy": [
    "{sparse}",
    "{loop}/work.adp/incoming/files"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing-8.json",
    "--docs",
    "{loop}/docs-8.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [
      "home",
      "home.lead",
      "index.html"
     ],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  }
 ]
}
```

A state that predates the status table still acks from the proposal's record under `incoming/db/incoming/` (the fixture `legacy-record`, whose file name takes the proposal id the last step printed):

```json fixture
{
 "fixture": "legacy-record",
 "files": {
  "work.adp/incoming/db/incoming/<pid>.json": "{\"status\": \"applied\", \"applied\": {\"version\": \"9\", \"at\": \"\"}}"
 }
}
```

```json vector
{
 "vector": "loop-empty-applied-version-and-older-state",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{loop}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  },
  {
   "copy": [
    "{loop}/mine",
    "{loop}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{loop}/work",
    "--by",
    "agent-a",
    "--summary",
    "Lead: greeting"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/loop/work.adp/propose-<pid>.json",
    "parts": 2,
    "files": 1,
    "chunks": 0,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/loop/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/loop/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/loop/work.adp/propose-<pid>"
   }
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{applied-empty}/docs.json"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{loop}/work",
    "--proposal",
    "<pid>"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "incoming/<pid> applied"
    ],
    "live": {
     "at": "<time>",
     "version": "7"
    },
    "incoming": {
     "held": [],
     "unacked": [],
     "pending_replies": []
    }
   }
  },
  {
   "copy": [
    "{legacy}/mine",
    "{legacy}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "propose",
    "{legacy}/work",
    "--by",
    "agent-a",
    "--summary",
    "Lead: greeting"
   ],
   "exit": 0,
   "stdout": {
    "proposal": "<pid>",
    "doc": "<tmp>/legacy/work.adp/propose-<pid>.json",
    "parts": 2,
    "files": 1,
    "chunks": 0,
    "next": "run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page",
    "batches": [
     [
      {
       "op": "set",
       "collection": "incoming",
       "doc_id": "<pid>",
       "file_path": "<tmp>/legacy/work.adp/propose-<pid>.json"
      },
      {
       "op": "set",
       "collection": "changes",
       "doc_id": "d-<ms>",
       "file_path": "<tmp>/legacy/work.adp/propose-<pid>/changes__d-<ms>.json"
      }
     ]
    ],
    "docs_dir": "<tmp>/legacy/work.adp/propose-<pid>"
   }
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{legacy}/work",
    "--proposal",
    "<pid>"
   ],
   "exit": 1,
   "stderr_text": [
    "<pid>: status unknown in the last export read; ack it once applied or declined"
   ]
  },
  {
   "copy": [
    "{legacy-record}/work.adp/incoming",
    "{legacy}/work.adp/incoming"
   ]
  },
  {
   "run": [
    "adp.py",
    "ack",
    "{legacy}/work",
    "--proposal",
    "<pid>"
   ],
   "exit": 0,
   "stdout": {
    "ack": [
     "incoming/<pid> applied"
    ],
    "live": {
     "at": "<time>",
     "version": "9"
    },
    "incoming": {
     "held": [],
     "unacked": [],
     "pending_replies": []
    }
   }
  }
 ]
}
```

The fixture `unrecorded` is a record that lists fewer parts than the page's files hold (none of `parts/app.js` or `styles/page.css`) and an old hash for
`_rest:index.html`. The files are the live ones, so the first export has nothing to send; after an edit, only what the edit changed is `new` or `ours`.

```json fixture
{
 "fixture": "unrecorded",
 "files": {
  "docs.json": "{\n \"manifest\": [\n  {\n   \"id\": \"current\",\n   \"data\": {\n    \"schema\": \"adp/2\",\n    \"page_hash\": \"7f4556515dd9\",\n    \"version\": \"7\",\n    \"parts\": {\n     \"_rest:index.html\": \"000000000000\",\n     \"home\": \"081b78b8f894\",\n     \"home.lead\": \"c6a82a517ff8\",\n     \"page.header\": \"0d957e9aee8d\"\n    },\n    \"parents\": {\n     \"_rest:index.html\": \"\",\n     \"home\": \"\",\n     \"home.lead\": \"home\",\n     \"page.header\": \"\"\n    }\n   },\n   \"version\": 7\n  }\n ]\n}\n"
 }
}
```

```json vector
{
 "vector": "loop-a-part-in-an-unchanged-file-is-not-a-change",
 "steps": [
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{unrecorded}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "clean: nothing to send"
   }
  },
  {
   "copy": [
    "{loop}/mine",
    "{loop}/work"
   ]
  },
  {
   "run": [
    "adp.py",
    "export",
    "{loop}/work",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000001",
    "--files-listing",
    "{loop}/listing.json",
    "--docs",
    "{unrecorded}/docs.json"
   ],
   "exit": 0,
   "stdout": {
    "report": {
     "new": [],
     "ours": [
      "_rest:index.html",
      "home",
      "home.lead",
      "index.html"
     ],
     "theirs": [],
     "applied": [],
     "held": [],
     "retired": []
    },
    "merged": true,
    "state": "<tmp>/loop/work.adp/state.json",
    "next": "adp.py propose <tmp>/loop/work --by NAME --summary S"
   }
  }
 ]
}
```
