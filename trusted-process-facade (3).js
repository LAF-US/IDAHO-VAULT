// `node_repl` runs model code in `untrustedContext` and allowlisted packages in `trustedContext`.
// The real `process` stays private because stdio can corrupt the JSONL transport and exit controls can kill the kernel.
// Trusted `import("node:process")` and ambient `process` both resolve to this frozen facade.
// Some trusted packages, including `@oai/sky`, read ambient `process` inside deferred methods.
// Those reads resolve against `trustedContext` globals, not the synthetic import module.
// The facade exposes passive metadata plus `once/off("exit")` for trusted helper cleanup.
// `cwd()` returns a startup snapshot, and listener wrappers never expose the real process as `this`.

const PROPERTY_LIST = Object.freeze([
  "arch",
  "cwd",
  "env",
  "off",
  "once",
  "pid",
  "platform",
]);

/**
 * @typedef {{
 *   exit: (code: number) => void,
 * }} TrustedProcessListenerByEvent
 */

/**
 * @typedef {keyof TrustedProcessListenerByEvent} TrustedProcessEventName
 */

/**
 * @typedef {TrustedProcessListenerByEvent[TrustedProcessEventName]} TrustedProcessListener
 */

/**
 * @typedef {Readonly<{
 *   arch: NodeJS.Process["arch"],
 *   cwd: () => string,
 *   env: Readonly<Record<string, string>>,
 *   off: <EventName extends TrustedProcessEventName>(
 *     eventName: EventName,
 *     listener: TrustedProcessListenerByEvent[EventName],
 *   ) => TrustedProcessFacade,
 *   once: <EventName extends TrustedProcessEventName>(
 *     eventName: EventName,
 *     listener: TrustedProcessListenerByEvent[EventName],
 *   ) => TrustedProcessFacade,
 *   pid: number,
 *   platform: NodeJS.Process["platform"],
 * }>} TrustedProcessFacade
 */

/**
 * @typedef {{
 *   cwd: string,
 *   env: Readonly<Record<string, string>>,
 *   process: Pick<
 *     NodeJS.Process,
 *     "arch" | "off" | "once" | "pid" | "platform"
 *   >,
 * }} TrustedProcessCreateArgs
 */

/**
 * Creates the frozen process facade exposed to trusted package code.
 *
 * @param {TrustedProcessCreateArgs} args
 * @returns {TrustedProcessFacade}
 */
function create(args) {
  /** @type {Map<TrustedProcessEventName, WeakMap<TrustedProcessListener, TrustedProcessListener[]>>} */
  const listenerWrappersByEventName = new Map();

  /**
   * @param {TrustedProcessEventName} eventName
   * @returns {WeakMap<TrustedProcessListener, TrustedProcessListener[]>}
   */
  function getListenerWrappersForEvent(eventName) {
    let wrappersByListener = listenerWrappersByEventName.get(eventName);

    if (!wrappersByListener) {
      wrappersByListener = new WeakMap();
      listenerWrappersByEventName.set(eventName, wrappersByListener);
    }

    return wrappersByListener;
  }

  /**
   * @param {TrustedProcessEventName} eventName
   * @param {TrustedProcessListener} listener
   * @param {TrustedProcessListener} wrappedListener
   */
  function registerListenerWrapper(eventName, listener, wrappedListener) {
    const wrappersByListener = getListenerWrappersForEvent(eventName);
    const wrappers = wrappersByListener.get(listener) ?? [];

    wrappers.push(wrappedListener);
    wrappersByListener.set(listener, wrappers);
  }

  /**
   * @param {TrustedProcessEventName} eventName
   * @param {TrustedProcessListener} listener
   * @param {TrustedProcessListener} wrappedListener
   */
  function unregisterListenerWrapper(eventName, listener, wrappedListener) {
    const wrappersByListener = listenerWrappersByEventName.get(eventName);
    const wrappers = wrappersByListener?.get(listener);

    if (!wrappers) return;

    const index = wrappers.lastIndexOf(wrappedListener);

    if (index !== -1) {
      wrappers.splice(index, 1);
    }

    if (wrappers.length === 0) {
      wrappersByListener.delete(listener);
    }
  }

  /**
   * @param {TrustedProcessEventName} eventName
   * @param {TrustedProcessListener} listener
   * @returns {TrustedProcessListener | undefined}
   */
  function unregisterLatestListenerWrapper(eventName, listener) {
    const wrappersByListener = listenerWrappersByEventName.get(eventName);
    const wrappers = wrappersByListener?.get(listener);
    const wrappedListener = wrappers?.pop();

    if (wrappers?.length === 0) {
      wrappersByListener.delete(listener);
    }

    return wrappedListener;
  }

  function cwd() {
    return args.cwd;
  }

  /**
   * @template {TrustedProcessEventName} EventName
   * @param {EventName} eventName
   * @param {TrustedProcessListenerByEvent[EventName]} listener
   * @returns {TrustedProcessFacade}
   */
  function once(eventName, listener) {
    assertAllowedEventListener(eventName, listener);

    /**
     * @param {...any} eventArgs
     */
    function wrappedListener(...eventArgs) {
      unregisterListenerWrapper(eventName, listener, wrappedListener);

      // Do not let EventEmitter bind `this` to the real host process.
      Reflect.apply(listener, undefined, eventArgs);
    }

    registerListenerWrapper(eventName, listener, wrappedListener);
    args.process.once(eventName, wrappedListener);

    return facade;
  }

  /**
   * @template {TrustedProcessEventName} EventName
   * @param {EventName} eventName
   * @param {TrustedProcessListenerByEvent[EventName]} listener
   * @returns {TrustedProcessFacade}
   */
  function off(eventName, listener) {
    assertAllowedEventListener(eventName, listener);

    const wrappedListener = unregisterLatestListenerWrapper(
      eventName,
      listener,
    );

    if (wrappedListener) {
      args.process.off(eventName, wrappedListener);
    }

    return facade;
  }

  const facade = Object.freeze({
    arch: args.process.arch,
    cwd,
    env: args.env,
    off,
    once,
    pid: args.process.pid,
    platform: args.process.platform,
  });

  assertFacadePropertyNames(facade);

  return facade;
}

/** @type {Set<TrustedProcessEventName>} */
const allowedEventNames = new Set(["exit"]);

/**
 * @template {TrustedProcessEventName} EventName
 * @param {EventName} eventName
 * @param {TrustedProcessListenerByEvent[EventName]} listener
 */
function assertAllowedEventListener(eventName, listener) {
  if (!allowedEventNames.has(eventName)) {
    const debug = JSON.stringify({ eventName, allowedEventNames });
    throw new Error(`process listener event unsupported ${debug}`);
  }

  if (typeof listener !== "function") {
    throw new TypeError("process listener must be a function");
  }
}

/**
 * @param {object} facade
 */
function assertFacadePropertyNames(facade) {
  const expected = new Set(PROPERTY_LIST);
  const actual = new Set(Reflect.ownKeys(facade));

  const missing = expected.difference(actual);
  if (missing.size) {
    throw new Error(`process missing (${[...missing].join(", ")})`);
  }

  const unexpected = actual.difference(expected);
  if (unexpected.size) {
    throw new Error(`process unexpected (${[...unexpected].join(", ")})`);
  }
}

module.exports = Object.freeze({
  create,
  PROPERTY_LIST,
});
