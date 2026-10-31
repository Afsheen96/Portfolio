"""Builds every page of the portfolio from one place.

All pages share the same header, footer and project data, so instead of
copying them into each HTML file by hand they are written here and the
HTML files are generated:

    python3 tools/build.py

Edit the PROJECTS list or the page functions below, run the command, then
commit the changed HTML files. Social links are NOT here: they live in
config.js so they can be changed without rebuilding.
"""
import html
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://afsheen96.github.io/Portfolio/'
FORM_ENDPOINT = 'https://formspree.io/f/xpzebdqb'
YEAR = '2026'
E = html.escape

# ---------------------------------------------------------------- icons
ICON = {
    'arrow': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'back': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
    'ext': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    'code': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>',
    'check': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
    'eye': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    'desktop': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>',
    'tablet': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M11 18h2"/></svg>',
    'phone': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 17h2"/></svg>',
    'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>',
    'star': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/></svg>',
    'layout': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M8 21h8"/></svg>',
    'spark': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/></svg>',
    'refresh': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8 8 0 0 0-14.9-3M4 4v4h4M4 13a8 8 0 0 0 14.9 3M20 20v-4h-4"/></svg>',
    'search': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>',
    'rocket': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15c-1.5 1.3-2 4-2 6 2 0 4.7-.5 6-2M9 15l-3-3c1-4 4.5-8 12-9-1 7.5-5 11-9 12z"/><circle cx="15" cy="9" r="1.5"/></svg>',
    'chat': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
    'globe': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>',
    'book': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 21V5M19 19v2H6"/></svg>',
    'handshake': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 11l3-3 3 2 4-4 3 3-7 7a2 2 0 0 1-3 0l-1-1M3 10l4-4 3 2"/></svg>',
    'clock': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'pin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
    'briefcase': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/></svg>',
    'chev': '<svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
    'send': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/></svg>',
}

BRAND = {
    'email': ('Gmail', '<svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true">'
              '<path fill="#4285F4" d="M1.6 21h3.8v-9.2L0 7.7v11.7C0 20.3.7 21 1.6 21z"/>'
              '<path fill="#34A853" d="M18.6 21h3.8c.9 0 1.6-.7 1.6-1.6V7.7l-5.4 4.1z"/>'
              '<path fill="#FBBC04" d="M18.6 4.6v7.2L24 7.7V5.5c0-2-2.3-3.2-3.9-2z"/>'
              '<path fill="#EA4335" d="M5.4 11.8V4.6L12 9.5l6.6-4.9v7.2L12 16.7z"/>'
              '<path fill="#C5221F" d="M0 5.5v2.2l5.4 4.1V4.6L3.9 3.5C2.3 2.3 0 3.5 0 5.5z"/></svg>'),
    'linkedin': ('LinkedIn', '<svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A66C2" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>'),
    'github': ('GitHub', '<svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#181717" d="M12 .3a12 12 0 0 0-3.8 23.38c.6.12.82-.26.82-.58v-2.04c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.5 1 .1-.78.42-1.31.76-1.61-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.1-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.64 1.66.24 2.88.12 3.18a4.65 4.65 0 0 1 1.23 3.22c0 4.61-2.8 5.62-5.48 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.83.58A12 12 0 0 0 12 .3"/></svg>'),
}

