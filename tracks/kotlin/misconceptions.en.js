/* Kotlin track misconceptions (English). */
ADE.addMisconceptions('en', 'kotlin', {
  "val-immutable": { wrong: "Declaring with val makes the data immutable.", right: "val only forbids reassigning the reference; the object it points to can still change (a MutableList, for example). [[src:book-effective-kotlin]] [[src:kt-basic-syntax]]", example: "`val list = mutableListOf(1, 2)` then `list.add(3)` compiles and runs.", chapter: "kotlin/k1" },
  "auto-widening": { wrong: "Kotlin widens Int to Long or Double on assignment, like Java.", right: "Kotlin does no implicit conversion on assignment or for arguments; call toLong(), toDouble(). Only in mixed arithmetic does the result take the wider type. [[src:kt-numbers]]", example: "`val l: Long = 1.5.toLong()` works; passing an Int to a Double parameter is a compile error.", chapter: "kotlin/k1" },
  "overflow-error": { wrong: "Overflowing an Int raises an error.", right: "The compiler reports nothing; the result wraps around to a negative value. [[src:kt-numbers]]", example: "`Int.MAX_VALUE + 1` gives -2147483648.", chapter: "kotlin/k1" }
});
