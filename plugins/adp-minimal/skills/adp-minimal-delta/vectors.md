# Vectors: adp-minimal-delta

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

## Contract: `classify`, in `adp.py` and `adp.js`

```json fixture
{"fixture": "three", "files": {
 "base.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"000000000002\", \"theirs\": \"000000000003\", \"both\": \"000000000004\", \"agree\": \"000000000005\", \"old\": \"000000000006\", \"dropped\": \"000000000007\", \"p\": \"000000000008\", \"p.c\": \"000000000009\"}, \"files\": {\"index.html\": \"aaaaaaaaaaaa\"}, \"parents\": {\"p.c\": \"p\"}}",
 "live.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"000000000002\", \"theirs\": \"00000000000c\", \"both\": \"00000000000d\", \"agree\": \"00000000000e\", \"old\": \"000000000006\", \"dropped\": \"000000000007\", \"p\": \"000000000008\", \"p.c\": \"00000000000f\", \"livenew\": \"000000000010\"}, \"files\": {\"index.html\": \"aaaaaaaaaaaa\"}, \"parents\": {\"p.c\": \"p\"}}",
 "incoming.json": "{\"parts\": {\"same\": \"000000000001\", \"mine\": \"00000000001b\", \"theirs\": \"000000000003\", \"both\": \"00000000001d\", \"agree\": \"00000000000e\", \"p\": \"000000000018\", \"p.c\": \"000000000019\", \"fresh\": \"000000000020\"}, \"files\": {\"index.html\": \"bbbbbbbbbbbb\"}, \"parents\": {\"p.c\": \"p\"}, \"retired\": {\"old\": \"replaced by fresh\"}}"}}
```

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
   "mine",
   "index.html"
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

## Contract: the loop (`export`, `propose`, `ack`, `gate`)

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
    "<pid>: status unknown in the last export; ack it once applied or declined"
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