# ---------------------------------------------------------------- projects
# Order matters: this is the order everywhere on the site.
PROJECTS = [
    dict(
        slug='hightechzone', name='HighTechZone', full='HighTechZone',
        short='AI tools, tech guides and digital skills',
        tagline='A multi-page technology learning website with AI tool guides, tech tips, digital-skills tutorials, free resources and interactive tools.',
        card='My own technology learning website: AI tool guides, tech tips, digital-skills tutorials and interactive tools, with a bold animated dark design.',
        client='Personal', role='Founder, Designer &amp; Developer', year='2026', type='Website',
        category='website', featured=True,
        live='https://afsheen96.github.io/HighTechZone/', source='https://github.com/Afsheen96', source_label='GitHub profile',
        tech=['HTML5', 'CSS3', 'JavaScript', 'SEO', 'GitHub Pages', 'Git'],
        desktop='hightechzone-desktop.webp', mobile='hightechzone-mobile.webp', og='hightechzone.jpg',
        gallery=[('hightechzone-desktop.webp', 'Animated hero with orbiting topic cards'),
                 ('hightechzone-guides.webp', '"Discover Your Next AI Advantage" guide cards'),
                 ('hightechzone-tools.webp', 'Interactive tools and downloadable templates')],
        overview=['HighTechZone is my own website, "Your Gateway to Smarter Technology". It brings AI tool guides, practical tech tips, digital-skills tutorials and free resources together in one place.',
                  'I designed and built it myself with plain HTML, CSS and JavaScript: a bold dark theme with warm gradients, an animated hero, dropdown navigation, a search dialog, FAQ sections, articles and interactive tools such as an AI Prompt Builder, a Password Strength Checker and a Budget Tracker template.'],
        problem=['People who want to learn about AI tools and digital skills usually find the information scattered across many websites, often full of jargon.', 'I wanted one premium-looking, easy-to-explore home for practical guides and tools: a site that works well on every device and costs nothing to host.'],
        built=['I designed the HighTechZone brand and hand-coded a multi-page website with HTML, CSS and JavaScript: a bold dark theme, an animated hero, dropdown navigation for AI Tools, Guides, Projects, Services, About and Contact, a site search dialog, articles and FAQ sections.', 'I also built interactive tools that run in the browser, an AI Prompt Builder and a Password Strength Checker, plus a downloadable Budget Tracker template. SEO basics (meta tags, Open Graph, structured data, sitemap) are built in, and the site is published on GitHub Pages.'],
        result=['HighTechZone is live and hosted for free. Visitors can browse guides, try the tools right in their browser and download templates on a phone, tablet or desktop.', 'It shows that I can create a brand and deliver a complete multi-page website, from design to deployment.'],
        features=[('Animated hero', 'A starry, glowing hero with orbiting topic cards that makes a strong first impression.'),
                  ('Clear multi-page structure', 'AI Tools, Guides, Projects, Services, About and Contact, with dropdown navigation.'),
                  ('Search dialog', 'Visitors can quickly search the site from any page.'),
                  ('Interactive tools', 'AI Prompt Builder and Password Strength Checker that run right in the browser.'),
                  ('Free templates', 'Downloadable resources like a monthly Budget Tracker spreadsheet.'),
                  ('Articles &amp; guides', 'Step-by-step guides on AI writing, creative design and productivity.'),
                  ('FAQ sections', 'Common questions answered in tidy, expandable sections.'),
                  ('SEO-ready', 'Meta tags, Open Graph, structured data, sitemap and robots.txt.'),
                  ('Fully responsive', 'Carefully designed for phones, tablets and desktops.')],
        highlights=[('Multi-page', 'website with its own brand'), ('3', 'interactive tools &amp; templates'), ('100%', 'hand-coded, hosted free on GitHub Pages')],
    ),
    dict(
        slug='learning-ai-lecture-hub', name='Learning AI Lecture Hub', full='Learning AI Lecture Hub',
        short='Searchable AI lecture library',
        tagline='A clean, searchable library that helps learners find and open the Learn Freelancing AI lectures from one organised page.',
        card='A searchable lecture library that puts the Learn Freelancing AI lectures in one place, with instant search, category filters and one-click "Watch Lecture" links.',
        client='Personal (student project)', role='Designer &amp; Developer', year='2026', type='Learning Platform',
        category='website',
        live='https://afsheen96.github.io/lecture-library/', source='https://github.com/Afsheen96/lecture-library', source_label='Source code',
        tech=['HTML5', 'CSS3', 'JavaScript', 'JSON', 'Node.js build script', 'GitHub Actions', 'GitHub Pages'],
        desktop='lecture-hub-desktop.webp', mobile='lecture-hub-mobile.webp', og=None, full_page='lecture-hub-full.webp',
        gallery=[('lecture-hub-desktop.webp', 'Course cover and "Find Your Next Lecture." search'),
                 ('lecture-hub-list.webp', 'Numbered lecture list with categories and Watch Lecture buttons'),
                 ('lecture-hub-search.webp', 'Instant search: typing "SEO" finds the right lecture'),
                 ('lecture-hub-faq.webp', 'About section and Frequently Asked Questions')],
        overview=['Learning AI Lecture Hub (published as "Learn Freelancing AI — Lecture Library") is an independent, student-made page that collects the links to Sir Hisham Sarwar\'s Learn Freelancing AI lectures, so learners can find any lecture in seconds.',
                  'Learners can search by lecture name, number or topic, filter by category (AI &amp; Automation, Freelancing, Web &amp; App Development, Digital Marketing) and open the original video with one click. The page clearly states that it is not an official website and that the videos stay on Facebook.'],
        problem=['The Learn Freelancing AI lecture links were spread across many Facebook posts. Finding one specific lesson again, for example "the SEO one", meant a lot of scrolling, especially on a phone.'],
        built=['I made one organised page. All lectures live in a single lectures.json file, and a small Node.js build script turns them into real HTML that search engines can read.', 'I added instant search by name, number or topic, category filters, numbered lecture cards with "Watch Lecture" buttons, an FAQ and a clear privacy section. GitHub Actions rebuilds and publishes the site on every update, and the page states that it is an independent student project, not an official website.'],
        result=['Learners can find any lecture in seconds and open the original video in one tap, on phone or desktop.', 'Adding a new lecture takes one line of data, and the site publishes itself automatically.'],
        features=[('Instant search', 'Search lectures by name, number or category; results update as you type.'),
                  ('Category filters', 'One-tap filters for AI &amp; Automation, Freelancing, Web &amp; App Development and Digital Marketing.'),
                  ('Numbered lecture cards', 'Each lecture shows its number, title, category tag and a "Watch Lecture" button.'),
                  ('Opens the original video', 'Links open the original lecture on Facebook in a new tab; nothing is copied or re-hosted.'),
                  ('Helpful FAQ', 'Eight answers on searching, watching, Facebook access, topics and updates.'),
                  ('Easy to update', 'All lectures live in one JSON file with a validation script and a step-by-step guide.'),
                  ('Auto-publishing', 'GitHub Actions builds and deploys the site on every push.'),
                  ('Privacy-first analytics', 'Clear privacy section with an option to turn analytics off.'),
                  ('Mobile friendly', 'Designed to be easy to search and tap on a phone.')],
        highlights=[('8', 'lectures organised and searchable'), ('4', 'category filters'), ('1 file', 'to add new lectures')],
    ),
    dict(
        slug='fomi-studio', name='Fomi Studio', full='Fomi Studio: AI Image Workspace',
        short='AI image-generation workspace',
        tagline='A responsive AI image-generation workspace, turned from a design mockup into a real, working Next.js app.',
        card='A responsive AI image-generation workspace built with Next.js from a design mockup, with a working generator, gallery, image viewer and phone, tablet and desktop layouts.',
        client='Hiring Assessment', assessment=True, role='Frontend Developer', year='2026', type='Web App',
        category='webapp',
        live='https://fomi-studio-weld.vercel.app', source='https://github.com/Afsheen96/fomi-studio', source_label='Source code',
        tech=['Next.js', 'React', 'CSS Modules', 'JavaScript', 'Vercel', 'GitHub'],
        desktop='fomi-studio-desktop.webp', mobile='fomi-studio-mobile.webp', og='fomi-studio.jpg',
        gallery=[('fomi-studio-desktop.webp', 'Image Generator workspace with the guided tutorial'),
                 ('../fomi-studio.jpg', 'Prompt panel, references and creations gallery')],
        overview=["I built this as part of a frontend hiring assessment: an AI Image Generator design mockup turned into a real, working Next.js app.",
                  'It includes a model picker, reference uploads, a prompt box with keyboard shortcuts, a mocked API that "generates" images and videos, loading placeholders in the right shape, a masonry gallery, a full-size viewer with keyboard navigation, and a guided tutorial that highlights the real controls.'],
        problem=['As part of a frontend hiring assessment, I was given a static design mockup of an AI Image Generator.', 'A mockup does not show how a product behaves. The task was to make every part of it actually work (generating, waiting, browsing and viewing) on every screen size, without a real AI backend.'],
        built=['I rebuilt the interface in Next.js as reusable React components styled with CSS Modules: a model picker, reference uploads, a prompt box with keyboard shortcuts and a mocked API that "generates" images and videos with realistic waiting times.', 'Loading placeholders match the shape of the coming result, the gallery is a masonry grid and a full-size viewer supports keyboard navigation. A guided tutorial highlights the real controls. Phone, tablet and desktop each get their own layout (on phones the generator becomes a bottom sheet), and the app is deployed on Vercel.'],
        result=['Anyone can test the complete flow through a live link, on any device.', 'The project shows how I turn a static design into a working, responsive and accessible front end.'],
        features=[('Model picker &amp; references', 'Choose a model and add style or character references, just like the original design.'),
                  ('Smart prompt box', 'Keyboard shortcuts: Ctrl + Enter to generate and / to focus the prompt.'),
                  ('Mocked generation API', 'Images and videos "generate" with realistic waiting times, so the full flow can be tested.'),
                  ('Shape-matched loading states', 'Placeholders appear in the exact size and ratio of the coming result.'),
                  ('Masonry gallery &amp; viewer', 'A tidy gallery with a full-size viewer you can move through with the keyboard.'),
                  ('Guided tutorial', 'A step-by-step tour that highlights the real controls for first-time users.'),
                  ('Three real layouts', 'Phone, tablet and desktop each get their own layout, not just a squeezed one.'),
                  ('Fast &amp; accessible', 'next/image, lazy loading and accessible components throughout.'),
                  ('Deployed on Vercel', 'Live, shareable and updated straight from GitHub.')],
        highlights=[('3', 'layouts: phone, tablet, desktop'), ('4-step', 'guided tutorial'), ('2026', 'built &amp; deployed on Vercel')],
    ),
    dict(
        slug='fomi-flow', name='Fomi Flow', full='Fomi Flow: Version-based Workspace',
        short='Version-based AI image workspace',
        tagline='My redesign of an AI image workspace where every image is a version you can compare, branch and restore.',
        card='My own redesign of an AI image workspace: every image is a version you can compare, branch and restore, with an automatic "what changed" summary.',
        client='Hiring Assessment', assessment=True, role='Product &amp; UI', year='2026', type='Product Redesign',
        category='webapp',
        live='https://fomi-studio-weld.vercel.app/flow', source='https://github.com/Afsheen96/fomi-studio', source_label='Source code',
        tech=['Next.js', 'React', 'UX Design', 'JavaScript', 'CSS Modules', 'Vercel'],
        desktop='fomi-flow-desktop.webp', mobile='fomi-flow-mobile.webp', og='fomi-flow.jpg',
        gallery=[('fomi-flow-desktop.webp', 'Project sidebar, version history and "What changed" panel'),
                 ('../fomi-flow.jpg', 'Compare slider showing v2 against v4')],
        overview=['My own concept, created during the same frontend hiring assessment. Most AI image tools show results as an endless feed, so good results get lost. In Fomi Flow every generation is a version inside a project.',
                  'A version strip shows the history (with branches like "from v2"), a compare slider puts two versions side by side, and a "What changed" panel lists the prompt words added or removed and any settings change.'],
        problem=['While working on the same hiring assessment, I noticed a UX problem in most AI image tools: results appear in an endless feed.', 'Creators who refine one image many times lose track of which prompt made which result, and going back to an older idea means starting over.'],
        built=['I designed and built Fomi Flow as my own concept, where every generation is a numbered version inside a project. A version strip shows the history and branches (like "v4 from v2"), a compare slider puts two versions side by side, and a "What changed" panel lists the prompt words added or removed and any settings change.', 'The prompt bar starts filled with the selected version, and notes, copy-prompt and keyboard shortcuts make iterating faster. It is built with Next.js and works on phone, tablet and desktop.'],
        result=['Creators can see how an image evolved, compare any two versions and continue from any point instead of starting over.', 'The project shows my UX thinking: spotting a real problem, then designing and building a clear solution.'],
        features=[('Versions, not a feed', 'Every generation is saved as a numbered version inside a project.'),
                  ('Branching history', 'A version strip shows where each image came from, e.g. "v4 from v2".'),
                  ('Compare slider', 'Drag a slider to see two versions side by side.'),
                  ('"What changed" panel', 'Lists prompt words added or removed and any settings change, like ratio 1:1 to 4:3.'),
                  ('Edit from any version', 'The prompt bar starts with the selected version, so you only change a few words.'),
                  ('Keyboard shortcuts', 'Arrow keys move between versions and C opens compare.'),
                  ('Notes &amp; copy prompt', 'Save a note on why you kept a version and copy its prompt in one click.'),
                  ('Projects sidebar', 'Separate projects like campaigns or poster sets, each with its own versions.'),
                  ('Works everywhere', 'Designed for phone, tablet and desktop.')],
        highlights=[('1 click', 'to compare any two versions'), ('Auto', '"what changed" summaries'), ('2026', 'concept, design &amp; build')],
    ),
]

