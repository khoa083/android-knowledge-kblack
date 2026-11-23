/* Hiểu lầm track arch (English). */
ADE.addMisconceptions('en', 'arch', {
  "activity-keeps-data": { wrong: "Data kept in an Activity's fields is still there after rotating the screen.", right: "On a configuration change the system destroys the Activity and creates a new instance; the old instance's fields go with it. Keep state in a ViewModel. [[src:ax-config-changes]] [[src:ax-viewmodel]]", example: "Chapter G1: the free-slot list has to reload after every rotation.", chapter: "arch/g1" },
  "domain-required": { wrong: "Android's standard architecture requires a domain layer with use cases.", right: "The official guide requires at least a UI and a data layer; the domain layer is optional, for complex logic or logic reused by several ViewModels. [[src:ax-arch-guide]]", example: "For a screen that just reads a list, a use case that forwards the repository call unchanged is overhead.", chapter: "arch/g1" }
});
