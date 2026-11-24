/* Misconceptions for the cleancode track (English). */
ADE.addMisconceptions('en', 'cleancode', {
  "short-means-simple": { wrong: "A short function, under 24 lines, is simple enough.", right: "Line count is only one measure. A function can still have too many paths and too many variables to track at once. [[src:book-seemann]]", example: "Chapter J1: a 19-line function with 9 paths and 13 variables.", chapter: "cleancode/j1" },
  "seven-is-a-law": { wrong: "The human brain holds exactly 7 things, so every function must stay under 7.", right: "Seemann says plainly that 7 is symbolic and the exact number does not matter; what works is having a threshold and paying attention to it. [[src:book-seemann]]", example: "Chapter J1: exceeding the threshold is sometimes the best response, as long as you bring the code back later.", chapter: "cleancode/j1" }
});
