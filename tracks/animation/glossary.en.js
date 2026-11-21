/* Animation track glossary (English). frame-clock and launched-effect already exist in the coroutines track (global ids). */
ADE.addGlossary('en', 'animation', {
  "animation-spec": { term: "AnimationSpec", def: "Defines how a value goes from start to target over time: spring, tween, keyframes, repeatable, snap.", chapter: "animation/c2" },
  "spring-spec": { term: "spring", def: "A spec that simulates a spring with a damping ratio and stiffness; it keeps velocity continuous when the target changes. The default of animate*AsState.", chapter: "animation/c2" },
  "tween-spec": { term: "tween", def: "A spec that runs over a duration with an easing; 300 ms and FastOutSlowInEasing by default.", chapter: "animation/c2" },
  "easing": { term: "easing", def: "A function turning a time fraction into a progress fraction; the standard easings are cubic-bezier curves.", chapter: "animation/c2" },
  "decay": { term: "decay animation", def: "An animation with no fixed target: the end is computed from the initial velocity, typically after a fling.", chapter: "animation/c6" },
  "animatable": { term: "Animatable", def: "A value holder driven by suspend APIs (animateTo, snapTo, animateDecay, stop); a new animation cancels the running one.", chapter: "animation/c6" },
  "animate-as-state": { term: "animate*AsState", def: "An API returning an animated value that follows a target; changing the target mid-way continues from the current value and velocity.", chapter: "animation/c1" },
  "transition": { term: "Transition", def: "Several animated values following one state; each child can have its own spec.", chapter: "animation/c3" },
  "animated-visibility": { term: "AnimatedVisibility", def: "A composable that animates showing and hiding; content leaves the Composition after the exit finishes.", chapter: "animation/c4" },
  "animated-content": { term: "AnimatedContent", def: "A composable that animates content changes by targetState; you must use the content lambda parameter.", chapter: "animation/c4" },
  "target-value": { term: "target value", def: "The value an animation is heading to; different from the current value on screen.", chapter: "animation/c1" },
  "test-clock": { term: "mainClock", def: "The ComposeTestRule test clock; turn off autoAdvance to move time yourself; advanceTimeBy rounds up to frames.", chapter: "animation/c8" },
  "graphics-layer": { term: "graphicsLayer", def: "A modifier for draw-time transforms (scale, translation, alpha…); reading state in its lambda affects only the draw phase.", chapter: "animation/c7" }
});
