//This is an iframe embed code, not a link. The embed code is video dependent. I know we typically like to avoid stringified HTML, but this is a notable exception where the HTML is designed for this exact use-case.
const heroLink =
    '<iframe width="100%" height="600px" src="https://www.youtube.com/embed/5atxB5RRUvI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';

const saveWithMenuLink =
    'https://drive.google.com/uc?id=1Dln5UAUWBWwxx2KObHgkU7B7fnvOW0Ym';
const saveWithButtonLink =
    'https://drive.google.com/uc?id=18AVF0Yqe8ESjOVEH9WAsZOofi9xdD7Jl';
const searchLink =
    'https://drive.google.com/uc?id=1Sr6OCIiT0aSa0Bs_gZK-IWgOC9Il9QUc';
const shareLink =
    'https://drive.google.com/uc?id=1Y5l2wsQhJTu1cwQm_rWJXkqyYd79fAEK';

export const onboardingMD =
    `

# Elevate your Jupyter experience with Pieces

<div class="nav">
    <a href="https://docs.pieces.app/extensions-plugins/obsidian" style="display: inline-block; text-decoration: none; border-radius: 4px;">Docs</a>		<a href="https://pieces.app" style="display: inline-block; text-decoration: none; border-radius: 4px;">Learn More</a>
</div>

<div class="hero">

` +
    heroLink +
    `
</div>

## Your Guide to Getting Started with Pieces for Developers Jupyter Plugin

#### 1. Save your first snippet
- To save a snippet, highlight the text, right-click, and select "Save to Pieces."
![Save to Pieces via Menu](${saveWithMenuLink})

**Additional ways to save**
- Click the Pieces Save button within any code block.
![Save to Pieces via Button](${saveWithButtonLink})

- Highlight the desired code and use our dedicated keyboard shortcuts
<div class="img onboarding-keyboardShortcuts"></div>
<div class="img onboarding-saveWithShortcut"></div>


#### 2. Find & use your snippets
- To access your saved snippets, click on the Pieces icon in your left sidebar.
![Search Your Pieces](${searchLink})


#### 3. Share your Snippets
- Collaborate with others with ease using shareable links for your snippets
![Share you Snippets](${shareLink})


### Maximize productivity with our Flagship Desktop App
Utilize the Pieces [Flagship Desktop App](https://pieces.app) in combination with our Jupyter Plugin to streamline your workflow and enhance your development productivity.

- Get back in flow with our Workflow Activity View
- Save time with In-Project Snippet Discovery
- Enjoy real-time and scope-relevant suggestions
- Extract and use code and text from screenshots
<div class="img onboarding-withDesktopApp"></div>

### Socials

<a href="https://discord.gg/GkmyfqWf3W" style="display: inline-block; text-decoration: none; border-radius: 4px;">Discord</a>		<a href="https://www.youtube.com/@getpieces" style="display: inline-block; text-decoration: none; border-radius: 4px;">YouTube</a>		<a href="https://twitter.com/@getpieces" style="display: inline-block; text-decoration: none; border-radius: 4px;">Twitter</a>		<a href="https://www.linkedin.com/company/getpieces" style="display: inline-block; text-decoration: none; border-radius: 4px;">LinkedIn</a>		<a href="https://www.facebook.com/getpieces" style="display: inline-block; text-decoration: none; border-radius: 4px;">Facebook</a>
`;
