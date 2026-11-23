/* Kotlin track glossary (English). */
ADE.addGlossary('en', 'kotlin', {
  "val-var": { term: "val / var", def: "val is a reference assigned once; var can be reassigned. val does not make the object behind it immutable: a val pointing to a MutableList can still get new elements.", chapter: "kotlin/k1" },
  "type-inference": { term: "type inference", def: "The compiler works out the type of a variable or expression from its initial value; the type is fixed at compile time and does not change at runtime.", chapter: "kotlin/k1" },
  "integer-division": { term: "integer division", def: "Dividing two integers gives an integer and drops the fraction (5 / 2 = 2). To keep the fraction, one operand must be a Double or Float.", chapter: "kotlin/k1" },
  "smart-cast": { term: "smart cast", def: "The compiler treats a variable as a narrower type (String instead of String?, say) after a check, only when it can prove the variable does not change between the check and the use.", chapter: "kotlin/k2" },
  "platform-type": { term: "platform type (T!)", def: "The type of a value from Java with no nullability annotation; it means T or T?. Kotlin relaxes null checks for it, so it may throw an NPE at runtime.", chapter: "kotlin/k2" },
  "elvis": { term: "Elvis ?:", def: "An operator returning the left side if it is not null, otherwise the right side; the right side may be return or throw.", chapter: "kotlin/k2" },
  "when-expression": { term: "when expression", def: "when returns the value of the first matching branch; used as an expression, its branches must cover every case (usually with else).", chapter: "kotlin/k1" }
});