CATEGORY_LABEL = {'website': 'Website', 'webapp': 'Web App'}


def shot(p, key):
    return f"resources/shots/{p[key]}"


# ---------------------------------------------------------------- layout
NAV = [('home', 'Home', ''), ('about', 'About', 'about/'), ('skills', 'Skills', 'skills/'),
       ('projects', 'Projects', 'projects/'), ('contact', 'Contact', 'contact/')]


def head(root, path, title, desc, image='resources/shots/hightechzone-desktop.webp', og_type='website', css=(), ld=None):
    url = BASE + path
    extra = ''.join(f'\n  <link rel="stylesheet" href="{root}{c}">' for c in css)
    ld_tag = f'\n  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    return f'''<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{E(desc, quote=True)}">
  <meta name="author" content="Afsheen Kiran">
  <meta name="theme-color" content="#6070ff">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Afsheen Kiran Portfolio">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{E(desc, quote=True)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}{image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap">
  <link rel="stylesheet" href="{root}style.css">{extra}{ld_tag}
</head>
'''


def header(root, active):
    def link(cls, key, label, href):
        cur = ' aria-current="page"' if key == active else ''
        act = ' active' if key == active else ''
        return f'<li><a class="{cls}{act}" href="{root}{href}"{cur}>{label}</a></li>'
    desk = '\n          '.join(link('nav-link', *n) for n in NAV)
    mob = '\n          '.join(link('mobile-nav', *n).replace('<li>', '<li class="mobile-link">', 1) for n in NAV)
    hire_act = ' active' if active == 'hire' else ''
    hire_cur = ' aria-current="page"' if active == 'hire' else ''
    return f'''<body data-page="{active}">
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="scroll-progress" aria-hidden="true"></div>
  <div class="page-veil" aria-hidden="true"></div>

  <div class="header-nav" id="header-nav">
    <header class="header">
      <p class="logo"><a href="{root}" aria-label="Afsheen, home">Afsheen</a></p>
      <nav aria-label="Main">
        <ul class="mobile-menu" id="mobile-menu">
          <li class="mobile-close"><button type="button" class="close-icon" id="menu-close" aria-label="Close menu"><span></span><span></span></button></li>
          {mob}
          <li class="mobile-link"><a class="mobile-nav mobile-hire{hire_act}" href="{root}hire-me/"{hire_cur}>Hire me</a></li>
        </ul>
        <button type="button" class="menu" id="menu-open" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false">
          <img src="{root}resources/menuicon.png" alt="" width="18" height="12">
        </button>
        <ul class="menu-link">
          {desk}
          <li><a class="nav-cta magnetic{hire_act}" href="{root}hire-me/"{hire_cur}>Hire me</a></li>
        </ul>
      </nav>
    </header>
  </div>
'''


def footer(root, scripts=()):
    links = ''.join(f'<li><a href="{root}{h}">{l}</a></li>' for _, l, h in NAV) + f'<li><a href="{root}hire-me/">Hire me</a></li>'
    js = ''.join(f'\n  <script src="{root}{s}"></script>' for s in scripts)
    return f'''
  <footer class="site-footer">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="logo footer-logo" href="{root}">Afsheen</a>
        <p>Front-end web developer &amp; web designer building visually appealing, responsive and user-friendly websites.</p>
      </div>
      <nav aria-label="Footer">
        <ul class="footer-links">{links}</ul>
      </nav>
      {social(root, 'small')}
    </div>
    <div class="footer-bottom">
      <p>&copy; <span id="year">{YEAR}</span> Afsheen Kiran. Designed &amp; built with care.</p>
      <a href="#main" class="back-top">Back to top <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6" /></svg></a>
    </div>
  </footer>

  <script src="{root}config.js"></script>
  <script src="{root}site.js"></script>{js}
</body>

