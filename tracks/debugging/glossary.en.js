/* Glossary for the debugging track (English). */
ADE.addGlossary('en', 'debugging', {
  "reproduce": { term: "reproduce (a bug)", def: "Find a sequence of steps that makes the bug happen on every run. Only a bug that reproduces reliably lets you test a hypothesis and a fix.", chapter: "debugging/l1" },
  "adb": { term: "adb (Android Debug Bridge)", def: "A command-line tool for driving an Android device from a computer: install apps, run shell commands, copy files, take bug reports. It has a client and a server on the computer and the adbd daemon on the device.", chapter: "debugging/l1" },
  "bug-report": { term: "bug report", def: "A ZIP file gathering a device's system logs, error logs, system service state and stack traces, used to find bugs that happen on another device.", chapter: "debugging/l1" },
  "breakpoint": { term: "breakpoint", def: "A stopping point set on a line of code: when execution reaches it, the debugger pauses the app so you can look at variables. It can have a condition, only log without stopping, or stop only the thread that hits it.", chapter: "debugging/l2" },
  "suspend-policy": { term: "suspend policy", def: "Decides which threads stop when a breakpoint is hit: All stops every thread in the app, Thread stops only the thread that hit the breakpoint.", chapter: "debugging/l2" },
  "logcat": { term: "Logcat", def: "Where you see the whole device's logs (the system, other apps, your app), read from the logd process's ring buffers; filtered with queries by tag, package, level, process.", chapter: "debugging/l3" },
  "log-tag": { term: "tag (of a log)", def: "A short string attached to each log line saying where it comes from, usually the class name; used for filtering in Logcat.", chapter: "debugging/l3" },
  "stack-trace": { term: "stack trace", def: "A snapshot of the chain of function calls when an exception was thrown: the first line is the exception type and message, each \"at\" line is a frame, and the top frame is where it was thrown.", chapter: "debugging/l4" },
  "root-cause": { term: "root cause", def: "The first exception in a chain of wrapped errors, usually in the last \"Caused by\" section of a stack trace; the layers above only add context.", chapter: "debugging/l4" }
});
