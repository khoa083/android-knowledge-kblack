/* Shared misconceptions (English). Track-specific entries live in tracks/<id>/misconceptions.en.js. */
ADE.addMisconceptions('en', 'shared', {
  'sim-is-real': {
    wrong: 'The simulation on this site is Compose or kotlinx.coroutines actually running.',
    right: 'A simulation is a [[term:conceptual-simulation]]: a teaching model written in JavaScript. It shows cause and effect, it does not reproduce every internal detail, and each simulation states what it simplifies.',
    example: 'A simulation can show the order of steps according to its model, but it does not guarantee the real thread schedule or the timing of each frame.'
  }
});