</html>
'''


def social(root, size=''):
    items = []
    for key in ('email', 'linkedin', 'github'):
        label, svg = BRAND[key]
        items.append(f'<li><a class="social-btn" data-social="{key}" aria-label="{label}" data-label="{label}">{svg}</a></li>')
    cls = 'social-pro' + (f' social-{size}' if size else '')
    return f'<ul class="{cls}">' + ''.join(items) + '</ul>'


def frame(src, alt, url_text='', lazy=True, cls='', w=1440, h=900):
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    bar = f'<em>{E(url_text)}</em>' if url_text else ''
    return f'''<div class="browser-frame {cls}">
            <div class="browser-bar"><span></span><span></span><span></span>{bar}</div>
            <div class="frame-shot"><img src="{src}" alt="{E(alt, quote=True)}" width="{w}" height="{h}"{lz}></div>
          </div>'''


def phone(src, alt, cls=''):
    return f'''<div class="phone-frame {cls}"><span class="phone-notch"></span><img src="{src}" alt="{E(alt, quote=True)}" width="585" height="1266" loading="lazy" decoding="async"></div>'''


def project_card(p, i, root, big=False):
    num = f'{i + 1:02d}'
    host = p['live'].replace('https://', '').rstrip('/')
    cls = 'project-card reveal' + (' is-featured' if big else '')
    badge = f'<span class="feature-badge">{ICON["star"]} Featured project</span>' if p.get('featured') else ''
    if p.get('assessment'):
        badge += f'<span class="assess-badge">{ICON["briefcase"]} Hiring Assessment</span>'
    client = '' if p.get('assessment') else f'<li><strong>{p["client"]}</strong></li>\n            <li><div class="dot"></div></li>\n            '
    tags = ''.join(f'<li>{E(t)}</li>' for t in p['tech'][:4])
    return f'''
      <article class="{cls}" data-category="{p['category']}">
        <a class="pc-media" href="{root}projects/{p['slug']}/" aria-label="Open the {p['full']} case study" tabindex="-1">
          <span class="pc-glow" aria-hidden="true"></span>
          {frame(root + shot(p, 'desktop'), 'Screenshot of the ' + html.unescape(p['full']) + ' website on desktop', host, cls='pc-desktop')}
          {phone(root + shot(p, 'mobile'), 'Screenshot of ' + html.unescape(p['full']) + ' on a phone', 'pc-phone')}
          <span class="pc-hint" aria-hidden="true">View case study {ICON['arrow']}</span>
        </a>
        <div class="pc-body">
          <div class="pc-top">
            <span class="pc-num">{num}</span>
            <span class="pc-type">{p['type']}</span>
            {badge}
          </div>
          <h3 class="pc-title"><a href="{root}projects/{p['slug']}/">{p['full']}</a></h3>
          <ul class="proj">
            {client}<li>{p['role']}</li>
            <li><div class="dot"></div></li>
            <li>{p['year']}</li>
          </ul>
          <p class="pro">{E(p['card'])}</p>
          <ul class="language">{tags}</ul>
          <div class="work-actions">
            <a class="btn btn-primary btn-shine magnetic" href="{root}projects/{p['slug']}/">View Project {ICON['arrow']}</a>
            <a class="btn btn-ghost magnetic" href="{p['live']}" target="_blank" rel="noopener">Live Preview {ICON['ext']}</a>
            <button type="button" class="icon-link quick-view" data-project="{p['slug']}" aria-label="Quick view of {p['full']}" title="Quick view">{ICON['eye']}</button>
          </div>
        </div>
      </article>'''


def projects_json(root):
    data = [dict(slug=p['slug'], name=html.unescape(p['full']), client=html.unescape(p['client']),
                 role=html.unescape(p['role']), year=p['year'], text=html.unescape(' '.join(p['overview'])),
                 tech=p['tech'], image=root + shot(p, 'desktop'), live=p['live'], source=p['source'],
                 sourceLabel=p['source_label'], page=f"{root}projects/{p['slug']}/") for p in PROJECTS]
    return '<script type="application/json" id="projects-data">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def cta_band(root, title='Have a project in mind?', text="Let's turn your idea into a fast, beautiful website that your clients will love."):
    return f'''
    <section class="cta-band">
      <div class="cta-inner reveal">
        <span class="cta-orb" aria-hidden="true"></span>
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="hero-actions center">
          <a class="btn cta-light btn-shine magnetic" href="{root}hire-me/">Hire me for a project {ICON['arrow']}</a>
          <a class="btn cta-outline magnetic" href="{root}contact/">Just say hello</a>
        </div>
      </div>
    </section>'''


def page_hero(eyebrow, title, sub, extra=''):
    return f'''
    <section class="page-hero">
      <div class="page-hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
      <div class="wrap">
        <p class="eyebrow reveal">{eyebrow}</p>
        <h1 class="page-title reveal">{title}</h1>
        <p class="page-sub reveal">{sub}</p>{extra}
      </div>
    </section>'''


def write(rel, content):
    path = os.path.join(ROOT_DIR, rel)
    os.makedirs(os.path.dirname(path) or ROOT_DIR, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote', rel)


# ---------------------------------------------------------------- pages
def home():
    root = ''
    cards = ''.join(project_card(p, i, root, big=(i == 0)) for i, p in enumerate(PROJECTS))
    ld = {"@context": "https://schema.org", "@type": "Person", "name": "Afsheen Kiran",
          "jobTitle": "Front-End Web Developer & Web Designer", "url": BASE,
          "sameAs": ["https://www.linkedin.com/in/afsheenkiran/", "https://github.com/Afsheen96"]}
    return head(root, '', 'Afsheen Kiran | Front-End Web Developer &amp; Web Designer',
                'Afsheen Kiran is a front-end web developer and web designer who turns ideas into visually appealing, responsive and user-friendly websites. See HighTechZone, Learning AI Lecture Hub, Fomi Studio and Fomi Flow.',
                ld=ld) + header(root, 'home') + f'''
  <main id="main">
    <section class="main-container hero" id="top">
      <canvas class="hero-canvas" aria-hidden="true"></canvas>
      <div class="hero-aurora" aria-hidden="true"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>
      <div class="hero-spotlight" aria-hidden="true"></div>
      <div class="hero-shapes" aria-hidden="true">
        <span class="shape shape-dot" data-depth="30"></span>
        <span class="shape shape-bar" data-depth="18"></span>
        <span class="shape shape-ring2" data-depth="40"></span>
        <span class="shape shape-plus" data-depth="24"></span>
      </div>
      <section class="headline">
        <p class="availability hero-in d-0"><span class="pulse"></span>Available for freelance projects</p>
        <h1 class="heading hero-heading">
          <span class="line"><span>I'm Afsheen.</span></span>
          <span class="line"><span>Glad to see <span class="gradient-text">you!</span></span></span>
        </h1>
        <p class="hero-roles hero-in d-3" aria-live="polite">
          I design &amp; build <span class="typed" id="typed">modern websites</span><span class="caret" aria-hidden="true"></span>
        </p>
        <p class="headline-paragraph hero-in d-4">
          I'm a Front-End Web Developer and Web Designer who turns ideas into
          visually appealing, responsive, and user-friendly websites. I combine
          creative design with modern web technologies to build engaging digital
          experiences that help businesses and individuals establish a strong
          online presence.
        </p>
        <div class="hero-actions hero-in d-5">
          <a class="btn btn-primary btn-shine magnetic" href="projects/">View my work {ICON['arrow']}</a>
          <a class="btn btn-ghost magnetic" href="hire-me/">Hire me</a>
        </div>
        <div class="hero-connect hero-in d-6">
          <h2 class="mini-headline">LET'S CONNECT</h2>
          {social(root)}
        </div>
      </section>
      <a class="scroll-cue" href="#services" aria-label="Scroll down"><span></span></a>
    </section>

    <section class="services" id="services" aria-label="What I can do for you">
      <article class="service reveal">
        <span class="service-icon">{ICON['layout']}</span>
        <h2>Website Design</h2>
        <p>Clean, modern layouts that look great and make your brand easy to trust.</p>
      </article>
      <article class="service reveal">
        <span class="service-icon">{ICON['code']}</span>
        <h2>Frontend Development</h2>
        <p>Fast, accessible websites and web apps with HTML, CSS, JavaScript, React and Next.js.</p>
      </article>
      <article class="service reveal">
        <span class="service-icon">{ICON['phone']}</span>
        <h2>Responsive Design</h2>
        <p>Every page looks great and works smoothly on phones, tablets and desktops.</p>
      </article>
    </section>

    <section class="work-section" aria-labelledby="work-title">
      <div class="section-head reveal">
        <p class="eyebrow">Featured work</p>
        <h2 class="section-title" id="work-title">My Recent Works</h2>
        <p class="section-sub">Real projects I designed and built. Every screenshot is taken from the live project.</p>
      </div>
      <div class="project-list">{cards}
      </div>
      <div class="center-link reveal"><a class="btn btn-ghost magnetic" href="projects/">See all projects {ICON['arrow']}</a></div>
    </section>

    <section class="about-teaser">
      <div class="wrap teaser-grid">
        <div class="reveal">
          <p class="eyebrow">About</p>
          <h2 class="section-title left">Hello, I'm Afsheen</h2>
          <p class="headline-paragraph">With an MSc in Information Technology, I design and build websites with HTML, CSS, JavaScript, React and Next.js, focusing on clean design and a smooth experience on every device.</p>
          <div class="hero-actions">
            <a class="btn btn-primary magnetic" href="about/">More about me {ICON['arrow']}</a>
            <a class="btn btn-ghost magnetic" href="skills/">My skills</a>
          </div>
        </div>
        <ul class="teaser-stats reveal" aria-label="What you can expect">
          <li><span class="ts-icon">{ICON['rocket']}</span><strong>7&ndash;14 Days</strong><span>Typical project delivery</span></li>
          <li><span class="ts-icon">{ICON['chat']}</span><strong>Within 24 Hours</strong><span>Client response time</span></li>
          <li><span class="ts-icon">{ICON['refresh']}</span><strong>2 Rounds</strong><span>Included revisions</span></li>
          <li><span class="ts-icon">{ICON['phone']}</span><strong>100%</strong><span>Responsive focus: desktop, tablet &amp; mobile design</span></li>
        </ul>
      </div>
    </section>
{cta_band(root)}
  </main>
  {projects_json(root)}
  <div id="popupWindow" class="project_window"></div>
