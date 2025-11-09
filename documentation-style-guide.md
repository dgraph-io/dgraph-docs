
# Dgraph Documentation Style Guide

This style guide provides editorial guidelines for writing developer documentation for Dgraph database and related projects.

## Goals and Audience

This guide helps you write documentation that is consistent with existing documentation and as easy as possible to understand. Everything in this guide is a guideline, not a rigid rule—diverge when it makes your documentation better.

## Voice & Tone

- **Be conversational and friendly** – sound like a knowledgeable friend, not pedantic
- **Write for a global audience** – many readers are non-native English speakers
- **Use second person** – address the reader as "you," not "we"
- **Use active voice** – make clear who's performing the action
- **Use present tense**
- **Address Dgraph in third person** – "Dgraph provides..." not "we provide..."

## Content Types

Identify the type of content you're creating and try to follow the [Diátaxis framework](https://diataxis.fr/) for organizing documentation:

- **Tutorials** – Step-by-step learning paths for beginners. Start with prerequisites, guide through each step, and end with next steps.
- **How-to guides** – Goal-oriented instructions for specific tasks. Assume some knowledge, focus on the problem, provide clear steps.
- **Reference documentation** – Comprehensive technical details (API methods, configuration options, command syntax). Be thorough, consistent, and precise.
- **Explanations** – Clarify how things work and why. Provide context, background, and understanding without step-by-step instructions.

Consider stating the content type at the beginning if it helps readers understand what to expect.

## Structure & Readability

- **Front-load key information** – put the main point in the first sentence
- **Break up large paragraphs** – use headings, lists, and shorter sections
- **Keep sentences short** – aim for under 26 words
- **Use parallel structures** – make similar items grammatically consistent
- **Define abbreviations** on first use and repeat as needed
- **Provide context** – don't assume readers already know what you're talking about
- **Avoid negative constructions** when possible – tell readers what they can do, not what they can't

## Headings & Titles

- **Page titles**: Title Case ("Deploy Your App in Production")
- **Section headings**: Sentence case ("Test your schema with a simple UI")

## Formatting Conventions

- **`code font`** – command-line input/output, code entity names (variables, functions, types, etc.)
- **`italic code font`** – placeholders the reader should replace (server names, custom values)
- ***italic*** – introducing a term for the first time
- **bold** – file/directory names, UI elements, error messages, emphasis (sparingly)

In Markdown, use backticks (`` ` ``) for code font.

## Lists & Organization

- **Numbered lists** – for sequential steps
- **Bulleted lists** – for most other lists
- **Description lists** – for related pairs of data
- **Use serial commas** – include comma before final "and" or "or"

## Links

Write descriptive link text that makes sense on its own:
- Use the exact title/heading you're linking to, OR
- Describe the destination in plain language

Avoid generic phrases like "click here" or "read more."

### Internal Links with `relref`

Use Hugo's `relref` shortcode for internal links to other documentation pages:

```
[link text]({{< relref "filename.md" >}})
```

For links to specific sections, include the anchor:
```
[link text]({{< relref "filename.md#section-anchor" >}})
```

For files in subdirectories, use absolute paths from the `content` directory:
```
[link text]({{< relref "/path/to/file.md" >}})
```

**Examples:**
- `{{< relref "dgraph-glossary.md#entity" >}}` - Links to the entity section in glossary
- `{{< relref "/dql/query/functions.md#aggregation-functions" >}}` - Links to a section in a subdirectory

**Best practices:**
- Always use `relref` for internal documentation links
- Use descriptive link text that makes sense without context
- Test links after adding them to ensure they resolve correctly

## Images and Figures

Use Hugo shortcodes to include images in documentation:

### Figure Shortcode

Use the `figure` shortcode for images with captions and optional styling:

```
{{<figure class="medium image" src="/images/path/to/image.png" title="Image Title" alt="Alt text">}}
```

**Attributes:**
- `src`: Path to image file (stored in `static/images/`)
- `title`: Caption displayed with the image
- `alt`: Alternative text for accessibility (required)
- `class`: Optional styling class (e.g., `"medium image"`, `"large image"`)

**Example:**
```
{{<figure class="medium image" src="/images/tutorials/graph-example.png" title="Example graph structure" alt="A graph showing nodes and relationships">}}
```

### Load-img Shortcode

Use `load-img` for simple images without captions:

```
{{% load-img "/images/path/to/image.png" "Alt text" %}}
```

**Best practices:**
- Store images in `static/images/` directory
- Always provide descriptive `alt` text for accessibility
- Use descriptive file names (e.g., `graph-example.png` not `img1.png`)
- Keep image file sizes reasonable for web performance
- Use `figure` for images that need captions or explanations
- Use `load-img` for simple inline images

## Grammar & Language

- **Put conditions before instructions** – "If X, do Y" not "Do Y if X"
- **Use unambiguous dates** – YYYY-MM-DD format
- **Use US English spelling and punctuation**
- **Don't use the same word to mean different things**
- **Avoid jargon** – spell out abbreviations on first use

## What Not to Do

- **Don't pre-announce features** – document what exists now, not future plans
- **Don't be overly colloquial or frivolous** – maintain professionalism
- **Don't assume the reader's context** – provide necessary background

---

*This guide is derived from Google's developer documentation style guide and O'Reilly Media's editorial standards.*