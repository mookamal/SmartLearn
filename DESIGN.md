# Design System Specification: The Cognitive Catalyst

## 1. Overview & Creative North Star
The "Cognitive Catalyst" is the creative North Star for this design system. It moves the user away from the generic, cold "SaaS dashboard" aesthetic and toward a sophisticated, editorial learning environment. 

This system is built on the philosophy that learning requires both high-focus immersion and high-energy motivation. To achieve this, we break the "template" look by using **intentional asymmetry**, **layered depth**, and **tonal hierarchy**. We treat the UI not as a flat screen, but as a series of physical, high-quality materials—fine paper, frosted glass, and deep ink—organized to guide the mind.

---

## 2. Colors: Psychology of the Mind
We use a palette specifically tuned to cognitive states. Blue is discarded in favor of **Deep Indigo** for deep work, **Amber** for motivational triggers, and **Teal** for the satisfaction of achievement.

### Primary: Deep Indigo (Focus)
*   `primary`: `#1c0070` | `on_primary`: `#ffffff`
*   `primary_container`: `#311b92`
*   **Usage:** Reserved for the core "Deep Work" areas—navigation, primary headings, and focus-intensive actions. It anchors the eye and signals a professional, scholarly environment.

### Secondary: Amber (Motivation)
*   `secondary`: `#7e5700` | `on_secondary`: `#ffffff`
*   `secondary_container`: `#feb300`
*   **Usage:** Used for "Energy" moments. CTAs, progress highlights, and motivational prompts. It provides a warm contrast to the Indigo, preventing the UI from feeling too heavy.

### Tertiary: Teal (Achievement)
*   `tertiary`: `#002420` | `tertiary_fixed`: `#8df5e4`
*   **Usage:** Used for "Success" states and completion markers. It represents the "cool-down" and clarity that follows a successful learning session.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to define sections. Boundaries must be created through background color shifts. Use `surface_container_low` (`#f7f2f8`) for the page background and `surface_container_lowest` (`#ffffff`) for content blocks to create a soft, natural edge.

### The "Glass & Gradient" Rule
For hero sections or primary CTAs, use subtle gradients transitioning from `primary` (`#1c0070`) to `primary_container` (`#311b92`). For floating overlays (like profile menus), use a backdrop-blur (12px–20px) with a semi-transparent `surface` color to create an "Editorial Glass" effect.

---

## 3. Typography: The Editorial Voice
We utilize **Plus Jakarta Sans** for its modern, geometric clarity. The scale is designed to create high-contrast hierarchy, making complex information feel digestible.

*   **Display (lg/md/sm):** Used for high-impact landing moments or course titles. Tight letter spacing (-2%) to give it an authoritative, "magazine" feel.
*   **Headline (lg/md/sm):** 1.5rem to 2rem. Used to break up content sections. These should always use the `primary` color to maintain the Focus anchor.
*   **Title (lg/md/sm):** 1rem to 1.375rem. Used for card headers and module titles.
*   **Body (lg/md/sm):** 0.75rem to 1rem. Specifically use `on_surface_variant` (`#474553`) for body-md to reduce eye strain during long reading sessions.
*   **Label (md/sm):** Used for micro-copy and metadata.

---

## 4. Elevation & Depth: Tonal Layering
Instead of traditional shadows, we communicate hierarchy through the **Layering Principle**.

### Surface Hierarchy
Stack tiers to define importance:
1.  **Base:** `surface` (`#fdf8fd`)
2.  **Sectioning:** `surface_container_low` (`#f7f2f8`)
3.  **Content Cards:** `surface_container_lowest` (`#ffffff`)
4.  **Raised Elements:** `surface_bright` (`#fdf8fd`)

### Ambient Shadows
Shadows should feel like natural light, not digital effects.
*   **Subtle (Cards):** 0px 4px 20px rgba(28, 27, 31, 0.04) (using a tint of `on_surface`).
*   **Deep (Modals):** 0px 12px 40px rgba(28, 27, 31, 0.08).

### The "Ghost Border" Fallback
If contrast is needed for accessibility, use the `outline_variant` (`#c9c4d5`) at **15% opacity**. Never use a 100% opaque border.

---

## 5. Components: Principles of Interaction

### Buttons
*   **Primary:** Indigo (`primary`) with an 8px (`sm`) or 12px (`md`) radius. High-end buttons should use a subtle inner-glow (1px white top-border at 10% opacity) to feel tactile.
*   **Secondary:** Amber (`secondary_container`). Use for "Next Lesson" or "Start Quiz."
*   **Tertiary:** No background. Use `title-sm` typography with a 4px bottom-margin indicator.

### Cards & Modules
*   **Rule:** Forbid divider lines. Use `surface_container` transitions.
*   **Radius:** 16px (`xl`) for large course containers; 12px (`lg`) for internal lesson cards.
*   **Spacing:** Use the 4px grid. Standard card padding is 24px (6 units).

### Inputs & Fields
*   **State:** Default state should use `surface_container_high` (`#ebe7ec`) background with no border.
*   **Focus:** Transition to a 2px `primary` bottom-border only (no full box-stroke) to maintain the editorial look.

### Learning-Specific Components
*   **Focus-Mode Overlay:** A full-screen `surface` container with a 40px backdrop blur, stripping away navigation to leave only the content and a "close" action.
*   **Achievement Chips:** Use `tertiary_fixed_dim` (`#70d8c8`) with `on_tertiary_fixed` text for a sophisticated "badge" look.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical margins (e.g., more white space on the left than the right in hero sections) to create an editorial feel.
*   **Do** use the 4px grid religiously for all padding and margins.
*   **Do** leverage "Surface Nesting" to separate content instead of adding lines.
*   **Do** use the `secondary` (Amber) sparingly—it is a high-energy "spark," not a primary theme.

### Don’t:
*   **Don’t** use pure black (#000000) for text. Use `on_surface` (`#1c1b1f`).
*   **Don’t** use standard 1px borders. If a container feels lost, increase the background contrast or add an Ambient Shadow.
*   **Don’t** use more than three levels of depth on a single screen.
*   **Don’t** use generic blue icons. Always pull from the `primary`, `secondary`, or `tertiary` tokens.