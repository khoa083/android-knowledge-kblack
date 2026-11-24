/* Hiểu lầm track sysdesign (English). */
ADE.addMisconceptions('en', 'sysdesign', {
  "design-is-complete": { wrong: "The screen design is enough to start coding.", right: "Designs usually show only the best case: tidy content, a good network. Errors, empty and offline states, expired sessions and error codes must be asked of the designer and the backend first. [[src:book-tjeerd]]", example: "Chapter I1: six questions turned into six secondary requirements.", chapter: "sysdesign/i1" },
  "viewmodel-survives-death": { wrong: "A ViewModel keeps data through everything, so a form in a ViewModel is safe.", right: "A ViewModel survives configuration changes but is lost when the system kills the process. Small things the user just entered belong in saved state; large or long-lived things in durable storage. [[src:ax-saving-states]]", example: "Chapter I2: open the Camera, the process is killed, come back to an empty form.", chapter: "sysdesign/i2" }
});
