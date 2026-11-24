/* Glossary for the cleancode track (English). */
ADE.addGlossary('en', 'cleancode', {
  "cyclomatic-complexity": { term: "cyclomatic complexity", def: "The number of paths through a piece of code. Counting by hand, Seemann's way: start at 1, add 1 for each branching or looping instruction (if, for, while, each when branch). It is also the minimum number of tests that cover every path.", chapter: "cleancode/j1" },
  "working-memory": { term: "working memory", def: "The part of short-term memory holding what you are thinking about. It holds only a few pieces of information at once; Seemann uses 7 as a symbolic threshold when reading code.", chapter: "cleancode/j1" },
  "stepdown-rule": { term: "stepdown rule", def: "Martin's rule: code reads top-down like a narrative, each function followed by those one level of abstraction below.", chapter: "cleancode/j1" },
  "code-rot": { term: "code rot", def: "Code growing more complex with each small change nobody notices, until nobody dares to touch it. Seemann proposes a threshold on a metric to curb it.", chapter: "cleancode/j1" }
});
