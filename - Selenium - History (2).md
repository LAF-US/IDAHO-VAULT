---
source: "https://www.selenium.dev/history/"
author:
published:
created: 2026-04-20
---
## Selenium History

> [!green] The story starts in 2004
> The story starts in 2004 at ThoughtWorks in Chicago, with Jason Huggins building the Core mode as "JavaScriptTestRunner" for the testing of an internal Time and Expenses application (Python, Plone). Automatic testing of any applications is core to ThoughtWork's style, given the Agile leanings of this consultancy. He has help from Paul Gross and Jie Tina Wang. For them, this was a day job.
> 
> Jason started demoing the test tool to various colleagues. Many were excited about its immediate and intuitive visual feedback, as well as its potential to grow as a reusable testing framework for other web applications.
> 
> Soon after in 2004 fellow ThoughtWorker Paul Hammant saw the demo, and started discussions about the open sourcing of Selenium, as well as defining a 'driven' mode of Selenium where you'd get to use Selenium over the wire from a language of your choice, that would get around the 'same origin policy'. Other (then) colleagues, Aslak Hellesoy and Mike Melia, experimented with different ideas for the 'server' piece, including page rewriting to get around the same origin policy. Paul wrote the original server piece in Java, and Aslak and Obie Fernandez ported that the client driver to Ruby, setting the foundation for drivers in yet more languages.
> 
> ThoughtWorkers in various offices around the world picked up Selenium for commercial projects, and contributed back to Selenium from the lessons learned on these projects. Mike Williams, Darrell Deboer, and Darren Cotterill all helped with the increasing the capabilities and the robustness of it.

> [!orange] Meanwhile, outside of ThoughtWorks...
> At Bea, Dan Fabulich and Nelson Sproul came to the conclusion that the driver/server to browser architecture was not the most useful or flexible, so forked the driver coder and crafted that into a standalone server that leveraged and bundled MortBay's Jetty as a web-proxy. When the code was merged back it became known as "Selenium Remote Control" and the old driven codeline and capability was retired.
> 
> Pat Lightbody became involved at the same time, with a commercial idea that required him to quit his day job (Jive Software). The idea was "Hosted QA", and it was eventually moved into Gomez's service line. Pat worked with Dan and Nelson making Selenium RC stable for large scale deployment. Pat had privately coded a grid for Hosted QA that took screenshots of browsers in various states, and was looking after multiple customers concurrently. Jason had the same hosted QA idea a year before, but did not quit his day job to do it.
> 
> In 2007 Dan moved to the rapidly growing Redfin, which also part-time sponsors his time on Selenium, and encourages a speaking agenda.

> [!cyan] Selenium IDE: Made in Japan
> Shinya Kasatani in Japan became interested in Selenium, and realised that he could wrap the core code into an IDE module into the Firefox browser, and be able to record tests as well as play them back in the same plugin. This tool, turned out an eye opener in more ways that was originally thought as it is not bound to the same origin policy.
> 
> Mike Williams got involved again in the Summer of 2006 where he led a team from ThoughWorks China, primarily Wang Peng Chao, Huang Liang and Xiong Jie but with the help of others. They worked on improving Selenium Core with the goal of getting it closer to 1.0

> [!blue] Google Too!
> Jason Huggins left Thoughtworks in 2007 and joined the (then secret) Selenium support team inside Google.
> 
> Jennifer Bevan (and other unnamed Googlers) had coded their own grid capabilty for Selenium RC, and deployed it internally for the testing of multiple public web applications. Google hosted a GTAC conference in New York and talked about their use of Selenium for the first time. Jennifer soon became a committer on the Selenium projects.
> 
> Haw-bin Chai in Chicago provided patches for XPath functionality and developed an extension called "UI Element" that makes the grammar of locators much simpler. He was invited into the Selenium development team in 2007.
> 
> Simon Stewart at ThoughtWorks had been working on a different web testing tool called WebDriver. It did not rely on JavaScript to do the heavy lifting, but instead had a client for each browser that was coded from scratch. It also had a 'higher level' API than Selenium-RC and showed lots of promise. Simon presented the tool at GTAC, and started work on compatibility with Selenium-RC, which gave rise to the obvious conclusion that the two projects should merge. Simon, at Google from 2007 to 2012, but later at Facebook, Deliveroo, and Apple, got to spend some of his time making that a reality.