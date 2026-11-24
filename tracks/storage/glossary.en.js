/* Thuật ngữ track storage (English). */
ADE.addGlossary('en', 'storage', {
  "app-specific-storage": { term: "app-specific storage", def: "Directories only your app uses (filesDir, cacheDir and their external counterparts). No permissions needed; removed on uninstall; the internal ones are encrypted from Android 10.", chapter: "storage/h1" },
  "shared-storage": { term: "shared storage", def: "Where files the user wants to keep and other apps can see live: images, video and audio through MediaStore; documents through the Storage Access Framework. Not removed on uninstall.", chapter: "storage/h1" },
  "cache-dir": { term: "cache directory (cacheDir)", def: "A private directory for temporary data. When the device runs low on storage the system may delete files here, so keep only things you can recreate or download again.", chapter: "storage/h1" },
  "datastore": { term: "DataStore", def: "A Jetpack library that stores key–value pairs (Preferences DataStore) or typed objects (Proto DataStore): read through a Flow, written by suspend functions as transactions. The recommended replacement for SharedPreferences, meant for small data.", chapter: "storage/h1" },
  "room": { term: "Room", def: "A Jetpack library over SQLite: entities are tables, DAOs hold the query functions, SQL is checked at compile time. Meant for structured data with many records that you need to query.", chapter: "storage/h1" }
});