''' + footer(root, ('hero.js', 'index.js'))


def about():
    root = '../'
    steps = [('Discover', 'We talk about your goals, your audience and what success looks like.', ICON['chat']),
             ('Design', 'I plan the layout and look, keeping your brand colours and identity.', ICON['layout']),
             ('Build', 'I code a fast, responsive website and share progress as I go.', ICON['code']),
             ('Launch', 'I publish it (GitHub Pages or Vercel) and show you how to update it.', ICON['rocket'])]
    step_html = ''.join(f'''
          <li class="step reveal"><span class="step-icon">{ic}</span><span class="step-num">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (t, d, ic) in enumerate(steps))
    return head(root, 'about/', 'About Afsheen Kiran | Frontend Developer &amp; Web Designer',
                'Learn about Afsheen Kiran, a front-end web developer and web designer who builds visually appealing, responsive websites, and how she works with clients.') + header(root, 'about') + f'''
  <main id="main">
{page_hero('About', 'About <span class="gradient-text">Myself</span>', 'The person behind the projects, and how I like to work.')}
    <section class="about about-page">
      <div class="about-container">
        <div class="sub-container reveal">
          <h2 class="heading">Hello, I'm Afsheen</h2>
          <p class="headline-paragraph">I'm Afsheen Kiran, a web developer with an MSc in Information Technology. My studies gave me a solid understanding of how software and the web work, and I now use that foundation to design and build websites of my own.</p>
          <p class="headline-paragraph">I'm especially interested in modern web technologies and in how technology can make everyday tasks easier. I enjoy turning ideas into real projects: my Learning AI Lecture Hub, for example, brings scattered lecture links together into one organised, searchable library.</p>
          <p class="headline-paragraph">I focus on responsive design, clear user experience and clean, modern interfaces, so every page is easy to use on phones, tablets and desktops. I love learning new things, building creative projects and using technology to solve real-world problems.</p>
          <h2 class="mini-headline">LET'S CONNECT</h2>
          {social(root)}
          <div class="hero-actions">
            <a class="btn btn-primary btn-shine magnetic" href="../hire-me/">Hire me {ICON['arrow']}</a>
            <a class="btn btn-ghost magnetic" href="../skills/">See my skills</a>
          </div>
        </div>
        <div class="about-cards reveal">
          <article class="value-card"><span class="service-icon">{ICON['globe']}</span><h3>Built for real visitors</h3><p>Every site I make is responsive, accessible and quick to load on any device.</p></article>
          <article class="value-card"><span class="service-icon">{ICON['spark']}</span><h3>Design meets code</h3><p>I combine creative design with clean, modern code for interfaces people enjoy using.</p></article>
          <article class="value-card"><span class="service-icon">{ICON['book']}</span><h3>Easy to own</h3><p>I explain things plainly and leave simple guides so you can update your site yourself.</p></article>
          <article class="value-card"><span class="service-icon">{ICON['search']}</span><h3>Ready to be found</h3><p>SEO basics like meta tags, sitemaps and structured data come built in.</p></article>
        </div>
      </div>
    </section>

    <section class="process">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">How I work</p>
          <h2 class="section-title">From idea to live website</h2>
        </div>
        <ol class="steps">{step_html}
        </ol>
      </div>
    </section>
{cta_band(root, 'Want to work together?', 'Tell me about your project and I will reply with ideas and next steps.')}
  </main>
''' + footer(root)


def skills():
    root = '../'
    def chips(items):
        return ''.join(f'<li>{t}</li>' for t in items)
    used = {
        'HighTechZone': 'projects/hightechzone/', 'Learning AI Lecture Hub': 'projects/learning-ai-lecture-hub/',
        'Fomi Studio': 'projects/fomi-studio/', 'Fomi Flow': 'projects/fomi-flow/'}
    def used_in(names):
        return '<p class="used-in">Used in: ' + ', '.join(f'<a href="{root}{used[n]}">{n}</a>' for n in names) + '</p>'
    groups = [
        ('Frameworks &amp; libraries', ICON['layout'], ['React', 'Next.js', 'CSS Modules'], ['Fomi Studio', 'Fomi Flow']),
        ('Design &amp; UX', ICON['spark'], ['Responsive design', 'UI / UX design', 'Product redesign', 'Accessibility', 'Animations &amp; micro-interactions'], ['HighTechZone', 'Fomi Flow']),
        ('SEO &amp; performance', ICON['search'], ['Meta &amp; Open Graph tags', 'Structured data', 'Sitemaps &amp; robots.txt', 'Lazy loading', 'Image optimisation'], ['HighTechZone', 'Learning AI Lecture Hub']),
        ('Tools &amp; deployment', ICON['rocket'], ['Git &amp; GitHub', 'GitHub Pages', 'GitHub Actions', 'Vercel', 'Node.js scripts', 'JSON data'], ['Learning AI Lecture Hub', 'Fomi Studio']),
    ]
    g_html = ''.join(f'''
        <article class="skill-group reveal">
          <div class="sg-head"><span class="service-icon">{ic}</span><h2>{t}</h2></div>
          <ul class="tag-list">{chips(items)}</ul>
          {used_in(u)}
        </article>''' for t, ic, items, u in groups)
    return head(root, 'skills/', 'Skills &amp; Expertise | Afsheen Kiran',
                'Skills and expertise of Afsheen Kiran: JavaScript, HTML, CSS, React, Next.js, responsive design, SEO, GitHub Pages, and Vercel.') + header(root, 'skills') + f'''
  <main id="main">
{page_hero('Skills', 'Skills &amp; <span class="gradient-text">Expertise</span>', 'The languages, frameworks and tools I use to design and build websites, with links to the real projects where I used them.')}
    <section class="skills-page">
      <div class="wrap">
        <article class="skill-group lang-group reveal">
          <div class="sg-head"><span class="service-icon">{ICON['code']}</span><h2>Languages</h2></div>
          <ul class="skill-container">
            <li class="skills"><img src="{root}resources/jslogo.png" alt="JavaScript logo" width="50" height="50"><span class="skill-name">JavaScript</span></li>
            <li class="skills"><img src="{root}resources/htmllogo.png" alt="HTML logo" width="50" height="51"><span class="skill-name">HTML</span></li>
            <li class="skills"><img src="{root}resources/csslogo.png" alt="CSS logo" width="50" height="51"><span class="skill-name">CSS</span></li>
          </ul>
          {used_in(['HighTechZone', 'Learning AI Lecture Hub', 'Fomi Studio'])}
        </article>
        <div class="skill-grid">{g_html}
        </div>
      </div>
    </section>
{cta_band(root, 'Need these skills on your project?', 'I can design and build your website from start to finish.')}
  </main>
''' + footer(root)


def projects_index():
    root = '../'
    cards = ''.join(project_card(p, i, root, big=(i == 0)) for i, p in enumerate(PROJECTS))
    return head(root, 'projects/', 'Projects | Afsheen Kiran Portfolio',
                'Website and web app projects by Afsheen Kiran: HighTechZone, Learning AI Lecture Hub, Fomi Studio and Fomi Flow, each with a full case study and live link.') + header(root, 'projects') + f'''
  <main id="main">
{page_hero('Portfolio', 'My <span class="gradient-text">Projects</span>', 'Websites and web apps I designed and built. Open any project for the full case study, real screenshots and a live preview.')}
    <section class="work-section projects-page">
      <div class="filter-bar reveal" role="group" aria-label="Filter projects">
        <button type="button" class="filter-btn active" data-filter="all" aria-pressed="true">All <span>{len(PROJECTS)}</span></button>
        <button type="button" class="filter-btn" data-filter="website" aria-pressed="false">Websites <span>{sum(p['category'] == 'website' for p in PROJECTS)}</span></button>
        <button type="button" class="filter-btn" data-filter="webapp" aria-pressed="false">Web Apps <span>{sum(p['category'] == 'webapp' for p in PROJECTS)}</span></button>
      </div>
      <div class="project-list">{cards}
      </div>
    </section>
{cta_band(root)}
  </main>
  {projects_json(root)}
  <div id="popupWindow" class="project_window"></div>
''' + footer(root, ('index.js',))


