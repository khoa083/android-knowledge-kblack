/* Kotlin track glossary (English). */
ADE.addGlossary('en', 'kotlin', {
  "val-var": { term: "val / var", def: "val is a reference assigned once; var can be reassigned. val does not make the object behind it immutable: a val pointing to a MutableList can still get new elements.", chapter: "kotlin/k1" },
  "type-inference": { term: "type inference", def: "The compiler works out the type of a variable or expression from its initial value; the type is fixed at compile time and does not change at runtime.", chapter: "kotlin/k1" },
  "integer-division": { term: "integer division", def: "Dividing two integers gives an integer and drops the fraction (5 / 2 = 2). To keep the fraction, one operand must be a Double or Float.", chapter: "kotlin/k1" },
  "smart-cast": { term: "smart cast", def: "The compiler treats a variable as a narrower type (String instead of String?, say) after a check, only when it can prove the variable does not change between the check and the use.", chapter: "kotlin/k2" },
  "platform-type": { term: "platform type (T!)", def: "The type of a value from Java with no nullability annotation; it means T or T?. Kotlin relaxes null checks for it, so it may throw an NPE at runtime.", chapter: "kotlin/k2" },
  "elvis": { term: "Elvis ?:", def: "An operator returning the left side if it is not null, otherwise the right side; the right side may be return or throw.", chapter: "kotlin/k2" },
  "lateinit": { term: "lateinit", def: "Marks a non-null var that will be assigned after the object is created; reading it before then throws UninitializedPropertyAccessException. Not allowed for primitive types.", chapter: "kotlin/k3" },
  "companion-object": { term: "companion object", def: "An object tied to a class, holding members called through the class name (like Java statics); initialised when the class is loaded.", chapter: "kotlin/k3" },
  "data-class": { term: "data class", def: "A class for which the compiler generates equals, hashCode, toString, componentN and copy from the primary constructor properties.", chapter: "kotlin/k4" },
  "hash-table": { term: "hash table", def: "The structure behind HashSet/HashMap: an array of buckets; hashCode picks the bucket, equals compares inside it. An element modified after being added can end up in the wrong bucket.", chapter: "kotlin/k4" },
  "sealed": { term: "sealed class / interface", def: "A type with a fixed set of direct subtypes known at compile time (same package and module); a when over it can be exhaustive without else.", chapter: "kotlin/k5" },
  "exhaustive": { term: "exhaustive", def: "A when that handles every possible case of its subject; required when the when is an expression.", chapter: "kotlin/k5" },
  "nothing-type": { term: "Nothing", def: "The type of an expression that never completes normally, such as throw or TODO(); a subtype of every type, so it fits after ?: or in a when branch.", chapter: "kotlin/k6" },
  "precondition": { term: "require / check / error", def: "Stdlib precondition functions: require for arguments (IllegalArgumentException), check for state (IllegalStateException), error() throws IllegalStateException at once.", chapter: "kotlin/k6" },
  "use-function": { term: "use", def: "An extension on Closeable: runs the block and always closes the resource, even if the block throws; the exception still propagates.", chapter: "kotlin/k6" },
  "when-expression": { term: "when expression", def: "when returns the value of the first matching branch; used as an expression, its branches must cover every case (usually with else).", chapter: "kotlin/k1" }
});
