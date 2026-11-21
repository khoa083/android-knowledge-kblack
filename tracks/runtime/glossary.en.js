/* Runtime track glossary (English). */
ADE.addGlossary('en', 'runtime', {
  "composition": { term: "Composition", def: "The result of running composables for one UI tree, kept by the runtime and updated incrementally.", chapter: "runtime/b0" },
  "recomposition": { term: "recomposition", def: "Re-running the composables that may have changed when inputs change; unchanged parts are skipped. It is not the same as redrawing.", chapter: "runtime/b7" },
  "recomposer": { term: "Recomposer", def: "The scheduler for recomposition and for applying changes to one or more Compositions.", chapter: "runtime/b5" },
  "composer": { term: "Composer", def: "The interface that Compose Compiler-generated code calls for positional memoization, change detection and incremental re-runs.", chapter: "runtime/b2" },
  "applier": { term: "Applier", def: "The component that applies the tree operations (insert, remove, move, update) emitted by the composition; generic over the node type.", chapter: "runtime/b6" },
  "slot-table": { term: "SlotTable", def: "Group- and position-based data used to remember values and identify parts of the composition; not the UI tree. Implementation details can change.", chapter: "runtime/b3" },
  "snapshot": { term: "Snapshot", def: "An isolated view of the values of state objects; changes in a mutable snapshot are applied atomically.", chapter: "runtime/b4" },
  "restart-scope": { term: "restart scope", def: "A part of the composition that can re-run on its own when a state it read changes.", chapter: "runtime/b2" },
  "composition-identity": { term: "composition identity", def: "How the runtime recognises the same composable instance across runs: call site, order and key().", chapter: "runtime/b3" },
  "stability": { term: "stability", def: "A property of a type that lets Compose compare parameters with equals and trust that every change is reported.", chapter: "runtime/b8" },
  "strong-skipping": { term: "strong skipping", def: "A compiler mode (default since Kotlin 2.0.20) that makes composables with unstable parameters skippable, comparing unstable parameters with ===.", chapter: "runtime/b8" },
  "compose-phases": { term: "Compose phases", def: "The three phases Composition, Layout and Drawing; the phase that reads a state is the one that must run again.", chapter: "runtime/b7" },
  "semantics-tree": { term: "semantics tree", def: "A parallel tree describing what UI elements mean, used by accessibility services and testing.", chapter: "runtime/b9" },
  "compose-view": { term: "ComposeView", def: "An Android View that hosts Compose content; initial composition on attach or createComposition().", chapter: "runtime/b1" },
  "composition-local": { term: "CompositionLocal", def: "Data passed implicitly down the composition tree, such as a theme.", chapter: "runtime/b0" }
});