def contact():
    root = '../'
    return head(root, 'contact/', 'Contact | Afsheen Kiran',
                'Get in touch with Afsheen Kiran for questions, networking or collaborations.') + header(root, 'contact') + f'''
  <main id="main">
{page_hero('Contact', 'Let\'s <span class="gradient-text">Connect</span>', 'Questions, networking, collaborations or just a friendly hello. I read every message.')}
    <section class="contact-page">
      <div class="wrap contact-grid">
        <div class="contact-side reveal">
          <h2 class="side-title">Ways to reach me</h2>
          <ul class="contact-cards">
            <li><a class="contact-card" data-social="email" data-show-value="true">
              <span class="cc-icon">{BRAND['email'][1]}</span>
              <span class="cc-text"><strong>Email</strong><span class="cc-value" data-social-value>Coming soon</span></span>
              <span class="cc-arrow">{ICON['arrow']}</span></a></li>
            <li><a class="contact-card" data-social="linkedin">
              <span class="cc-icon">{BRAND['linkedin'][1]}</span>
              <span class="cc-text"><strong>LinkedIn</strong><span class="cc-value" data-social-value>Connect professionally</span></span>
              <span class="cc-arrow">{ICON['arrow']}</span></a></li>
            <li><a class="contact-card" data-social="github">
              <span class="cc-icon">{BRAND['github'][1]}</span>
              <span class="cc-text"><strong>GitHub</strong><span class="cc-value" data-social-value>See my code</span></span>
              <span class="cc-arrow">{ICON['arrow']}</span></a></li>
          </ul>
          <div class="info-note">
            <span class="service-icon">{ICON['clock']}</span>
            <p><strong>Usually replies within 1&ndash;2 working days.</strong> Looking to start a website project? The <a href="../hire-me/">Hire Me page</a> has a project form made for that.</p>
          </div>
        </div>

        <div class="contact-form-card reveal">
          <h2 class="side-title">Send a message</h2>
          <form action="{FORM_ENDPOINT}" method="post" class="pro-form" id="contactform" data-ajax-form data-draft-key="contact-draft" novalidate>
            <input type="hidden" name="_subject" value="New message from your portfolio Contact page">
            <input type="hidden" name="form_type" value="General contact">
            <div class="field-row">
              <div class="field"><label for="c-name">Your name</label><input type="text" id="c-name" name="name" maxlength="60" autocomplete="name" required placeholder="Jane Smith"></div>
              <div class="field"><label for="c-email">Email</label><input type="email" id="c-email" name="email" autocomplete="email" required placeholder="jane@example.com"></div>
            </div>
            <div class="field"><label for="c-subject">Subject</label><input type="text" id="c-subject" name="subject" maxlength="100" required placeholder="What would you like to talk about?"></div>
            <div class="field"><label for="c-message">Message</label><textarea id="c-message" name="message" rows="6" maxlength="1000" required placeholder="Write your message here"></textarea></div>
            <input type="text" name="_gotcha" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
            <p class="form-status" role="status" aria-live="polite"></p>
            <button class="btn btn-primary btn-shine form-submit" type="submit">Send message {ICON['send']}</button>
          </form>
        </div>
      </div>
    </section>
  </main>
''' + footer(root, ('forms.js',))


def hire():
    root = '../'
    packages = [
        dict(icon=ICON['rocket'], name='Landing Page', price=79, radio='Landing page',
             desc='A focused one-page website for your product, service or event.',
             items=['Custom single-page website', 'Modern and attractive UI/UX design', 'Responsive mobile-friendly layout',
                    'Front-end development', 'Clear call-to-action sections', 'Basic on-page SEO'],
             time='5&ndash;7 days'),
        dict(icon=ICON['globe'], name='Business Website', price=199, radio='New website', featured=True,
             desc='A complete multi-page website for your business or personal brand.',
             items=['Up to 5 website pages', 'Professional website design', 'Responsive front-end development',
                    'Home, About, Services, Projects, and Contact pages', 'Contact form integration', 'Basic SEO setup',
                    'Smooth animations and interactions'],
             time='10&ndash;14 days'),
        dict(icon=ICON['refresh'], name='Website Redesign', price=129, radio='Website redesign',
             desc='A modern refresh for the website you already have.',
             items=['Redesign of up to 3 existing pages', 'Modern UI/UX improvements', 'Responsive layout improvements',
                    'Better visual consistency', 'Modern styling and interactions', 'Front-end performance improvements where applicable'],
             time='7&ndash;10 days'),
    ]
    faqs = [
        ('How many revisions are included?',
         'Every package includes 2 rounds of revisions. Additional revisions or major changes to the agreed scope are discussed separately.'),
        ('What is your payment process?',
         'I work with 50% of the payment upfront to start the project and the remaining 50% before final delivery.'),
        ('How long does a project take?',
         'It depends on the package: about 5&ndash;7 days for a Landing Page, 10&ndash;14 days for a Business Website and 7&ndash;10 days for a Website Redesign. The exact timeline depends on the project&rsquo;s complexity and on receiving your content (text, images, logo) on time.'),
        ('Can I request custom features?',
         'Yes. Tell me what you need and we will discuss it together. Custom features are quoted separately before any work starts.'),
        ('Do you provide website maintenance?',
         'Yes. Ongoing maintenance and updates can be arranged as a separate service. We can agree on what you need after your website is live.'),
    ]
    reasons = [
        ('Proven, live work', 'HighTechZone, Learning AI Lecture Hub and two Next.js apps are live right now. You can click and test them.', 'projects/'),
        ('Every device covered', 'Each project in my portfolio has layouts tested on phone, tablet and desktop.', None),
        ('Built to be found', 'My sites include SEO essentials such as structured data, sitemaps and clean HTML.', None),
        ('Free or low-cost hosting', 'I deploy on GitHub Pages or Vercel and can set up automatic publishing.', None),
        ('You stay in control', 'Plain explanations and simple guides so you can update content yourself.', None),
        ('Creative design, clean code', 'I pair creative, on-brand design with clean, modern code, so your site looks great and works well.', None),
    ]
    def price_card(k):
        feat = k.get('featured')
        items = ''.join(f'<li>{ICON["check"]}<span>{t}</span></li>' for t in k['items'])
        badge = f'<span class="price-badge">{ICON["star"]} Recommended</span>' if feat else ''
        btn = 'btn-primary btn-shine' if feat else 'btn-ghost'
        return f'''
          <article class="price-card reveal{' is-featured' if feat else ''}">
            {badge}
            <span class="service-icon">{k['icon']}</span>
            <h3>{k['name']}</h3>
            <p class="price-desc">{k['desc']}</p>
            <p class="price"><span class="price-from">Starting at</span><strong>${k['price']}</strong><span class="price-cur">USD</span></p>
            <ul class="price-list">{items}</ul>
            <p class="price-time">{ICON['clock']} Estimated delivery: <strong>{k['time']}</strong></p>
            <a class="btn {btn} magnetic price-cta" href="#inquiry" data-package="{k['radio']}">Get Started {ICON['arrow']}</a>
          </article>'''
    p_html = ''.join(price_card(k) for k in packages)
    f_html = ''.join(f'''
          <div class="accordion faq-item reveal">
            <h3><button type="button" class="accordion-toggle" aria-expanded="false" aria-controls="faq-{i}" id="faq-q-{i}"><span>{q}</span>{ICON['chev']}</button></h3>
            <div class="accordion-panel" id="faq-{i}" role="region" aria-labelledby="faq-q-{i}"><div><p>{a}</p></div></div>
          </div>''' for i, (q, a) in enumerate(faqs, 1))
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}
    r_html = ''.join(f'''<li class="reason reveal"><span class="reason-check">{ICON['check']}</span><div><h3>{t}</h3><p>{d}{f' <a href="{root}{l}">See projects</a>' if l else ''}</p></div></li>''' for t, d, l in reasons)
    def opts(items):
        return ''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in items)
    return head(root, 'hire-me/', 'Hire Me | Website Design &amp; Development by Afsheen Kiran',
                'Hire Afsheen Kiran to design and build your website. Landing pages from $79, business websites from $199 and website redesigns from $129. Send a project inquiry.',
                ld=ld) + header(root, 'hire') + f'''
  <main id="main">
    <section class="hire-hero">
      <div class="page-hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
      <div class="wrap hire-hero-grid">
        <div>
          <p class="availability reveal"><span class="pulse"></span>Taking new projects</p>
          <h1 class="page-title reveal">Let's Build Something <span class="gradient-text">Amazing</span> Together</h1>
          <p class="page-sub reveal">Need a website that looks premium, loads fast and works on every phone? I design and build websites and web apps for businesses, creators and personal brands, and I make the process simple and friendly.</p>
          <div class="hero-actions reveal">
            <a class="btn btn-primary btn-shine magnetic" href="#inquiry">Start your project {ICON['arrow']}</a>
            <a class="btn btn-ghost magnetic" href="../projects/">See my work</a>
          </div>
        </div>
        <div class="hire-visual reveal" aria-hidden="true">
          {frame(root + 'resources/shots/hightechzone-desktop.webp', '', 'afsheen96.github.io/HighTechZone', cls='hv-back')}
          {phone(root + 'resources/shots/lecture-hub-mobile.webp', '', 'hv-phone')}
        </div>
      </div>
    </section>

    <section class="hire-services pricing" id="pricing">
      <div class="wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Packages</p>
          <h2 class="section-title">Services &amp; Pricing</h2>
          <p class="section-sub">Simple packages for web design and front-end development. Pick the one that fits, or tell me about something custom.</p>
        </div>
        <div class="price-grid">{p_html}
        </div>
        <p class="price-note reveal">{ICON['spark']}<span>All prices are in USD and are <strong>starting prices</strong>. Final pricing depends on the project&rsquo;s scope and complexity. Domain, hosting, premium assets (such as paid fonts, themes or stock images) and additional functionality are charged separately where applicable.</span></p>

        <div class="faq" id="faq">
          <div class="section-head reveal">
            <p class="eyebrow">FAQ</p>
            <h2 class="section-title">Frequently asked questions</h2>
          </div>
          <div class="faq-list">{f_html}
          </div>
        </div>
      </div>
    </section>

    <section class="why">
      <div class="wrap why-grid">
        <div class="reveal">
          <p class="eyebrow">Why work with me</p>
          <h2 class="section-title left">Reasons clients choose me</h2>
          <p class="section-sub left">Based on what I have actually built and shipped, not on promises.</p>
        </div>
        <ul class="reasons">{r_html}</ul>
      </div>
    </section>

    <section class="form-container inquiry" id="inquiry">
      <div class="inquiry-card reveal">
        <h2 class="form-heading">Tell me about your project</h2>
        <p class="form-paragraph">Share a few details and I'll reply with questions, ideas and next steps. Budget and timeline are optional.</p>
        <form action="{FORM_ENDPOINT}" method="post" class="pro-form inquiry-form" id="hireform" data-ajax-form data-draft-key="hire-draft" novalidate>
          <input type="hidden" name="_subject" value="New PROJECT INQUIRY from your portfolio Hire Me page">
          <input type="hidden" name="form_type" value="Project inquiry (Hire Me)">
          <input type="hidden" name="package" value="No package selected">
          <div class="field-row">
            <div class="field"><label for="h-name">Your name</label><input type="text" id="h-name" name="name" maxlength="60" autocomplete="name" required placeholder="Jane Smith"></div>
            <div class="field"><label for="h-email">Email address</label><input type="email" id="h-email" name="email" autocomplete="email" required placeholder="jane@company.com"></div>
          </div>
          <fieldset class="field type-field">
            <legend>Project type</legend>
            <div class="type-options">
              <label class="type-option"><input type="radio" name="project_type" value="New website" required><span>{ICON['globe']} New website</span></label>
              <label class="type-option"><input type="radio" name="project_type" value="Website redesign"><span>{ICON['refresh']} Redesign</span></label>
              <label class="type-option"><input type="radio" name="project_type" value="Landing page"><span>{ICON['rocket']} Landing page</span></label>
              <label class="type-option"><input type="radio" name="project_type" value="Portfolio or personal site"><span>{ICON['star']} Portfolio</span></label>
              <label class="type-option"><input type="radio" name="project_type" value="Web app (React / Next.js)"><span>{ICON['code']} Web app</span></label>
              <label class="type-option"><input type="radio" name="project_type" value="Something else"><span>{ICON['chat']} Other</span></label>
            </div>
          </fieldset>
          <div class="field"><label for="h-desc">Project description</label><textarea id="h-desc" name="project_description" rows="5" maxlength="2000" required placeholder="What is the project, who is it for, and what should the website do?"></textarea></div>
          <div class="field-row">
            <div class="field"><label for="h-budget">Estimated budget <span class="optional">(optional)</span></label>
              <select id="h-budget" name="budget"><option value="">Select a range</option>{opts(['Under $250', '$250 - $500', '$500 - $1,000', '$1,000 - $2,500', '$2,500+', 'Not sure yet'])}</select></div>
            <div class="field"><label for="h-time">Expected timeline <span class="optional">(optional)</span></label>
              <select id="h-time" name="timeline"><option value="">Select a timeline</option>{opts(['As soon as possible', 'Within 2 weeks', 'Within 1 month', '1 - 3 months', 'Flexible'])}</select></div>
          </div>
          <input type="text" name="_gotcha" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="form-status" role="status" aria-live="polite"></p>
          <button class="form-button form-submit btn-shine" type="submit">Send project inquiry {ICON['send']}</button>
          <p class="form-note">Prefer a quick general question? Use the <a href="../contact/">Contact page</a>.</p>
        </form>
      </div>
    </section>
  </main>
''' + footer(root, ('forms.js',))


