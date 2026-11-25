/* Glossary for the debugging track (English). */
ADE.addGlossary('en', 'debugging', {
  "reproduce": { term: "reproduce (a bug)", def: "Find a sequence of steps that makes the bug happen on every run. Only a bug that reproduces reliably lets you test a hypothesis and a fix.", chapter: "debugging/l1" },
  "adb": { term: "adb (Android Debug Bridge)", def: "A command-line tool for driving an Android device from a computer: install apps, run shell commands, copy files, take bug reports. It has a client and a server on the computer and the adbd daemon on the device.", chapter: "debugging/l1" },
  "bug-report": { term: "bug report", def: "A ZIP file gathering a device's system logs, error logs, system service state and stack traces, used to find bugs that happen on another device.", chapter: "debugging/l1" }
});
