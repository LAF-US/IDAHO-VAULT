import assert from "node:assert/strict";

async function settleSelectionUi(page) {
  await page.evaluate(
    () =>
      new Promise((resolveFrame) => {
        requestAnimationFrame(() => requestAnimationFrame(resolveFrame));
      }),
  );
}

export async function verifyAskChatGPTSelectionContext(page, { componentTitle, selectedContextIncludes }) {
  const actions = page.getByRole("dialog", { name: "Selection actions" });
  await actions.getByRole("button", { name: "Ask ChatGPT", exact: true }).click();
  const composer = page.getByRole("dialog", { name: "Ask ChatGPT about this dashboard" });
  const questionInput = composer.getByRole("textbox", { name: "Question for ChatGPT" });
  const question = "Explain this selected dashboard evidence.";
  await questionInput.fill(question);
  const sendLink = composer.getByRole("link", { name: "Send to ChatGPT" });
  await sendLink.waitFor();
  const href = new URL(await sendLink.getAttribute("href"));
  const prompt = href.searchParams.get("prompt") ?? href.searchParams.get("q");
  assert.ok(prompt, "Selection actions must construct a real question handoff");
  assert.equal(
    prompt.split("\n").at(-1),
    `Question: ${question}`,
    "The selected-context handoff must retain the entered question as its final labeled line",
  );
  assert.ok(
    prompt.includes(`Chart: ${componentTitle}\n`),
    "The question must refer to the selected component, not the entire dashboard",
  );
  const selectedContext = /^Selected (?:point|context): (.+)$/mu.exec(prompt)?.[1];
  assert.ok(
    selectedContext && selectedContext !== "Entire dashboard",
    "Selection actions must retain nonempty selected evidence",
  );
  if (selectedContextIncludes) {
    assert.ok(selectedContext.includes(selectedContextIncludes), "The handoff must retain the selected label or text");
  }
  await questionInput.fill("");
  await page.keyboard.press("Escape");
  await composer.waitFor({ state: "hidden" });
}

export async function verifyEditorAskChatGPTSelectionModes(page) {
  const selectedBar = page.locator('[data-component-id="segment-breakdown"] .chart-ranked-list-row').first();
  await selectedBar.scrollIntoViewIfNeeded();
  await page.getByRole("button", { name: "Edit text and layout" }).click();
  await selectedBar.click();
  await settleSelectionUi(page);
  assert.equal(
    await page.getByRole("dialog", { name: "Selection actions" }).count(),
    0,
    "Ask ChatGPT must stay hidden in edit mode",
  );
  assert.equal(
    await page.locator(".dashboard-ask-selected-region").count(),
    0,
    "Edit mode must not show chart-selection regions",
  );
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await page.getByRole("button", { name: "Edit text and layout" }).waitFor();

  await selectedBar.click();
  await settleSelectionUi(page);
  await page.getByRole("dialog", { name: "Selection actions" }).waitFor();
  assert.equal(
    await page.getByRole("dialog", { name: "Selection actions" }).count(),
    1,
    "Ordinary file/browser viewers may select marks regardless of edit permission",
  );
  await page.keyboard.press("Escape");
}

