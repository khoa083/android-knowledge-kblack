/* Hiểu lầm track storage (English). */
ADE.addMisconceptions('en', 'storage', {
  "prefs-for-lists": { wrong: "A long list can just be turned into JSON and stored as one string in SharedPreferences.", right: "SharedPreferences loads the whole file into memory and rewrites the whole file on every write; editing one appointment rewrites all 500. Data with many records that you query or edit row by row belongs in Room. [[src:aosp-sp-impl]] [[src:ax-datastore]]", example: "Chapter H1: 500 appointments in one JSON string.", chapter: "storage/h1" },
  "cache-is-safe": { wrong: "Files in cacheDir stay there until the app deletes them.", right: "When the device runs low on storage, the system may delete cache files. Keep only things you can recreate or download again there, and check the file exists before reading it. [[src:ax-app-specific]]", example: "Chapter H1: the visit-results PDF goes in the cache because it can be downloaded again.", chapter: "storage/h1" }
});
