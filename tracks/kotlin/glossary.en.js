/* Kotlin track glossary (English). */
ADE.addGlossary('en', 'kotlin', {
  "val-var": { term: "val / var", def: "val is a reference assigned once; var can be reassigned. val does not make the object behind it immutable: a val pointing to a MutableList can still get new elements.", chapter: "kotlin/k1" },
  "type-inference": { term: "type inference", def: "The compiler works out the type of a variable or expression from its initial value; the type is fixed at compile time and does not change at runtime.", chapter: "kotlin/k1" },
  "integer-division": { term: "integer division", def: "Dividing two integers gives an integer and drops the fraction (5 / 2 = 2). To keep the fraction, one operand must be a Double or Float.", chapter: "kotlin/k1" },
  "when-expression": { term: "when expression", def: "when returns the value of the first matching branch; used as an expression, its branches must cover every case (usually with else).", chapter: "kotlin/k1" }
});
