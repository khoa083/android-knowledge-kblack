/* Glossary for the cleancode track (English). */
ADE.addGlossary('en', 'cleancode', {
  "cyclomatic-complexity": { term: "cyclomatic complexity", def: "The number of paths through a piece of code. Counting by hand, Seemann's way: start at 1, add 1 for each branching or looping instruction (if, for, while, each when branch). It is also the minimum number of tests that cover every path.", chapter: "cleancode/j1" },
  "working-memory": { term: "working memory", def: "The part of short-term memory holding what you are thinking about. It holds only a few pieces of information at once; Seemann uses 7 as a symbolic threshold when reading code.", chapter: "cleancode/j1" },
  "stepdown-rule": { term: "stepdown rule", def: "Martin's rule: code reads top-down like a narrative, each function followed by those one level of abstraction below.", chapter: "cleancode/j1" },
  "cqs": { term: "command query separation (CQS)", def: "Bertrand Meyer's principle: a function that changes state (a command) returns no data; a function that returns data (a query) changes no state. The signature then tells you whether it reads or writes.", chapter: "cleancode/j2" },
  "observable-side-effect": { term: "side effect (observable)", def: "A change callers can observe beyond the return value: writing a database, clearing a cache, mutating an object's field, sending over the network. Mutating a local variable inside the function does not count.", chapter: "cleancode/j2" },
  "flag-argument": { term: "flag argument", def: "A Boolean parameter that decides whether the function does one thing or another. Martin treats it as a sign the function does two things; split it into two named functions.", chapter: "cleancode/j2" },
  "code-rot": { term: "code rot", def: "Code growing more complex with each small change nobody notices, until nobody dares to touch it. Seemann proposes a threshold on a metric to curb it.", chapter: "cleancode/j1" }
});
