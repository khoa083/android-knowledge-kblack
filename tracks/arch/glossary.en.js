/* Thuật ngữ track arch (English). */
ADE.addGlossary('en', 'arch', {
  "separation-of-concerns": { term: "separation of concerns", def: "Splitting an app into parts (classes, files, modules, layers) that each have one clear responsibility; the most important principle in Android's architecture guide.", chapter: "arch/g1" },
  "configuration-change": { term: "configuration change", def: "Rotating the screen, changing language or font size…: the system destroys the current Activity and creates a new instance with the new configuration.", chapter: "arch/g1" },
  "state-holder": { term: "state holder (ViewModel)", def: "A class that holds and produces state for a screen, separate from the Activity; ViewModel is a state holder that survives configuration changes.", chapter: "arch/g1" },
  "ssot": {"term": "single source of truth (SSOT)", "def": "The single owner of a type of data: only it modifies that data, exposes it as an immutable type and receives changes through functions or events. Offline-first apps usually make the database the SSOT.", "chapter": "arch/g2"},
  "udf": {"term": "unidirectional data flow (UDF)", "def": "State flows one way, from its holder down to the UI; events flow the opposite way, up to the SSOT where the data is changed.", "chapter": "arch/g2"},
  "dependency-rule": {"term": "Dependency Rule", "def": "The central rule of Clean Architecture (Robert C. Martin, presented for Android by Boudjnah): dependency arrows point only inward, toward the domain; inner layers know nothing about outer ones.", "chapter": "arch/g2"},
  "dependency-inversion": {"term": "dependency inversion", "def": "Put an interface on the side that uses it (for example a repository interface next to the use case) and make the implementation depend on that interface, so the dependency arrow points against the direction of the call.", "chapter": "arch/g2"}
});
