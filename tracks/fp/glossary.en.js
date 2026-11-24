/* Glossary for the fp track (English). */
ADE.addGlossary('en', 'fp', {
  "pure-function": { term: "pure function", def: "A function meeting two conditions: the same input always gives the same output, and a call does nothing besides returning the result (no clock reads, no logging, no changing outside variables). Seemann puts it briefly: deterministic and free of side effects.", chapter: "fp/p1" },
  "referential-transparency": { term: "referential transparency", def: "A property of an expression: replacing it with its value wherever it is used leaves the program's meaning unchanged. A function is pure when calls to it, with arguments that are themselves transparent, have this property.", chapter: "fp/p1" },
  "substitution-model": { term: "substitution model", def: "Reasoning about a program by replacing each expression with its value, like solving an equation, until a single value remains. It only works when the expressions are referentially transparent.", chapter: "fp/p1" },
  "persistent-data-structure": { term: "persistent data structure", def: "A structure that never changes in place: every change returns a new version and keeps the old one intact. An immutable singly linked list is the classic example.", chapter: "fp/p2" },
  "data-sharing": { term: "data sharing", def: "A new version reuses the unchanged part of the old one instead of copying it: adding x at the front of xs creates Cons(x, xs), and xs is shared. Safe because the data is immutable.", chapter: "fp/p2" },
  "tail-position": { term: "tail position", def: "A call is in tail position when the caller does nothing but return its result. A recursive function whose calls are all in tail position and that is marked tailrec is turned into a loop by Kotlin.", chapter: "fp/p2" }
});
