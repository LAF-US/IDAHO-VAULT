// Trusted-only bridge for host-mediated capabilities.

const {
  createPrivilegedNodeReplConfig,
} = require("./privileged-node-repl-config.js");

function createPrivilegedNodeReplBridge({
  addAfterSubmittedCodeHook,
  authenticatedFetch,
  createElicitation,
  env,
  getCurrentExecState,
  isPlainObject,
  makeRejectedThenable,
  nativePipe,
  nodeRepl,
  pendingPrivilegedNodeReplRequests,
  privilegedBridgeAuthToken,
  send,
  telemetryBridge,
  trackExecBackgroundOperation,
}) {
  let privilegedNodeReplRequestCounter = 0;

  function sendPrivileged(execState, message) {
    send({
      ...message,
      exec_id: execState.id,
      token: privilegedBridgeAuthToken,
    });
  }

  function handlePrivilegedNodeReplOperation(operationName, buildPayload) {
    let execState;
    try {
      execState = getCurrentExecState();
    } catch (error) {
      return makeRejectedThenable(error);
    }

    const operation = (async () => {
      const payload = await buildPayload();
      const id = `${execState.id}-privileged-node-repl-${privilegedNodeReplRequestCounter++}`;
      sendPrivileged(execState, {
        ...payload,
        id,
      });
      return new Promise((resolve, reject) => {
        pendingPrivilegedNodeReplRequests.set(id, (res) => {
          if (!res.ok) {
            reject(new Error(res.error || `${operationName} failed`));
            return;
          }
          resolve(res.value ?? {});
        });
      });
    })();

    return trackExecBackgroundOperation(execState, operation);
  }

  function withSuspendedTimeout(fn) {
    let execState;
    try {
      execState = getCurrentExecState();
      if (typeof fn !== "function") {
        throw new Error("nodeRepl.withSuspendedTimeout expected a function");
      }
    } catch (error) {
      return makeRejectedThenable(error);
    }

    const operation = (async () => {
      sendPrivileged(execState, {
        type: "suspend_timeout",
      });
      try {
        return await fn();
      } finally {
        sendPrivileged(execState, {
          type: "resume_timeout",
        });
      }
    })();

    return trackExecBackgroundOperation(execState, operation);
  }

  const privilegedNodeReplConfig = createPrivilegedNodeReplConfig({
    handlePrivilegedNodeReplOperation,
    isPlainObject,
  });
  const launchServices = Object.freeze({
    openApplication(target) {
      return handlePrivilegedNodeReplOperation(
        "nodeRepl.launchServices.openApplication",
        async () => {
          const normalized = normalizeLaunchServicesTarget(
            await target,
            isPlainObject,
          );
          return {
            type: "launch_services_action",
            action: "open_application",
            application_path: normalized.applicationPath,
            bundle_identifier: normalized.bundleIdentifier,
          };
        },
      );
    },
  });

  const privilegedNodeReplProperties = {
    addAfterSubmittedCodeHook: {
      configurable: false,
      enumerable: true,
      value: addAfterSubmittedCodeHook,
      writable: false,
    },
    gaasBrowserConfig: {
      configurable: false,
      enumerable: true,
      get() {
        return getCurrentExecState().gaasBrowserConfig;
      },
    },
    launchServices: {
      configurable: false,
      enumerable: true,
      value: launchServices,
      writable: false,
    },
    config: {
      configurable: false,
      enumerable: true,
      value: privilegedNodeReplConfig,
      writable: false,
    },
    env: {
      configurable: false,
      enumerable: true,
      value: env,
      writable: false,
    },
    createElicitation: {
      configurable: false,
      enumerable: true,
      value(request) {
        return createElicitation(request, privilegedBridgeAuthToken);
      },
      writable: false,
    },
    fetch: {
      configurable: false,
      enumerable: true,
      value(input, init) {
        return authenticatedFetch(input, init, privilegedBridgeAuthToken);
      },
      writable: false,
    },
    nativePipe: {
      configurable: false,
      enumerable: true,
      value: nativePipe,
      writable: false,
    },
    emitContentItem: {
      configurable: false,
      enumerable: true,
      value(text) {
        if (typeof text !== "string") {
          throw new Error("nodeRepl.emitContentItem expected a string");
        }
        getCurrentExecState().contentItems.push(text);
      },
      writable: false,
    },
    withSuspendedTimeout: {
      configurable: false,
      enumerable: true,
      value: withSuspendedTimeout,
      writable: false,
    },
  };
  if (telemetryBridge != null) {
    privilegedNodeReplProperties.telemetry = {
      configurable: false,
      enumerable: true,
      value: telemetryBridge,
      writable: false,
    };
  }

  return Object.freeze(Object.create(nodeRepl, privilegedNodeReplProperties));
}

function normalizeLaunchServicesTarget(target, isPlainObject) {
  if (!isPlainObject(target)) {
    throw new Error(
      "nodeRepl.launchServices.openApplication expected a target object",
    );
  }
  const unexpectedKeys = Object.keys(target).filter(
    (key) => key !== "applicationPath" && key !== "bundleIdentifier",
  );
  if (unexpectedKeys.length > 0) {
    throw new Error(
      "nodeRepl.launchServices.openApplication received an unsupported target",
    );
  }
  const applicationPath = nonEmptyString(target.applicationPath);
  const bundleIdentifier = nonEmptyString(target.bundleIdentifier);
  if ((applicationPath == null) === (bundleIdentifier == null)) {
    throw new Error(
      "nodeRepl.launchServices.openApplication expected exactly one of applicationPath or bundleIdentifier",
    );
  }
  return { applicationPath, bundleIdentifier };
}

function nonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0
    ? value.trim()
    : undefined;
}

module.exports = {
  createPrivilegedNodeReplBridge,
};
