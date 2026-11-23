/* Thuật ngữ track arch (English). */
ADE.addGlossary('en', 'arch', {
  "separation-of-concerns": { term: "separation of concerns", def: "Splitting an app into parts (classes, files, modules, layers) that each have one clear responsibility; the most important principle in Android's architecture guide.", chapter: "arch/g1" },
  "configuration-change": { term: "configuration change", def: "Rotating the screen, changing language or font size…: the system destroys the current Activity and creates a new instance with the new configuration.", chapter: "arch/g1" },
  "state-holder": { term: "state holder (ViewModel)", def: "A class that holds and produces state for a screen, separate from the Activity; ViewModel is a state holder that survives configuration changes.", chapter: "arch/g1" }
});