def case_page(p, idx):
    root = '../../'
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    prv = PROJECTS[(idx - 1) % len(PROJECTS)]
    host = p['live'].replace('https://', '').rstrip('/')
    feats = ''.join(f'''
          <li class="feature reveal"><span class="feature-icon">{ICON['check']}</span><h3>{t}</h3><p>{d}</p></li>''' for t, d in p['features'])
    tech = ''.join(f'<li>{E(t)}</li>' for t in p['tech'])
    hl = ''.join(f'<div class="stat"><strong>{a}</strong><span>{b}</span></div>' for a, b in p['highlights'])

    def paras(key):
        return ''.join(f'<p>{E(t)}</p>' for t in p[key])
    # The first gallery shot illustrates "What I Built"; the rest stay in the gallery.
    built_shot, built_cap = p['gallery'][1] if len(p['gallery']) > 1 else p['gallery'][0]
    gallery = [g for g in p['gallery'] if g[0] != built_shot]
    built_src = 'shots/' + built_shot if not built_shot.startswith('../') else built_shot[3:]
    built_big = built_shot.startswith('../')
    built_img = frame(root + 'resources/' + built_src, built_cap, host, w=(1088 if built_big else 1440), h=(896 if built_big else 900))
    gal = ''.join(f'''
          <figure class="gallery-item reveal">
            <button type="button" class="zoomable" data-lightbox="{root}resources/{'shots/' + g if not g.startswith('../') else g[3:]}" data-caption="{E(c, quote=True)}" aria-label="Enlarge: {E(c, quote=True)}">
              {frame(root + 'resources/' + ('shots/' + g if not g.startswith('../') else g[3:]), c, w=(1088 if g.startswith('../') else 1440), h=(896 if g.startswith('../') else 900))}
            </button>
            <figcaption>{E(c)}</figcaption>
          </figure>''' for g, c in gallery)
    full = ''
    if p.get('full_page'):
        full = f'''
        <figure class="fullpage reveal">
          <div class="browser-frame">
            <div class="browser-bar"><span></span><span></span><span></span><em>{E(host)}</em></div>
            <div class="fullpage-scroll" tabindex="0" aria-label="Scrollable full-page screenshot">
              <img src="{root}{shot(p, 'full_page')}" alt="Full-page screenshot of {p['full']}" width="960" height="2487" loading="lazy" decoding="async">
            </div>
          </div>
          <figcaption>Scroll inside the frame to see the whole page.</figcaption>
        </figure>'''
    og_img = f"resources/{p['og']}" if p.get('og') else shot(p, 'desktop')
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": html.unescape(p['full']),
          "description": p['tagline'], "url": f"{BASE}projects/{p['slug']}/", "image": BASE + shot(p, 'desktop'),
          "dateCreated": p['year'], "creator": {"@type": "Person", "name": "Afsheen Kiran", "url": BASE}}
    source_btn = f'<a class="btn btn-ghost magnetic" href="{p["source"]}" target="_blank" rel="noopener">{ICON["code"]} {p["source_label"]}</a>'
    return head(root, f"projects/{p['slug']}/", f"{p['full']} | Case Study by Afsheen Kiran", p['tagline'],
                image=og_img, og_type='article', css=('projects/project.css',), ld=ld) + header(root, 'projects') + f'''
  <main id="main">
    <section class="case-hero">
      <div class="page-hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
      <div class="case-wrap">
        <nav class="breadcrumb reveal" aria-label="Breadcrumb">
          <a href="{root}">Home</a><span>/</span><a href="{root}projects/">Projects</a><span>/</span><span aria-current="page">{p['name']}</span>
        </nav>
        <p class="eyebrow reveal">Project {idx + 1:02d} &middot; {p['type']}{f' <span class="assess-badge">{ICON["briefcase"]} Hiring Assessment</span>' if p.get('assessment') else ''}</p>
        <h1 class="case-title reveal">{p['full']}</h1>
        <p class="case-tagline reveal">{E(p['tagline'])}</p>
        <ul class="case-meta reveal">
          <li><span>{'Context' if p.get('assessment') else 'Client'}</span><strong>{p['client']}</strong></li>
          <li><span>Role</span><strong>{p['role']}</strong></li>
          <li><span>Year</span><strong>{p['year']}</strong></li>
          <li><span>Type</span><strong>{p['type']}</strong></li>
        </ul>
        <div class="case-actions reveal">
          <a class="btn btn-primary btn-shine magnetic" href="{p['live']}" target="_blank" rel="noopener">Visit live website {ICON['ext']}</a>
          {source_btn}
        </div>
      </div>
      <div class="case-wrap">
        <div class="hero-devices reveal">
          {frame(root + shot(p, 'desktop'), 'Screenshot of ' + html.unescape(p['full']) + ' on desktop', host, lazy=False, cls='hd-desktop')}
          {phone(root + shot(p, 'mobile'), 'Screenshot of ' + html.unescape(p['full']) + ' on a phone', 'hd-phone')}
        </div>
      </div>
    </section>

    <section class="case-section case-study" aria-labelledby="cs-title">
      <div class="case-wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Case study</p>
          <h2 class="section-title" id="cs-title">From problem to result</h2>
          <ol class="cs-path" aria-hidden="true"><li>Problem</li><li>What I Built</li><li>Result</li></ol>
        </div>
        <div class="cs-flow">
          <article class="cs-step reveal">
            <header class="cs-head"><span class="cs-letter">A</span><h3>Problem</h3></header>
            <div class="cs-body">{paras('problem')}</div>
          </article>
          <article class="cs-step reveal">
            <header class="cs-head"><span class="cs-letter">B</span><h3>What I Built</h3></header>
            <div class="cs-body">
              {paras('built')}
              <p class="cs-label">Tech stack</p>
              <ul class="language tech-list">{tech}</ul>
              <figure class="cs-shot">
                <button type="button" class="zoomable" data-lightbox="{root}resources/{built_src}" data-caption="{E(built_cap, quote=True)}" aria-label="Enlarge: {E(built_cap, quote=True)}">{built_img}</button>
                <figcaption>{E(built_cap)}</figcaption>
              </figure>
            </div>
          </article>
          <article class="cs-step reveal">
            <header class="cs-head"><span class="cs-letter">C</span><h3>Result</h3></header>
            <div class="cs-body">
              {paras('result')}
              <div class="stats cs-stats">{hl}</div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="case-section alt">
      <div class="case-wrap">
        <div class="section-head reveal"><p class="eyebrow">Screens</p><h2 class="section-title">More previews</h2>
          <p class="section-sub">Real screenshots from the live project. Click any screen to enlarge it.</p></div>
        <div class="gallery">{gal}
        </div>{full}
      </div>
    </section>

    <section class="case-section">
      <div class="case-wrap">
        <div class="section-head reveal"><p class="eyebrow">Features</p><h2 class="section-title">What it does</h2></div>
        <ul class="features">{feats}
        </ul>
      </div>
    </section>

    <section class="case-section alt" id="preview">
      <div class="case-wrap">
        <div class="section-head reveal">
          <p class="eyebrow">Live preview</p>
          <h2 class="section-title">Try the website right here</h2>
          <p class="section-sub">Load the real, live website below and switch between desktop, tablet and phone sizes.</p>
        </div>
        <div class="preview reveal" data-src="{p['live']}">
          <div class="preview-toolbar">
            <div class="device-switch" role="group" aria-label="Preview size">
              <button type="button" class="device-btn active" data-width="100%" aria-pressed="true">{ICON['desktop']}<span>Desktop</span></button>
              <button type="button" class="device-btn" data-width="768px" aria-pressed="false">{ICON['tablet']}<span>Tablet</span></button>
              <button type="button" class="device-btn" data-width="390px" aria-pressed="false">{ICON['phone']}<span>Phone</span></button>
            </div>
            <a class="preview-open" href="{p['live']}" target="_blank" rel="noopener">Open in new tab {ICON['ext']}</a>
          </div>
          <div class="preview-stage">
            <div class="preview-device">
              <div class="browser-bar"><span></span><span></span><span></span><em>{E(host)}</em></div>
              <div class="preview-screen">
                <img src="{root}{shot(p, 'desktop')}" alt="" class="preview-poster" loading="lazy" decoding="async" width="1440" height="900">
                <button type="button" class="preview-load btn btn-primary">{ICON['play']} Load live preview</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="case-cta">
      <div class="case-wrap cta-box reveal">
        <h2>Like what you see?</h2>
        <p>I can build a fast, beautiful and responsive website like this for your business too.</p>
        <div class="case-actions">
          <a class="btn cta-light btn-shine magnetic" href="{root}hire-me/">Start a project {ICON['arrow']}</a>
          <a class="btn cta-outline magnetic" href="{p['live']}" target="_blank" rel="noopener">Visit live website {ICON['ext']}</a>
        </div>
      </div>
    </section>

    <nav class="case-wrap project-nav" aria-label="More projects">
      <a class="pn-link reveal" href="{root}projects/{prv['slug']}/"><span>{ICON['back']} Previous project</span><strong>{prv['full']}</strong></a>
      <a class="pn-link next reveal" href="{root}projects/{nxt['slug']}/"><span>Next project {ICON['arrow']}</span><strong>{nxt['full']}</strong></a>
    </nav>
  </main>
  <div class="lightbox" id="lightbox" hidden>
    <button type="button" class="lightbox-close" aria-label="Close">&times;</button>
    <figure><img src="" alt=""><figcaption></figcaption></figure>
  </div>
''' + footer(root, ('projects/project.js',))


