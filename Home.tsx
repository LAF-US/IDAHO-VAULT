import { Mail, Linkedin, ExternalLink, Play } from "lucide-react";

/**
 * Design Philosophy: The Gemstone Aesthetic
 * - Clean white background with dark text
 * - Bold blue accent color for emphasis
 * - Minimalist, editorial layout
 * - Geometric elements and decorative touches
 * - High contrast, modern typography
 * - Plenty of whitespace
 */

export default function Home() {
  return (
    <div className="min-h-screen bg-white text-black">
      {/* Header */}
      <header className="border-b border-gray-200">
        <div className="container py-8 flex items-center justify-between">
          <div className="text-2xl font-bold tracking-tight">Logan Finney</div>
          <nav className="hidden md:flex gap-8 text-sm font-medium">
            <a href="#about" className="hover:text-blue-600 transition-colors">
              About
            </a>
            <a href="#work" className="hover:text-blue-600 transition-colors">
              Work
            </a>
            <a href="#contact" className="hover:text-blue-600 transition-colors">
              Contact
            </a>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="border-b border-gray-200">
        <div className="container py-20 md:py-28">
          <div className="max-w-3xl">
            <h1 className="text-6xl md:text-7xl font-bold leading-tight mb-6 tracking-tight">
              Documentary Journalist
            </h1>
            <p className="text-xl text-gray-700 mb-8 leading-relaxed max-w-2xl">
              I investigate stories that matter—uncovering truth through rigorous reporting and documentary filmmaking. Based in Idaho, I cover politics, government, and the people affected by policy.
            </p>

            <div className="flex gap-4">
              <a
                href="mailto:logan.finney@idahoptv.org"
                className="px-6 py-3 bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors"
              >
                Get in Touch
              </a>
              <a
                href="#work"
                className="px-6 py-3 border-2 border-black font-medium hover:bg-black hover:text-white transition-colors"
              >
                View Work
              </a>
            </div>

            {/* Social Links */}
            <div className="flex gap-6 mt-12">
              <a
                href="https://www.linkedin.com/in/loganfinney"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-blue-600 transition-colors"
                aria-label="LinkedIn"
              >
                <Linkedin className="w-6 h-6" />
              </a>
              <a
                href="https://www.youtube.com/@loganfinney"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-blue-600 transition-colors"
                aria-label="YouTube"
              >
                <Play className="w-6 h-6" />
              </a>
              <a
                href="mailto:logan.finney@idahoptv.org"
                className="text-gray-600 hover:text-blue-600 transition-colors"
                aria-label="Email"
              >
                <Mail className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="border-b border-gray-200">
        <div className="container py-20">
          <div className="max-w-3xl">
            <h2 className="text-4xl font-bold mb-8 tracking-tight">About</h2>

            <div className="space-y-6 text-lg text-gray-700 leading-relaxed">
              <p>
                I'm an award-winning professional journalist who specializes in covering politics, government, and policy. A North Idaho native, I grew up in the mountains of Bonner County and have maintained a lifelong fascination with Idaho's history, culture, and politics.
              </p>

              <p>
                My work focuses on investigating stories that reveal the intersection of policy, politics, and people. Through documentary filmmaking and multimedia production, I aim to illuminate the issues that shape our communities.
              </p>

              <p>
                I serve as a Producer/Writer at Idaho Public Television (PBS), creating documentary content and investigative journalism for the "Idaho Reports" series. My reporting has appeared across multiple platforms including FāVS News, Idaho Capital Sun, and Stonewall News Northwest.
              </p>
            </div>

            {/* Skills */}
            <div className="mt-12 pt-12 border-t border-gray-200">
              <h3 className="text-sm font-bold uppercase tracking-widest text-gray-600 mb-6">
                Core Skills
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {[
                  "Investigative Reporting",
                  "Documentary Filmmaking",
                  "Video Production",
                  "Podcast Production",
                  "Political Coverage",
                  "Policy Analysis",
                ].map((skill) => (
                  <div key={skill} className="text-sm font-medium text-gray-700">
                    {skill}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Work */}
      <section id="work" className="border-b border-gray-200">
        <div className="container py-20">
          <h2 className="text-4xl font-bold mb-12 tracking-tight">Work</h2>

          <div className="max-w-3xl">
            {/* Idaho Reports */}
            <div className="mb-16">
              <h3 className="text-2xl font-bold mb-2">Idaho Reports</h3>
              <p className="text-gray-600 mb-8">
                Producer and host of Idaho Reports—a comprehensive news program covering state government, policy, and politics.
              </p>

              <div className="space-y-6">
                {[
                  {
                    title: "The Price of Power",
                    subtitle: "Data Centers & Public Utilities",
                    date: "April 2026",
                  },
                  {
                    title: "Social Media Regulation",
                    subtitle: "Addictive Technology Policy",
                    date: "March 2026",
                  },
                  {
                    title: "Budget Analysis Series",
                    subtitle: "State Appropriations & Policy",
                    date: "February–March 2026",
                  },
                  {
                    title: "Immigration Enforcement",
                    subtitle: "ACLU Lawsuit & Community Impact",
                    date: "February 2026",
                  },
                ].map((item, idx) => (
                  <div key={idx} className="pb-6 border-b border-gray-200 last:border-b-0">
                    <div className="flex justify-between items-start gap-4">
                      <div>
                        <h4 className="font-bold text-black">{item.title}</h4>
                        <p className="text-sm text-gray-600">{item.subtitle}</p>
                      </div>
                      <p className="text-sm text-gray-500 whitespace-nowrap">{item.date}</p>
                    </div>
                  </div>
                ))}
              </div>

              <a
                href="https://authory.com/loganfinney"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 mt-8 text-blue-600 font-medium hover:text-blue-700"
              >
                Full Portfolio <ExternalLink className="w-4 h-4" />
              </a>
            </div>

            {/* Articles */}
            <div className="pt-12 border-t border-gray-200">
              <h3 className="text-2xl font-bold mb-2">Articles</h3>
              <p className="text-gray-600 mb-8">
                Reporting published across major news outlets.
              </p>

              <div className="space-y-6">
                {[
                  {
                    title: "Idaho bill to label products made with fetal cells dies in Senate committee",
                    publication: "Idaho Capital Sun & FāVS News",
                  },
                  {
                    title: "Boise Jewish congregation welcomes new rabbi, restores century-old Torah scrolls",
                    publication: "Idaho Capital Sun",
                  },
                  {
                    title: "LGBTQ+ Rights & Equality Coverage",
                    publication: "Stonewall News Northwest",
                  },
                ].map((item, idx) => (
                  <div key={idx} className="pb-6 border-b border-gray-200 last:border-b-0">
                    <h4 className="font-bold text-black mb-1">{item.title}</h4>
                    <p className="text-sm text-gray-600">{item.publication}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Publications */}
      <section className="border-b border-gray-200">
        <div className="container py-20">
          <h3 className="text-sm font-bold uppercase tracking-widest text-gray-600 mb-8">
            Published Across
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6 text-sm text-gray-700 max-w-3xl">
            {[
              "Idaho Public Television",
              "Idaho Capital Sun",
              "FāVS News",
              "Stonewall News Northwest",
              "Big Country News Connection",
              "Boise State Public Radio",
              "The Argonaut",
              "Idaho Education News",
              "InvestigateWest",
            ].map((source) => (
              <div key={source}>{source}</div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact */}
      <section id="contact" className="border-b border-gray-200">
        <div className="container py-20">
          <div className="max-w-3xl">
            <h2 className="text-4xl font-bold mb-6 tracking-tight">Get in Touch</h2>
            <p className="text-xl text-gray-700 mb-8">
              Interested in discussing investigative journalism, documentary work, or collaboration opportunities?
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="mailto:logan.finney@idahoptv.org"
                className="px-6 py-3 bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors"
              >
                Email
              </a>
              <a
                href="https://www.linkedin.com/in/loganfinney"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 border-2 border-black font-medium hover:bg-black hover:text-white transition-colors"
              >
                LinkedIn
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-gray-200">
        <div className="container text-center text-sm text-gray-600">
          <p>© 2026 Logan Finney</p>
        </div>
      </footer>
    </div>
  );
}
