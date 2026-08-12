const { AsyncLocalStorage } = require("node:async_hooks");
const { performance } = require("node:perf_hooks");

const responseMetaTraceVersion = 1;
// Reserve room for nested CDP spans and their enclosing command span. At 128,
// children could fill the buffer before the command span ended.
const maxResponseMetaTraceSpans = 1024;
const maxResponseMetaTraceAttrs = 32;
const maxResponseMetaTraceAttrKeyLength = 128;
const maxResponseMetaTraceNameLength = 128;
const maxResponseMetaTraceAttrStringLength = 256;

function roundTraceMs(value) {
  return Math.round(value * 1000) / 1000;
}

function isPlainObject(value) {
  return (
    value !== null &&
    typeof value === "object" &&
    (Object.getPrototypeOf(value) === Object.prototype ||
      Object.getPrototypeOf(value) === null)
  );
}

function sanitizeTraceAttrValue(value) {
  if (typeof value === "boolean") {
    return value;
  }
  if (typeof value === "number") {
    return Number.isFinite(value) ? value : undefined;
  }
  if (typeof value === "string") {
    return value.length <= maxResponseMetaTraceAttrStringLength
      ? value
      : value.slice(0, maxResponseMetaTraceAttrStringLength);
  }
  return undefined;
}

function sanitizeTraceName(value) {
  const name = String(value);
  if (name.length === 0) {
    return "unknown";
  }
  return name.length <= maxResponseMetaTraceNameLength
    ? name
    : name.slice(0, maxResponseMetaTraceNameLength);
}

function sanitizeTraceAttrs(value) {
  if (!isPlainObject(value)) {
    return {};
  }

  const attrs = {};
  let attrCount = 0;
  for (const [key, rawValue] of Object.entries(value)) {
    if (
      typeof key !== "string" ||
      key.length === 0 ||
      key.length > maxResponseMetaTraceAttrKeyLength
    ) {
      continue;
    }
    const sanitizedValue = sanitizeTraceAttrValue(rawValue);
    if (sanitizedValue === undefined) {
      continue;
    }
    attrs[key] = sanitizedValue;
    attrCount += 1;
    if (attrCount >= maxResponseMetaTraceAttrs) {
      break;
    }
  }
  return attrs;
}

function createResponseMetaTracer({ enabled, getCurrentExecState }) {
  const spanStorage = new AsyncLocalStorage();

  function buildTrace(execState) {
    if (!enabled || execState.telemetrySpans.length === 0) {
      return null;
    }

    const trace = {
      version: responseMetaTraceVersion,
      spans: execState.telemetrySpans
        .slice()
        .sort((a, b) => a.start_ms - b.start_ms),
    };
    if (execState.telemetryDroppedSpanCount > 0) {
      trace.dropped_span_count = execState.telemetryDroppedSpanCount;
    }
    return trace;
  }

  function makeNoopTelemetrySpan() {
    return Object.freeze({
      end() {},
    });
  }

  function telemetryStatus(value) {
    return value === "error" ? "error" : "ok";
  }

  function telemetryErrorKind(error) {
    return error instanceof Error && error.name ? error.name : typeof error;
  }

  function objectAttrs(value) {
    return value && typeof value === "object" && !Array.isArray(value)
      ? value
      : {};
  }

  function currentParentSpanId() {
    const activeSpan = spanStorage.getStore();
    return typeof activeSpan?.spanId === "string" ? activeSpan.spanId : null;
  }

  function startSpan(name, attrs = {}) {
    if (!enabled) {
      return { span: makeNoopTelemetrySpan() };
    }

    let execState;
    try {
      execState = getCurrentExecState();
    } catch {
      return { span: makeNoopTelemetrySpan() };
    }

    const spanId = `span-${++execState.telemetrySpanCounter}`;
    const parentSpanId = currentParentSpanId();
    const startMs = performance.now();
    let ended = false;

    const span = Object.freeze({
      end(options = {}) {
        if (ended) {
          return;
        }
        ended = true;

        const endMs = performance.now();
        if (execState.telemetrySpans.length >= maxResponseMetaTraceSpans) {
          execState.telemetryDroppedSpanCount += 1;
          return;
        }

        const startAttrs = objectAttrs(attrs);
        const endAttrs = objectAttrs(options.attrs);
        const record = {
          id: spanId,
          name: sanitizeTraceName(name),
          start_ms: roundTraceMs(startMs - execState.telemetryStartedAtMs),
          duration_ms: roundTraceMs(endMs - startMs),
          status: telemetryStatus(options.status),
          attrs: sanitizeTraceAttrs({ ...startAttrs, ...endAttrs }),
        };
        if (parentSpanId != null) {
          record.parent_id = parentSpanId;
        }
        execState.telemetrySpans.push(record);
      },
    });

    return { span, spanId };
  }

  function resultAttrsFor(result, resultAttrs) {
    if (typeof resultAttrs !== "function") {
      return undefined;
    }
    try {
      const attrs = resultAttrs(result);
      if (attrs && typeof attrs === "object" && !Array.isArray(attrs)) {
        return attrs;
      }
    } catch {
      // Telemetry must not affect runtime behavior.
    }
    return undefined;
  }

  const bridge = Object.freeze({
    startSpan(name, attrs = {}) {
      return startSpan(name, attrs).span;
    },

    async withSpan(name, attrs = {}, operation, options = {}) {
      if (typeof operation !== "function") {
        return undefined;
      }

      const resultAttrs =
        options && typeof options.resultAttrs === "function"
          ? options.resultAttrs
          : null;
      const { span, spanId } = startSpan(name, attrs);
      const run = async () => {
        try {
          const result = await operation();
          span.end({ attrs: resultAttrsFor(result, resultAttrs), status: "ok" });
          return result;
        } catch (error) {
          span.end({
            attrs: { "error.kind": telemetryErrorKind(error) },
            status: "error",
          });
          throw error;
        }
      };

      if (!spanId) {
        return await run();
      }
      return await spanStorage.run({ spanId }, run);
    },
  });

  return Object.freeze({
    bridge,
    buildTrace,
  });
}

module.exports = {
  createResponseMetaTracer,
};