def not_found():
    root = '/Portfolio/'
    return head(root, '404.html', 'Page not found | Afsheen Kiran', 'This page could not be found.') + header(root, '404') + f'''
  <main id="main">
{page_hero('Error 404', 'Page not <span class="gradient-text">found</span>', 'The page you were looking for has moved or does not exist.', f"""
        <div class="hero-actions reveal"><a class="btn btn-primary magnetic" href="{root}">Go to homepage {ICON['arrow']}</a><a class="btn btn-ghost magnetic" href="{root}projects/">See projects</a></div>""")}
  </main>
''' + footer(root)


def sitemap():
    urls = ['', 'about/', 'skills/', 'projects/', 'contact/', 'hire-me/'] + [f"projects/{p['slug']}/" for p in PROJECTS]
    body = ''.join(f'  <url><loc>{BASE}{u}</loc><lastmod>2026-10-26</lastmod></url>\n' for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


if __name__ == '__main__':
    write('index.html', home())
    write('about/index.html', about())
    write('skills/index.html', skills())
    write('projects/index.html', projects_index())
    write('contact/index.html', contact())
    write('hire-me/index.html', hire())
    for i, proj in enumerate(PROJECTS):
        write(f"projects/{proj['slug']}/index.html", case_page(proj, i))
    write('404.html', not_found())
    write('sitemap.xml', sitemap())