export async function verifyViewerAskChatGPTHandoff(page) {
  await page.evaluate(() => {
    const marker = document.createElement("meta");
    marker.name = "data-app-sites-project";
    marker.content = "appgprj_browser_handoff";
    document.head.append(marker);
  });
  const selectedBar = page.locator('[data-component-id="segment-breakdown"] .chart-ranked-list-row').first();
  await selectedBar.scrollIntoViewIfNeeded();
  await selectedBar.click();
  await settleSelectionUi(page);

  const selectionActions = page.getByRole("dialog", {
    name: "Selection actions",
  });
  await selectionActions.waitFor();
  await selectionActions.getByRole("button", { name: "Ask ChatGPT" }).click();
  const composer = page.getByRole("dialog", {
    name: "Ask ChatGPT about this dashboard",
  });
  await composer.waitFor();
  assert.equal(
    await composer.getByText("Send to ChatGPT", { exact: true }).count(),
    0,
    "The handoff label must stay hidden until the viewer enters a question",
  );

  const viewerQuestion = "What explains this segment?";
  await composer.getByRole("textbox", { name: "Question for ChatGPT" }).fill(viewerQuestion);
  const sendLink = composer.getByRole("link", { name: "Send to ChatGPT" });
  assert.equal(
    await sendLink.getAttribute("target"),
    "_blank",
    "Hosted web handoffs must preserve the dashboard in a separate tab",
  );
  assert.deepEqual(
    await sendLink.locator(".dashboard-ask-primary").evaluate((button) => {
      const bounds = button.getBoundingClientRect();
      return {
        width: bounds.width,
        height: bounds.height,
        radius: getComputedStyle(button).borderRadius,
      };
    }),
    { width: 28, height: 28, radius: "50%" },
    "The handoff action must use the 28px circular system button",
  );

  await sendLink.click();
  await page.waitForFunction(() => window.__dashboardDeepLinks.length === 1);
  const chatGPTLink = new URL((await page.evaluate(() => window.__dashboardDeepLinks))[0]);
  const chatGPTPrompt = chatGPTLink.searchParams.get("q");
  assert.equal(`${chatGPTLink.origin}${chatGPTLink.pathname}`, "https://chatgpt.com/");
  assert.deepEqual([...chatGPTLink.searchParams.keys()], ["q"]);
  assert.match(
    chatGPTPrompt,
    /^Answer this question about \[Product adoption and engagement\]\(sites-project:\/\/appgprj_browser_handoff\):\nChart: Active accounts by feature\nSelected point: .+\nQuestion: What explains this segment\?$/u,
    "The hosted handoff must use the compact Site, chart, selected-point, and question format",
  );
  assert.doesNotMatch(chatGPTPrompt, /Dashboard URL:|token=secret|#private-section/u);
  await composer.waitFor({ state: "hidden" });
  assert.equal(await composer.count(), 0, "The composer must close after handing the question to ChatGPT");
  await page.evaluate(() => {
    window.__dashboardDeepLinks = [];
  });

  const externalUserAgent = await page.evaluate(() => navigator.userAgent);
  try {
    for (const userAgent of [externalUserAgent, "CodexBrowser/1.0"]) {
      const desktop = userAgent === "CodexBrowser/1.0";
      await page.evaluate((value) => Object.defineProperty(navigator, "userAgent", { configurable: true, value }), userAgent);
      await page.getByRole("button", { name: "Ask ChatGPT", exact: true }).click();
      const dashboardComposer = page.getByRole("dialog", {
        name: "Ask ChatGPT about this dashboard",
      });
      const dashboardQuestion = "What should I know about this dashboard?";
      await dashboardComposer.getByRole("textbox", { name: "Question for ChatGPT" }).fill(dashboardQuestion);
      const dashboardSend = dashboardComposer.getByRole("link", { name: "Send to ChatGPT" });
      assert.equal(await dashboardSend.getAttribute("target"), desktop ? "_self" : "_blank");
      await dashboardSend.click();
      await page.waitForFunction(() => window.__dashboardDeepLinks.length === 1);
      const dashboardLink = new URL((await page.evaluate(() => window.__dashboardDeepLinks))[0]);
      assert.equal(`${dashboardLink.protocol}//${dashboardLink.host}${dashboardLink.pathname}`,
        desktop ? "codex://new" : "https://chatgpt.com/");
      assert.deepEqual([...dashboardLink.searchParams.keys()], desktop ? ["prompt", "browserUrl"] : ["q"]);
      if (desktop) assert.equal(dashboardLink.searchParams.get("browserUrl"), "https://dashboard.chatgpt.site/published");
      assert.equal(
        dashboardLink.searchParams.get(desktop ? "prompt" : "q"),
        `Answer this question about [Product adoption and engagement](sites-project://appgprj_browser_handoff):\nSelected context: Entire dashboard\nQuestion: ${dashboardQuestion}`,
        "Both browsers must retain the whole-dashboard question context",
      );
      await dashboardComposer.waitFor({ state: "hidden" });
      await page.evaluate(() => { window.__dashboardDeepLinks = []; });
    }
  } finally {
    await page.evaluate((value) => Object.defineProperty(navigator, "userAgent", { configurable: true, value }), externalUserAgent);
  }
}
